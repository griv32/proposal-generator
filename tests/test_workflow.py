"""Test cases for ProposalWorkflow functionality."""

import os
from unittest.mock import mock_open, patch

import pytest

from proposal_generator.models import (
    CustomerInfo,
    ImplementationPhase,
    ProjectRequirements,
    ProposalData,
)
from proposal_generator.workflow import ProposalWorkflow


class TestProposalWorkflow:
    """Test ProposalWorkflow functionality."""

    @pytest.fixture
    def mock_components(self):
        """Mock all workflow components."""
        with (
            patch("proposal_generator.workflow.TranscriptionProcessor") as mock_tp,
            patch("proposal_generator.workflow.ProposalGenerator") as mock_pg,
            patch("proposal_generator.workflow.OutputFormatter") as mock_of,
        ):
            yield mock_tp, mock_pg, mock_of

    @pytest.fixture
    def workflow(self, mock_components):
        """Create a ProposalWorkflow instance with mocked components."""
        with (
            patch("proposal_generator.workflow.load_dotenv"),
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}),
        ):
            return ProposalWorkflow("gpt-4")

    @pytest.fixture
    def sample_customer(self):
        """Sample customer for testing."""
        return CustomerInfo(
            company_name="Test Corp", industry="Technology", contact_person="John Doe"
        )

    @pytest.fixture
    def sample_requirements(self):
        """Sample requirements for testing."""
        return ProjectRequirements(scope="Test project", timeline="3 months")

    @pytest.fixture
    def sample_proposal(self, sample_customer, sample_requirements):
        """Sample proposal data for testing."""
        phases = [
            ImplementationPhase(
                name="Phase 1",
                activities=["Activity 1"],
                duration_weeks=2,
                deliverables=["Deliverable 1"],
            )
        ]
        return ProposalData(
            customer_info=sample_customer,
            requirements=sample_requirements,
            executive_summary="Test summary",
            what_success_looks_like="Success vision",
            implementation_phases=phases,
            investment_summary="Investment details",
            roi_analysis="ROI details",
            next_steps=["Step 1", "Step 2"],
        )

    def test_init_success(self, mock_components):
        """Test successful ProposalWorkflow initialization."""
        mock_tp, mock_pg, mock_of = mock_components

        with (
            patch("proposal_generator.workflow.load_dotenv") as mock_load_dotenv,
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}),
        ):

            workflow = ProposalWorkflow("gpt-3.5-turbo")

            # Verify environment loading and API key check
            mock_load_dotenv.assert_called_once()

            # Verify components were initialized with correct model
            mock_tp.assert_called_once_with("gpt-3.5-turbo")
            mock_pg.assert_called_once_with("gpt-3.5-turbo")
            mock_of.assert_called_once()

            assert workflow.model_name == "gpt-3.5-turbo"

    def test_init_default_model(self, mock_components):
        """Test ProposalWorkflow initialization with default model."""
        mock_tp, mock_pg, mock_of = mock_components

        with (
            patch("proposal_generator.workflow.load_dotenv"),
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}),
        ):

            ProposalWorkflow()

            mock_tp.assert_called_once_with("gpt-4")
            mock_pg.assert_called_once_with("gpt-4")

    def test_init_missing_api_key(self, mock_components):
        """Test ProposalWorkflow initialization without API key."""
        with (
            patch("proposal_generator.workflow.load_dotenv"),
            patch.dict(os.environ, {}, clear=True),
            pytest.raises(
                ValueError, match="OPENAI_API_KEY environment variable is not set"
            ),
        ):
            ProposalWorkflow()

    def test_check_api_key_present(self):
        """Test _check_api_key when API key is present."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            workflow = ProposalWorkflow.__new__(ProposalWorkflow)  # Create without init
            workflow._check_api_key()  # Should not raise

    def test_check_api_key_missing(self):
        """Test _check_api_key when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            workflow = ProposalWorkflow.__new__(ProposalWorkflow)  # Create without init
            with pytest.raises(
                ValueError, match="OPENAI_API_KEY environment variable is not set"
            ):
                workflow._check_api_key()

    def test_process_transcript_text_success(
        self, workflow, sample_customer, sample_requirements, sample_proposal, capsys
    ):
        """Test successful transcript text processing."""
        # Mock component responses
        workflow.transcription_processor.extract_customer_info.return_value = (
            sample_customer
        )
        workflow.transcription_processor.extract_project_requirements.return_value = (
            sample_requirements
        )
        workflow.proposal_generator.generate_proposal.return_value = sample_proposal
        workflow.output_formatter.save_outputs.return_value = {
            "markdown": "/path/to/proposal.md",
            "json": "/path/to/proposal.json",
        }

        transcript_text = "Sample transcript content"
        result = workflow.process_transcript_text(
            transcript_text, "./outputs", "custom_filename"
        )

        # Verify result structure
        assert result["success"] is True
        assert result["customer_info"] == sample_customer
        assert result["requirements"] == sample_requirements
        assert result["proposal_data"] == sample_proposal
        assert result["file_paths"]["markdown"] == "/path/to/proposal.md"
        assert result["file_paths"]["json"] == "/path/to/proposal.json"
        assert result["total_duration_weeks"] == 2

        # Verify component calls
        workflow.transcription_processor.extract_customer_info.assert_called_once_with(
            transcript_text
        )
        workflow.transcription_processor.extract_project_requirements.assert_called_once_with(
            transcript_text, sample_customer
        )
        workflow.proposal_generator.generate_proposal.assert_called_once_with(
            sample_customer, sample_requirements
        )
        workflow.output_formatter.save_outputs.assert_called_once_with(
            sample_proposal, "./outputs", "custom_filename"
        )

        # Verify console output
        captured = capsys.readouterr()
        assert "Processing transcript..." in captured.out
        assert "Step 1: Extracting customer information..." in captured.out
        assert "Step 2: Extracting project requirements..." in captured.out
        assert "Step 3: Generating comprehensive proposal..." in captured.out
        assert "Step 4: Formatting and saving outputs..." in captured.out
        assert "Step 5: Process complete!" in captured.out
        assert "Extracted info for: Test Corp" in captured.out

    def test_process_transcript_text_default_params(
        self, workflow, sample_customer, sample_requirements, sample_proposal
    ):
        """Test transcript processing with default parameters."""
        workflow.transcription_processor.extract_customer_info.return_value = (
            sample_customer
        )
        workflow.transcription_processor.extract_project_requirements.return_value = (
            sample_requirements
        )
        workflow.proposal_generator.generate_proposal.return_value = sample_proposal
        workflow.output_formatter.save_outputs.return_value = {
            "markdown": "/path/to/proposal.md",
            "json": "/path/to/proposal.json",
        }

        workflow.process_transcript_text("test transcript")

        # Verify default parameters were passed
        workflow.output_formatter.save_outputs.assert_called_once_with(
            sample_proposal, "./outputs", None
        )

    def test_process_transcript_text_error_handling(self, workflow, capsys):
        """Test error handling in transcript text processing."""
        # Mock an error in customer extraction
        workflow.transcription_processor.extract_customer_info.side_effect = Exception(
            "Test error"
        )

        result = workflow.process_transcript_text("test transcript")

        assert result["success"] is False
        assert "Test error" in result["error"]

        # Verify error output
        captured = capsys.readouterr()
        assert "ERROR: Error during processing: Test error" in captured.out

    def test_process_transcript_file_success(
        self, workflow, sample_customer, sample_requirements, sample_proposal
    ):
        """Test successful transcript file processing."""
        # Mock file operations
        transcript_content = "Sample transcript from file"
        mock_file_data = mock_open(read_data=transcript_content)

        # Mock component responses
        workflow.transcription_processor.extract_customer_info.return_value = (
            sample_customer
        )
        workflow.transcription_processor.extract_project_requirements.return_value = (
            sample_requirements
        )
        workflow.proposal_generator.generate_proposal.return_value = sample_proposal
        workflow.output_formatter.save_outputs.return_value = {
            "markdown": "/path/to/proposal.md",
            "json": "/path/to/proposal.json",
        }

        with (
            patch("builtins.open", mock_file_data),
            patch("os.path.exists", return_value=True),
        ):

            result = workflow.process_transcript_file(
                "/path/to/transcript.txt", "./outputs", "custom_filename"
            )

        # Verify result
        assert result["success"] is True
        assert result["customer_info"] == sample_customer

        # Verify file was read
        mock_file_data.assert_called_once_with(
            "/path/to/transcript.txt", encoding="utf-8"
        )

        # Verify transcript content was passed to processor
        workflow.transcription_processor.extract_customer_info.assert_called_once_with(
            transcript_content
        )

    def test_process_transcript_file_not_found(self, workflow, capsys):
        """Test processing when transcript file doesn't exist."""
        with patch("os.path.exists", return_value=False):
            result = workflow.process_transcript_file("/nonexistent/file.txt")

        assert result["success"] is False
        assert "Transcript file not found: /nonexistent/file.txt" in result["error"]

        captured = capsys.readouterr()
        assert "ERROR: Error reading transcript file:" in captured.out

    def test_process_transcript_file_empty(self, workflow, capsys):
        """Test processing when transcript file is empty."""
        mock_file_data = mock_open(read_data="")

        with (
            patch("builtins.open", mock_file_data),
            patch("os.path.exists", return_value=True),
        ):

            result = workflow.process_transcript_file("/path/to/empty.txt")

        assert result["success"] is False
        assert "Transcript file is empty" in result["error"]

    def test_process_transcript_file_whitespace_only(self, workflow, capsys):
        """Test processing when transcript file contains only whitespace."""
        mock_file_data = mock_open(read_data="   \n\t  \n  ")

        with (
            patch("builtins.open", mock_file_data),
            patch("os.path.exists", return_value=True),
        ):

            result = workflow.process_transcript_file("/path/to/whitespace.txt")

        assert result["success"] is False
        assert "Transcript file is empty" in result["error"]

    def test_process_transcript_file_read_error(self, workflow, capsys):
        """Test handling of file read errors."""
        with (
            patch("os.path.exists", return_value=True),
            patch("builtins.open", side_effect=OSError("Permission denied")),
        ):

            result = workflow.process_transcript_file("/path/to/file.txt")

        assert result["success"] is False
        assert "Permission denied" in result["error"]

        captured = capsys.readouterr()
        assert "ERROR: Error reading transcript file:" in captured.out

    def test_process_transcript_file_default_params(
        self, workflow, sample_customer, sample_requirements, sample_proposal
    ):
        """Test transcript file processing with default parameters."""
        mock_file_data = mock_open(read_data="test content")

        workflow.transcription_processor.extract_customer_info.return_value = (
            sample_customer
        )
        workflow.transcription_processor.extract_project_requirements.return_value = (
            sample_requirements
        )
        workflow.proposal_generator.generate_proposal.return_value = sample_proposal
        workflow.output_formatter.save_outputs.return_value = {
            "markdown": "/path/to/proposal.md",
            "json": "/path/to/proposal.json",
        }

        with (
            patch("builtins.open", mock_file_data),
            patch("os.path.exists", return_value=True),
        ):

            workflow.process_transcript_file("/path/to/file.txt")

        # Verify default parameters were used
        workflow.output_formatter.save_outputs.assert_called_once_with(
            sample_proposal, "./outputs", None
        )

    def test_process_transcript_file_console_output(
        self, workflow, sample_customer, sample_requirements, sample_proposal, capsys
    ):
        """Test console output during file processing."""
        mock_file_data = mock_open(read_data="test content")

        workflow.transcription_processor.extract_customer_info.return_value = (
            sample_customer
        )
        workflow.transcription_processor.extract_project_requirements.return_value = (
            sample_requirements
        )
        workflow.proposal_generator.generate_proposal.return_value = sample_proposal
        workflow.output_formatter.save_outputs.return_value = {
            "markdown": "/path/to/proposal.md",
            "json": "/path/to/proposal.json",
        }

        with (
            patch("builtins.open", mock_file_data),
            patch("os.path.exists", return_value=True),
        ):

            workflow.process_transcript_file("/path/to/transcript.txt")

        captured = capsys.readouterr()
        assert "Reading transcript from: /path/to/transcript.txt" in captured.out
