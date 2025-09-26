"""Test cases for ProposalGenerator functionality."""

import json
from unittest.mock import MagicMock, patch

import pytest

from proposal_generator.models import (
    CustomerInfo,
    ImplementationPhase,
    ProjectRequirements,
    ProposalData,
)
from proposal_generator.proposal_generator import ProposalGenerator


class TestProposalGenerator:
    """Test ProposalGenerator functionality."""

    @pytest.fixture
    def generator(self):
        """Create a ProposalGenerator instance for testing."""
        with patch("proposal_generator.proposal_generator.ChatOpenAI"):
            return ProposalGenerator("gpt-4")

    @pytest.fixture
    def sample_customer(self):
        """Sample customer info for testing."""
        return CustomerInfo(
            company_name="Test Corp",
            industry="Technology",
            contact_person="John Doe",
            email="john@testcorp.com",
        )

    @pytest.fixture
    def sample_requirements(self):
        """Sample project requirements for testing."""
        return ProjectRequirements(
            scope="Modernize legacy systems",
            timeline="6 months",
            budget="$200K-$500K",
            technical_needs=["POS upgrade", "Cloud migration"],
            key_deliverables=["99% uptime", "Mobile support"],
        )

    def test_init(self):
        """Test ProposalGenerator initialization."""
        with patch("proposal_generator.proposal_generator.ChatOpenAI") as mock_llm:
            generator = ProposalGenerator("gpt-3.5-turbo")

            mock_llm.assert_called_once_with(model="gpt-3.5-turbo")
            assert generator.llm.temperature == 0.2

    def test_init_default_model(self):
        """Test ProposalGenerator initialization with default model."""
        with patch("proposal_generator.proposal_generator.ChatOpenAI") as mock_llm:
            ProposalGenerator()

            mock_llm.assert_called_once_with(model="gpt-4")

    def test_generate_proposal_complete_flow(
        self, generator, sample_customer, sample_requirements
    ):
        """Test complete proposal generation flow."""
        # Mock all LLM responses
        mock_responses = [
            MagicMock(content="Executive summary content"),
            MagicMock(content="Success vision content"),
            MagicMock(
                content=json.dumps(
                    {
                        "phases": [
                            {
                                "name": "Phase 1: Planning",
                                "activities": ["Activity 1", "Activity 2"],
                                "duration_weeks": 2,
                                "deliverables": ["Plan document"],
                            }
                        ]
                    }
                )
            ),
            MagicMock(content="Investment summary content"),
            MagicMock(content="ROI analysis content"),
        ]

        generator.llm.invoke = MagicMock(side_effect=mock_responses)

        result = generator.generate_proposal(sample_customer, sample_requirements)

        assert isinstance(result, ProposalData)
        assert result.customer_info == sample_customer
        assert result.requirements == sample_requirements
        assert result.executive_summary == "Executive summary content"
        assert result.what_success_looks_like == "Success vision content"
        assert len(result.implementation_phases) == 1
        assert result.implementation_phases[0].name == "Phase 1: Planning"
        assert result.investment_summary == "Investment summary content"
        assert result.roi_analysis == "ROI analysis content"
        assert len(result.next_steps) == 4  # Default next steps

        # Verify all methods were called
        assert generator.llm.invoke.call_count == 5

    def test_generate_executive_summary(
        self, generator, sample_customer, sample_requirements
    ):
        """Test executive summary generation."""
        mock_response = MagicMock()
        mock_response.content = "  Executive summary with leading/trailing spaces  "
        generator.llm.invoke = MagicMock(return_value=mock_response)

        result = generator._generate_executive_summary(
            sample_customer, sample_requirements
        )

        assert result == "Executive summary with leading/trailing spaces"

        # Check that the prompt contains expected elements
        call_args = generator.llm.invoke.call_args[0][0]
        assert sample_customer.company_name in call_args
        assert sample_customer.industry in call_args
        assert sample_requirements.scope in call_args

    def test_generate_success_vision(
        self, generator, sample_customer, sample_requirements
    ):
        """Test success vision generation."""
        mock_response = MagicMock()
        mock_response.content = "Success vision content"
        generator.llm.invoke = MagicMock(return_value=mock_response)

        result = generator._generate_success_vision(
            sample_customer, sample_requirements
        )

        assert result == "Success vision content"

        # Check that the prompt contains expected elements
        call_args = generator.llm.invoke.call_args[0][0]
        assert sample_customer.company_name in call_args
        assert sample_requirements.scope in call_args
        assert "99% uptime, Mobile support" in call_args  # Joined deliverables

    def test_generate_success_vision_no_deliverables(self, generator, sample_customer):
        """Test success vision generation with no deliverables."""
        requirements = ProjectRequirements(
            scope="Test project", timeline="3 months", key_deliverables=[]
        )

        mock_response = MagicMock()
        mock_response.content = "Success vision content"
        generator.llm.invoke = MagicMock(return_value=mock_response)

        generator._generate_success_vision(sample_customer, requirements)

        call_args = generator.llm.invoke.call_args[0][0]
        assert "Not specified" in call_args

    def test_generate_implementation_phases_success(
        self, generator, sample_customer, sample_requirements
    ):
        """Test successful implementation phases generation."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "phases": [
                    {
                        "name": "Phase 1: Discovery",
                        "activities": ["Analysis", "Planning"],
                        "duration_weeks": 3,
                        "deliverables": ["Requirements doc", "Project plan"],
                    },
                    {
                        "name": "Phase 2: Implementation",
                        "activities": ["Development", "Testing"],
                        "duration_weeks": 8,
                        "deliverables": ["Working system"],
                    },
                ]
            }
        )
        generator.llm.invoke = MagicMock(return_value=mock_response)

        result = generator._generate_implementation_phases(
            sample_customer, sample_requirements
        )

        assert len(result) == 2
        assert isinstance(result[0], ImplementationPhase)
        assert result[0].name == "Phase 1: Discovery"
        assert result[0].activities == ["Analysis", "Planning"]
        assert result[0].duration_weeks == 3
        assert result[0].deliverables == ["Requirements doc", "Project plan"]

        assert result[1].name == "Phase 2: Implementation"
        assert result[1].duration_weeks == 8

        # Check that the prompt contains expected elements
        call_args = generator.llm.invoke.call_args[0][0]
        assert sample_customer.company_name in call_args
        assert sample_requirements.scope in call_args
        assert sample_requirements.timeline in call_args
        assert "POS upgrade, Cloud migration" in call_args  # Joined technical needs

    def test_generate_implementation_phases_no_technical_needs(
        self, generator, sample_customer
    ):
        """Test implementation phases generation with no technical needs."""
        requirements = ProjectRequirements(
            scope="Test project", timeline="3 months", technical_needs=[]
        )

        mock_response = MagicMock()
        mock_response.content = json.dumps({"phases": []})
        generator.llm.invoke = MagicMock(return_value=mock_response)

        generator._generate_implementation_phases(sample_customer, requirements)

        call_args = generator.llm.invoke.call_args[0][0]
        assert "None specified" in call_args

    def test_generate_implementation_phases_fallback(
        self, generator, sample_customer, sample_requirements
    ):
        """Test implementation phases fallback when JSON parsing fails."""
        mock_response = MagicMock()
        mock_response.content = "Invalid JSON response"
        generator.llm.invoke = MagicMock(return_value=mock_response)

        result = generator._generate_implementation_phases(
            sample_customer, sample_requirements
        )

        # Should return default fallback phases
        assert len(result) == 3
        assert result[0].name == "Phase 1: Discovery & Planning"
        assert result[0].duration_weeks == 2
        assert result[1].name == "Phase 2: Development & Implementation"
        assert result[1].duration_weeks == 6
        assert result[2].name == "Phase 3: Deployment & Training"
        assert result[2].duration_weeks == 2

    def test_generate_implementation_phases_missing_deliverables(
        self, generator, sample_customer, sample_requirements
    ):
        """Test implementation phases with missing deliverables field."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "phases": [
                    {
                        "name": "Phase 1: Test",
                        "activities": ["Activity 1"],
                        "duration_weeks": 2,
                        # Missing deliverables field
                    }
                ]
            }
        )
        generator.llm.invoke = MagicMock(return_value=mock_response)

        result = generator._generate_implementation_phases(
            sample_customer, sample_requirements
        )

        assert len(result) == 1
        assert result[0].deliverables == []  # Should default to empty list

    def test_generate_investment_summary(
        self, generator, sample_customer, sample_requirements
    ):
        """Test investment summary generation."""
        mock_response = MagicMock()
        mock_response.content = "Investment summary content"
        generator.llm.invoke = MagicMock(return_value=mock_response)

        result = generator._generate_investment_summary(
            sample_customer, sample_requirements
        )

        assert result == "Investment summary content"

        # Check that the prompt contains expected elements
        call_args = generator.llm.invoke.call_args[0][0]
        assert sample_customer.company_name in call_args
        assert sample_requirements.scope in call_args
        assert sample_requirements.budget in call_args

    def test_generate_investment_summary_no_budget(self, generator, sample_customer):
        """Test investment summary generation with no budget."""
        requirements = ProjectRequirements(
            scope="Test project", timeline="3 months", budget=None
        )

        mock_response = MagicMock()
        mock_response.content = "Investment summary content"
        generator.llm.invoke = MagicMock(return_value=mock_response)

        generator._generate_investment_summary(sample_customer, requirements)

        call_args = generator.llm.invoke.call_args[0][0]
        assert "Not specified" in call_args

    def test_generate_roi_analysis(
        self, generator, sample_customer, sample_requirements
    ):
        """Test ROI analysis generation."""
        mock_response = MagicMock()
        mock_response.content = "ROI analysis content"
        generator.llm.invoke = MagicMock(return_value=mock_response)

        result = generator._generate_roi_analysis(sample_customer, sample_requirements)

        assert result == "ROI analysis content"

        # Check that the prompt contains expected elements
        call_args = generator.llm.invoke.call_args[0][0]
        assert sample_customer.company_name in call_args
        assert sample_customer.industry in call_args
        assert sample_requirements.scope in call_args

    def test_generate_next_steps(self, generator, sample_customer, sample_requirements):
        """Test next steps generation."""
        result = generator._generate_next_steps(sample_customer, sample_requirements)

        assert isinstance(result, list)
        assert len(result) == 4
        assert "Review and approve this proposal" in result
        assert "Schedule a project kickoff meeting" in result
        assert "Finalize contract terms and timeline" in result
        assert "Begin Phase 1: Discovery & Planning" in result

    def test_implementation_phases_duration_conversion(
        self, generator, sample_customer, sample_requirements
    ):
        """Test that duration_weeks is properly converted to int."""
        mock_response = MagicMock()
        mock_response.content = json.dumps(
            {
                "phases": [
                    {
                        "name": "Phase 1: Test",
                        "activities": ["Activity 1"],
                        "duration_weeks": "4",  # String instead of int
                        "deliverables": ["Deliverable 1"],
                    }
                ]
            }
        )
        generator.llm.invoke = MagicMock(return_value=mock_response)

        result = generator._generate_implementation_phases(
            sample_customer, sample_requirements
        )

        assert len(result) == 1
        assert result[0].duration_weeks == 4
        assert isinstance(result[0].duration_weeks, int)
