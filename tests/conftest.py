"""Test configuration and fixtures."""

import pytest
import os
from unittest.mock import patch, MagicMock
from typing import Dict, Any

from proposal_generator.models import (
    CustomerInfo,
    ProjectRequirements,
    ProposalData,
    ImplementationPhase
)


@pytest.fixture
def sample_customer_info() -> CustomerInfo:
    """Sample customer information for testing."""
    return CustomerInfo(
        company_name="Test Corp",
        industry="Technology",
        contact_person="John Doe"
    )


@pytest.fixture
def sample_project_requirements() -> ProjectRequirements:
    """Sample project requirements for testing."""
    return ProjectRequirements(
        scope="Modernize legacy systems and improve efficiency",
        timeline="6 months project completion",
        budget="$200K-$500K budget range",
        technical_needs=[
            "POS system upgrade",
            "Inventory management automation",
            "Real-time data visibility"
        ],
        key_deliverables=[
            "99.9% system uptime",
            "Mobile payment capabilities",
            "PCI DSS compliance"
        ]
    )


@pytest.fixture
def sample_implementation_phases() -> list:
    """Sample implementation phases for testing."""
    return [
        ImplementationPhase(
            name="Phase 1: Discovery & Planning",
            activities=["Requirements analysis", "System design", "Project planning"],
            duration_weeks=4,
            deliverables=["Requirements document", "System design", "Project plan"]
        ),
        ImplementationPhase(
            name="Phase 2: Implementation",
            activities=["System development", "Testing", "Integration"],
            duration_weeks=8,
            deliverables=["Working system", "Test results"]
        )
    ]


@pytest.fixture
def sample_proposal_data(
    sample_customer_info: CustomerInfo,
    sample_project_requirements: ProjectRequirements,
    sample_implementation_phases: list
) -> ProposalData:
    """Complete sample proposal data for testing."""
    return ProposalData(
        customer_info=sample_customer_info,
        requirements=sample_project_requirements,
        executive_summary="This is a test executive summary for Test Corp modernization project.",
        what_success_looks_like="Success looks like achieving 99.9% uptime and modernized systems.",
        implementation_phases=sample_implementation_phases,
        investment_summary="Investment of $200K-$500K for comprehensive modernization.",
        roi_analysis="Expected ROI within 18 months through efficiency gains.",
        next_steps=["Review proposal", "Schedule kickoff", "Begin discovery"]
    )


@pytest.fixture
def sample_transcript() -> str:
    """Sample transcript for testing."""
    return """
    Discovery call with Test Corp, a technology company.

    Sales Rep: What challenges are you facing?
    Customer (John Doe, CTO): We need to modernize our legacy systems.
    Budget is around $300,000 and timeline is 6 months.
    We need better security and 99% uptime.

    Our main pain points are manual processes and outdated POS systems.
    """


@pytest.fixture
def mock_openai_customer_response() -> Dict[str, Any]:
    """Mock OpenAI API response for customer extraction."""
    return {
        "company_name": "Test Corp",
        "industry": "Technology",
        "contact_person": "John Doe",
        "email": "john@testcorp.com",
        "phone": None
    }


@pytest.fixture
def mock_openai_requirements_response() -> Dict[str, Any]:
    """Mock OpenAI API response for requirements extraction."""
    return {
        "scope": "Modernize legacy systems and improve efficiency",
        "timeline": "6 months",
        "budget": "$300,000",
        "technical_needs": ["POS system upgrade", "Security improvements"],
        "key_deliverables": ["99% uptime", "Modern systems"]
    }


@pytest.fixture
def api_key_env():
    """Temporarily set API key environment variable."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"}):
        yield


@pytest.fixture
def mock_llm_response():
    """Mock LangChain LLM response."""
    mock_response = MagicMock()
    mock_response.content = '{"test": "response"}'
    return mock_response


# Skip tests that require OpenAI API if key is not available
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "requires_openai: mark test as requiring OpenAI API key"
    )


def pytest_collection_modifyitems(config, items):
    """Skip OpenAI-dependent tests if no API key available."""
    if not os.getenv("OPENAI_API_KEY"):
        skip_openai = pytest.mark.skip(reason="OpenAI API key not available")
        for item in items:
            if "requires_openai" in item.keywords:
                item.add_marker(skip_openai)