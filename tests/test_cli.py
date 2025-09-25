"""Test cases for CLI functionality."""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from proposal_generator.cli import create_parser, main


class TestCreateParser:
    """Test CLI argument parser creation."""

    def test_parser_creation(self):
        """Test that parser is created successfully."""
        parser = create_parser()
        assert parser is not None
        assert parser.description == "AI-powered Proposal Generator"

    def test_required_input_argument(self):
        """Test required input argument parsing."""
        parser = create_parser()

        # Valid argument
        args = parser.parse_args(["--input", "test.txt"])
        assert args.input == "test.txt"

        # Missing required argument should raise error
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_optional_arguments(self):
        """Test optional argument parsing."""
        parser = create_parser()

        args = parser.parse_args(
            [
                "--input",
                "transcript.txt",
                "--output",
                "./custom_output",
                "--filename",
                "custom_proposal",
                "--model",
                "gpt-3.5-turbo",
            ]
        )

        assert args.input == "transcript.txt"
        assert args.output == "./custom_output"
        assert args.filename == "custom_proposal"
        assert args.model == "gpt-3.5-turbo"

    def test_default_values(self):
        """Test default argument values."""
        parser = create_parser()
        args = parser.parse_args(["--input", "test.txt"])

        assert args.output == "./outputs"
        assert args.filename is None
        assert args.model == "gpt-4"

    def test_version_argument(self):
        """Test version argument."""
        parser = create_parser()

        # Should not raise exception
        args = parser.parse_args(["--input", "test.txt", "--version"])
        assert args.version is True


class TestMainFunction:
    """Test main CLI function."""

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    def test_main_with_missing_input_file(self, capsys):
        """Test main function with non-existent input file."""
        with patch("sys.argv", ["proposal-generator", "--input", "nonexistent.txt"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "not found" in captured.out

    def test_main_without_api_key(self, capsys):
        """Test main function without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("sys.argv", ["proposal-generator", "--input", "test.txt"]):
                with patch("os.path.exists", return_value=True):
                    with pytest.raises(SystemExit) as exc_info:
                        main()

                    assert exc_info.value.code == 1
                    captured = capsys.readouterr()
                    assert "OPENAI_API_KEY" in captured.out

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("proposal_generator.cli.ProposalWorkflow")
    def test_main_successful_execution(self, mock_workflow, tmp_path):
        """Test successful main execution."""
        # Create temporary input file
        input_file = tmp_path / "test_transcript.txt"
        input_file.write_text("Test transcript content")

        # Mock workflow
        mock_instance = MagicMock()
        mock_instance.process_transcript_file.return_value = {
            "success": True,
            "file_paths": {
                "markdown": "/path/to/proposal.md",
                "json": "/path/to/proposal.json",
            },
        }
        mock_workflow.return_value = mock_instance

        test_args = [
            "proposal-generator",
            "--input",
            str(input_file),
            "--output",
            str(tmp_path),
            "--filename",
            "test_proposal",
        ]

        with patch("sys.argv", test_args):
            try:
                main()
            except SystemExit as e:
                # Should exit with code 0 on success
                assert e.code == 0

        # Verify workflow was called correctly
        mock_workflow.assert_called_once_with(model_name="gpt-4")
        mock_instance.process_transcript_file.assert_called_once_with(
            file_path=str(input_file),
            output_folder=str(tmp_path),
            filename="test_proposal",
        )

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("proposal_generator.cli.ProposalWorkflow")
    def test_main_workflow_error(self, mock_workflow, tmp_path, capsys):
        """Test main function handling workflow errors."""
        # Create temporary input file
        input_file = tmp_path / "test_transcript.txt"
        input_file.write_text("Test transcript content")

        # Mock workflow with error
        mock_instance = MagicMock()
        mock_instance.process_transcript_file.return_value = {
            "success": False,
            "error": "Processing failed",
        }
        mock_workflow.return_value = mock_instance

        test_args = [
            "proposal-generator",
            "--input",
            str(input_file),
            "--output",
            str(tmp_path),
        ]

        with patch("sys.argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Processing failed" in captured.out

    def test_main_version_display(self, capsys):
        """Test version display."""
        with patch(
            "sys.argv", ["proposal-generator", "--input", "test.txt", "--version"]
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0
            captured = capsys.readouterr()
            assert "AI Proposal Generator" in captured.out

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("proposal_generator.cli.ProposalWorkflow")
    def test_main_with_custom_model(self, mock_workflow, tmp_path):
        """Test main function with custom AI model."""
        # Create temporary input file
        input_file = tmp_path / "test_transcript.txt"
        input_file.write_text("Test transcript content")

        # Mock workflow
        mock_instance = MagicMock()
        mock_instance.process_transcript_file.return_value = {
            "success": True,
            "file_paths": {
                "markdown": "/path/to/proposal.md",
                "json": "/path/to/proposal.json",
            },
        }
        mock_workflow.return_value = mock_instance

        test_args = [
            "proposal-generator",
            "--input",
            str(input_file),
            "--model",
            "gpt-3.5-turbo",
        ]

        with patch("sys.argv", test_args):
            try:
                main()
            except SystemExit:
                pass

        # Verify workflow was initialized with custom model
        mock_workflow.assert_called_once_with(model_name="gpt-3.5-turbo")

    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
    @patch("proposal_generator.cli.ProposalWorkflow")
    def test_main_exception_handling(self, mock_workflow, tmp_path, capsys):
        """Test main function handling unexpected exceptions."""
        # Create temporary input file
        input_file = tmp_path / "test_transcript.txt"
        input_file.write_text("Test transcript content")

        # Mock workflow to raise exception
        mock_workflow.side_effect = Exception("Unexpected error")

        test_args = ["proposal-generator", "--input", str(input_file)]

        with patch("sys.argv", test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Unexpected error" in captured.out
