"""Test cases for Pydantic data models."""

from typing import List

import pytest
from pydantic import ValidationError

from proposal_generator.models import (
    CustomerInfo,
    ImplementationPhase,
    ProjectRequirements,
    ProposalData,
)


class TestCustomerInfo:
    """Test CustomerInfo model validation and functionality."""

    def test_valid_customer_info_creation(self):
        """Test creating CustomerInfo with valid data."""
        customer = CustomerInfo(
            company_name="Test Company",
            industry="Technology",
            contact_person="John Smith",
        )
        assert customer.company_name == "Test Company"
        assert customer.industry == "Technology"
        assert customer.contact_person == "John Smith"
        assert customer.email is None
        assert customer.phone is None

    def test_customer_info_with_optional_fields(self):
        """Test CustomerInfo with optional email and phone."""
        customer = CustomerInfo(
            company_name="Acme Corp",
            industry="Manufacturing",
            contact_person="Jane Doe",
            email="jane@acme.com",
            phone="+1-555-0123",
        )
        assert customer.email == "jane@acme.com"
        assert customer.phone == "+1-555-0123"

    def test_customer_info_missing_required_fields(self):
        """Test CustomerInfo validation with missing required fields."""
        with pytest.raises(ValidationError):
            CustomerInfo(
                company_name="Test Corp"
            )  # Missing industry and contact_person

        with pytest.raises(ValidationError):
            CustomerInfo(
                industry="Technology"
            )  # Missing company_name and contact_person

    def test_customer_info_empty_string_validation(self):
        """Test CustomerInfo validation with empty strings."""
        with pytest.raises(ValidationError):
            CustomerInfo(
                company_name="", industry="Technology", contact_person="John Doe"
            )


class TestProjectRequirements:
    """Test ProjectRequirements model validation and functionality."""

    def test_valid_project_requirements_creation(self):
        """Test creating ProjectRequirements with valid data."""
        requirements = ProjectRequirements(
            scope="Modernize legacy systems",
            timeline="6 months",
            budget="$200K-$500K",
            technical_needs=["POS upgrade", "Cloud migration"],
            key_deliverables=["System uptime", "Mobile support"],
        )
        assert requirements.scope == "Modernize legacy systems"
        assert requirements.timeline == "6 months"
        assert requirements.budget == "$200K-$500K"
        assert len(requirements.technical_needs) == 2
        assert len(requirements.key_deliverables) == 2

    def test_project_requirements_with_optional_fields(self):
        """Test ProjectRequirements with optional/default fields."""
        requirements = ProjectRequirements(
            scope="Simple automation project", timeline="3 months"
        )
        assert requirements.budget is None
        assert requirements.technical_needs == []
        assert requirements.key_deliverables == []

    def test_project_requirements_list_validation(self):
        """Test ProjectRequirements list field validation."""
        requirements = ProjectRequirements(
            scope="Test project",
            timeline="1 month",
            technical_needs=["Need 1", "Need 2", "Need 3"],
            key_deliverables=["Deliverable A"],
        )
        assert isinstance(requirements.technical_needs, list)
        assert isinstance(requirements.key_deliverables, list)
        assert len(requirements.technical_needs) == 3


class TestImplementationPhase:
    """Test ImplementationPhase model validation and functionality."""

    def test_valid_implementation_phase_creation(self):
        """Test creating ImplementationPhase with valid data."""
        phase = ImplementationPhase(
            name="Phase 1: Discovery",
            activities=["Analysis", "Planning", "Design"],
            duration_weeks=4,
            deliverables=["Requirements doc", "Project plan"],
        )
        assert phase.name == "Phase 1: Discovery"
        assert len(phase.activities) == 3
        assert phase.duration_weeks == 4
        assert len(phase.deliverables) == 2

    def test_implementation_phase_duration_validation(self):
        """Test ImplementationPhase duration field validation."""
        # Valid duration
        phase = ImplementationPhase(
            name="Test Phase",
            activities=["Task 1"],
            duration_weeks=8,
            deliverables=["Output"],
        )
        assert phase.duration_weeks == 8

        # Invalid duration (negative)
        with pytest.raises(ValidationError):
            ImplementationPhase(
                name="Test Phase",
                activities=["Task 1"],
                duration_weeks=-2,
                deliverables=["Output"],
            )

    def test_implementation_phase_empty_lists(self):
        """Test ImplementationPhase with empty lists."""
        phase = ImplementationPhase(
            name="Empty Phase", activities=[], duration_weeks=1, deliverables=[]
        )
        assert phase.activities == []
        assert phase.deliverables == []


class TestProposalData:
    """Test ProposalData model validation and functionality."""

    def test_valid_proposal_data_creation(
        self,
        sample_customer_info: CustomerInfo,
        sample_project_requirements: ProjectRequirements,
        sample_implementation_phases: List[ImplementationPhase],
    ):
        """Test creating ProposalData with valid nested models."""
        proposal = ProposalData(
            customer_info=sample_customer_info,
            requirements=sample_project_requirements,
            executive_summary="Executive summary text",
            what_success_looks_like="Success vision text",
            implementation_phases=sample_implementation_phases,
            investment_summary="Investment details",
            roi_analysis="ROI analysis text",
            next_steps=["Step 1", "Step 2", "Step 3"],
        )

        assert proposal.customer_info.company_name == "Test Corp"
        assert proposal.requirements.scope.startswith("Modernize")
        assert len(proposal.implementation_phases) == 2
        assert len(proposal.next_steps) == 3

    def test_proposal_data_helper_methods(self, sample_proposal_data: ProposalData):
        """Test ProposalData utility methods."""
        # Test total duration calculation
        total_weeks = sample_proposal_data.get_total_duration_weeks()
        assert total_weeks == 12  # 4 + 8 from sample phases

        # Test phase names extraction
        phase_names = sample_proposal_data.get_phase_names()
        assert len(phase_names) == 2
        assert "Phase 1: Discovery & Planning" in phase_names
        assert "Phase 2: Implementation" in phase_names

    def test_proposal_data_with_empty_phases(
        self,
        sample_customer_info: CustomerInfo,
        sample_project_requirements: ProjectRequirements,
    ):
        """Test ProposalData with empty implementation phases."""
        proposal = ProposalData(
            customer_info=sample_customer_info,
            requirements=sample_project_requirements,
            executive_summary="Test summary",
            what_success_looks_like="Test success vision",
            implementation_phases=[],
            investment_summary="Test investment",
            roi_analysis="Test ROI",
            next_steps=["Next step"],
        )

        assert len(proposal.implementation_phases) == 0
        assert proposal.get_total_duration_weeks() == 0
        assert proposal.get_phase_names() == []

    def test_proposal_data_nested_model_validation(
        self, sample_project_requirements: ProjectRequirements
    ):
        """Test ProposalData validation with invalid nested models."""
        # Invalid CustomerInfo should cause ValidationError
        with pytest.raises(ValidationError):
            ProposalData(
                customer_info=CustomerInfo(company_name=""),  # Empty name should fail
                requirements=sample_project_requirements,
                executive_summary="Test",
                what_success_looks_like="Test",
                implementation_phases=[],
                investment_summary="Test",
                roi_analysis="Test",
                next_steps=[],
            )
