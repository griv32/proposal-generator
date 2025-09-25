"""Test cases for TranscriptionProcessor functionality."""

import json
from unittest.mock import MagicMock, patch

import pytest

from proposal_generator.models import CustomerInfo, ProjectRequirements
from proposal_generator.transcription_processor import TranscriptionProcessor


class TestTranscriptionProcessor:
    """Test TranscriptionProcessor functionality."""

    @pytest.fixture
    def processor(self):
        """Create a TranscriptionProcessor instance for testing."""
        with patch("proposal_generator.transcription_processor.ChatOpenAI"):
            return TranscriptionProcessor("gpt-4")

    @pytest.fixture
    def mock_llm_response_customer(self):
        """Mock LLM response for customer extraction."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "company_name": "Test Corp",
                "industry": "Technology",
                "contact_person": "John Doe",
                "email": "john@testcorp.com",
                "phone": "+1-555-0123",
            }
        )
        return mock_response

    @pytest.fixture
    def mock_llm_response_requirements(self):
        """Mock LLM response for requirements extraction."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "scope": "Modernize legacy systems",
                "timeline": "6 months",
                "budget": "$200K-$500K",
                "technical_needs": ["POS upgrade", "Cloud migration"],
                "key_deliverables": ["System uptime", "Mobile support"],
            }
        )
        return mock_response

    def test_init(self):
        """Test TranscriptionProcessor initialization."""
        with patch("proposal_generator.transcription_processor.ChatOpenAI") as mock_llm:
            processor = TranscriptionProcessor("gpt-3.5-turbo")

            # Verify LLM was initialized correctly
            mock_llm.assert_called_once_with(model_name="gpt-3.5-turbo")
            assert processor.llm.temperature == 0.3

    def test_init_default_model(self):
        """Test TranscriptionProcessor initialization with default model."""
        with patch("proposal_generator.transcription_processor.ChatOpenAI") as mock_llm:
            processor = TranscriptionProcessor()

            mock_llm.assert_called_once_with(model_name="gpt-4")

    def test_extract_customer_info_success(self, processor, mock_llm_response_customer):
        """Test successful customer information extraction."""
        processor.llm.invoke = MagicMock(return_value=mock_llm_response_customer)

        transcript = "Discovery call with Test Corp, John Doe speaking..."
        result = processor.extract_customer_info(transcript)

        assert isinstance(result, CustomerInfo)
        assert result.company_name == "Test Corp"
        assert result.industry == "Technology"
        assert result.contact_person == "John Doe"
        assert result.email == "john@testcorp.com"
        assert result.phone == "+1-555-0123"

        # Verify LLM was called with correct prompt
        processor.llm.invoke.assert_called_once()
        call_args = processor.llm.invoke.call_args[0][0]
        assert transcript in call_args
        assert "company_name" in call_args
        assert "industry" in call_args

    def test_extract_customer_info_with_wrapped_json(self, processor):
        """Test customer extraction with JSON wrapped in text."""
        mock_response = MagicMock()
        mock_response.content = """Here is the extracted information:

        {
            "company_name": "Acme Corp",
            "industry": "Manufacturing",
            "contact_person": "Jane Smith",
            "email": null,
            "phone": null
        }

        This completes the extraction."""

        processor.llm.invoke = MagicMock(return_value=mock_response)

        result = processor.extract_customer_info("test transcript")

        assert isinstance(result, CustomerInfo)
        assert result.company_name == "Acme Corp"
        assert result.industry == "Manufacturing"
        assert result.contact_person == "Jane Smith"
        assert result.email is None
        assert result.phone is None

    def test_extract_customer_info_null_cleanup(self, processor):
        """Test that null strings are cleaned up properly."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "company_name": "Test Corp",
                "industry": "Technology",
                "contact_person": "John Doe",
                "email": "null",
                "phone": "",
            }
        )
        processor.llm.invoke = MagicMock(return_value=mock_response)

        result = processor.extract_customer_info("test transcript")

        assert result.email is None
        assert result.phone is None

    def test_extract_customer_info_invalid_json(self, processor):
        """Test handling of invalid JSON response."""
        mock_response = MagicMock()
        mock_response.content = "This is not valid JSON"
        processor.llm.invoke = MagicMock(return_value=mock_response)

        with pytest.raises(ValueError, match="Failed to parse customer information"):
            processor.extract_customer_info("test transcript")

    def test_extract_project_requirements_success(
        self, processor, mock_llm_response_requirements
    ):
        """Test successful project requirements extraction."""
        processor.llm.invoke = MagicMock(return_value=mock_llm_response_requirements)

        customer_info = CustomerInfo(
            company_name="Test Corp", industry="Technology", contact_person="John Doe"
        )
        transcript = "We need to modernize our systems..."

        result = processor.extract_project_requirements(transcript, customer_info)

        assert isinstance(result, ProjectRequirements)
        assert result.scope == "Modernize legacy systems"
        assert result.timeline == "6 months"
        assert result.budget == "$200K-$500K"
        assert result.technical_needs == ["POS upgrade", "Cloud migration"]
        assert result.key_deliverables == ["System uptime", "Mobile support"]

        # Verify LLM was called with correct prompt
        processor.llm.invoke.assert_called_once()
        call_args = processor.llm.invoke.call_args[0][0]
        assert transcript in call_args
        assert customer_info.company_name in call_args

    def test_extract_project_requirements_with_wrapped_json(self, processor):
        """Test requirements extraction with JSON wrapped in text."""
        mock_response = MagicMock()
        mock_response.content = """Based on the transcript, here are the requirements:

        {
            "scope": "Digital transformation project",
            "timeline": "8 months",
            "budget": null,
            "technical_needs": ["API integration"],
            "key_deliverables": ["Modern platform"]
        }

        End of analysis."""

        processor.llm.invoke = MagicMock(return_value=mock_response)
        customer_info = CustomerInfo(
            company_name="Test Corp", industry="Tech", contact_person="John Doe"
        )

        result = processor.extract_project_requirements(
            "test transcript", customer_info
        )

        assert result.scope == "Digital transformation project"
        assert result.timeline == "8 months"
        assert result.budget is None
        assert result.technical_needs == ["API integration"]
        assert result.key_deliverables == ["Modern platform"]

    def test_extract_project_requirements_budget_null_cleanup(self, processor):
        """Test that null budget is cleaned up properly."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "scope": "Test project",
                "timeline": "3 months",
                "budget": "null",
                "technical_needs": ["Need 1"],
                "key_deliverables": ["Deliverable 1"],
            }
        )
        processor.llm.invoke = MagicMock(return_value=mock_response)

        customer_info = CustomerInfo(
            company_name="Test Corp", industry="Tech", contact_person="John Doe"
        )
        result = processor.extract_project_requirements(
            "test transcript", customer_info
        )

        assert result.budget is None

    def test_extract_project_requirements_list_validation(self, processor):
        """Test that non-list values for lists are converted properly."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "scope": "Test project",
                "timeline": "3 months",
                "budget": "$100K",
                "technical_needs": "Single need",  # Not a list
                "key_deliverables": None,  # Not a list
            }
        )
        processor.llm.invoke = MagicMock(return_value=mock_response)

        customer_info = CustomerInfo(
            company_name="Test Corp", industry="Tech", contact_person="John Doe"
        )
        result = processor.extract_project_requirements(
            "test transcript", customer_info
        )

        assert result.technical_needs == []
        assert result.key_deliverables == []

    def test_extract_project_requirements_invalid_json(self, processor):
        """Test handling of invalid JSON response for requirements."""
        mock_response = MagicMock()
        mock_response.content = "Invalid JSON response"
        processor.llm.invoke = MagicMock(return_value=mock_response)

        customer_info = CustomerInfo(
            company_name="Test Corp", industry="Tech", contact_person="John Doe"
        )

        with pytest.raises(ValueError, match="Failed to parse project requirements"):
            processor.extract_project_requirements("test transcript", customer_info)

    def test_extract_customer_info_debug_output(self, processor, capsys):
        """Test that debug information is printed on errors."""
        mock_response = MagicMock()
        mock_response.content = (
            "Very long invalid JSON response that should be truncated in debug output"
            * 10
        )
        processor.llm.invoke = MagicMock(return_value=mock_response)

        with pytest.raises(ValueError):
            processor.extract_customer_info("test transcript")

        captured = capsys.readouterr()
        assert "DEBUG: AI Response was:" in captured.out
        # Should be truncated to 200 characters
        assert (
            len(captured.out.split("DEBUG: AI Response was:")[1].split("...")[0]) <= 210
        )

    def test_extract_requirements_debug_output(self, processor, capsys):
        """Test that debug information is printed on errors for requirements."""
        mock_response = MagicMock()
        mock_response.content = "Another very long invalid response" * 20
        processor.llm.invoke = MagicMock(return_value=mock_response)

        customer_info = CustomerInfo(
            company_name="Test Corp", industry="Tech", contact_person="John Doe"
        )

        with pytest.raises(ValueError):
            processor.extract_project_requirements("test transcript", customer_info)

        captured = capsys.readouterr()
        assert "DEBUG: AI Response was:" in captured.out
