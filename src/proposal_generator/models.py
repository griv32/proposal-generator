from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class CustomerInfo(BaseModel):
    """Customer information extracted from discovery call."""

    company_name: str = Field(..., description="Name of the client company")
    industry: str = Field(..., description="Industry sector of the client")
    contact_person: str = Field(..., description="Primary contact person name")
    email: Optional[str] = Field(None, description="Contact email address")
    phone: Optional[str] = Field(None, description="Contact phone number")

    @field_validator("company_name", "industry", "contact_person")
    @classmethod
    def validate_non_empty_strings(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v


class ProjectRequirements(BaseModel):
    """Project requirements and specifications."""

    scope: str = Field(..., description="Project scope and objectives")
    timeline: str = Field(..., description="Expected project timeline")
    budget: Optional[str] = Field(None, description="Budget range or constraints")
    technical_needs: List[str] = Field(
        default_factory=list, description="Technical requirements"
    )
    key_deliverables: List[str] = Field(
        default_factory=list, description="Main project deliverables"
    )


class ImplementationPhase(BaseModel):
    """Individual phase of project implementation."""

    name: str = Field(..., description="Phase name")
    activities: List[str] = Field(..., description="Activities in this phase")
    duration_weeks: int = Field(..., description="Duration in weeks (must be numeric)")
    deliverables: List[str] = Field(
        default_factory=list, description="Phase deliverables"
    )

    @field_validator("duration_weeks")
    @classmethod
    def validate_positive_duration(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Duration must be positive")
        return v


class ProposalData(BaseModel):
    """Complete proposal data structure."""

    customer_info: CustomerInfo = Field(..., description="Customer information")
    requirements: ProjectRequirements = Field(..., description="Project requirements")
    executive_summary: str = Field(..., description="Executive summary of the proposal")
    what_success_looks_like: str = Field(..., description="Vision of project success")
    implementation_phases: List[ImplementationPhase] = Field(
        ..., description="Project phases"
    )
    investment_summary: str = Field(..., description="Investment and pricing summary")
    roi_analysis: str = Field(..., description="Return on investment analysis")
    next_steps: List[str] = Field(
        default_factory=list, description="Immediate next steps"
    )

    def get_total_duration_weeks(self) -> int:
        """Calculate total project duration in weeks."""
        return sum(phase.duration_weeks for phase in self.implementation_phases)

    def get_phase_names(self) -> List[str]:
        """Get list of all phase names."""
        return [phase.name for phase in self.implementation_phases]
