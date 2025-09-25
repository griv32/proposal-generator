"""Test cases for OutputFormatter functionality."""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, mock_open

from proposal_generator.output_formatter import OutputFormatter
from proposal_generator.models import (
    CustomerInfo,
    ProjectRequirements,
    ImplementationPhase,
    ProposalData,
)


class TestOutputFormatter:
    """Test OutputFormatter functionality."""

    @pytest.fixture
    def formatter(self):
        """Create an OutputFormatter instance for testing."""
        return OutputFormatter()

    @pytest.fixture
    def sample_proposal(self, sample_proposal_data):
        """Use the fixture from conftest.py."""
        return sample_proposal_data

    def test_init(self, formatter):
        """Test OutputFormatter initialization."""
        assert formatter.markdown_template is not None
        assert formatter.json_template is not None
        assert "Business Proposal" in formatter.markdown_template
        assert "{{ company_name }}" in formatter.markdown_template

    def test_format_markdown_default_company(self, formatter, sample_proposal):
        """Test Markdown formatting with default company name."""
        result = formatter.format_markdown(sample_proposal)

        assert "# Business Proposal for Test Corp" in result
        assert "## Executive Summary" in result
        assert sample_proposal.executive_summary in result
        assert "## What Success Looks Like" in result
        assert sample_proposal.what_success_looks_like in result
        assert "## Implementation Plan" in result
        assert "**Total Project Duration:** 12 weeks" in result
        assert "Phase 1: Discovery & Planning" in result
        assert "Phase 2: Implementation" in result
        assert "## Investment Summary" in result
        assert sample_proposal.investment_summary in result
        assert "## ROI Analysis" in result
        assert sample_proposal.roi_analysis in result
        assert "## Next Steps" in result
        assert "Review proposal" in result

    def test_format_markdown_custom_company(self, formatter, sample_proposal):
        """Test Markdown formatting with custom company name."""
        custom_name = "Custom Company Inc"
        result = formatter.format_markdown(sample_proposal, custom_name)

        assert f"# Business Proposal for {custom_name}" in result
        assert "Contact: John Doe" in result

    def test_format_markdown_with_optional_contact_info(self, formatter):
        """Test Markdown formatting with optional contact information."""
        customer_info = CustomerInfo(
            company_name="Test Corp",
            industry="Tech",
            contact_person="Jane Smith",
            email="jane@test.com",
            phone="+1-555-0123",
        )
        requirements = ProjectRequirements(scope="Test project", timeline="3 months")
        phases = [
            ImplementationPhase(
                name="Test Phase",
                activities=["Activity 1"],
                duration_weeks=2,
                deliverables=["Deliverable 1"],
            )
        ]
        proposal = ProposalData(
            customer_info=customer_info,
            requirements=requirements,
            executive_summary="Test summary",
            what_success_looks_like="Success vision",
            implementation_phases=phases,
            investment_summary="Investment details",
            roi_analysis="ROI details",
            next_steps=["Next step"],
        )

        result = formatter.format_markdown(proposal)
        assert "- Email: jane@test.com" in result
        assert "- Phone: +1-555-0123" in result

    def test_format_json(self, formatter, sample_proposal):
        """Test JSON formatting."""
        result = formatter.format_json(sample_proposal)

        # Verify it's valid JSON
        parsed = json.loads(result)

        # Check structure
        assert "customer_info" in parsed
        assert "requirements" in parsed
        assert "executive_summary" in parsed
        assert "what_success_looks_like" in parsed
        assert "implementation_phases" in parsed
        assert "investment_summary" in parsed
        assert "roi_analysis" in parsed
        assert "next_steps" in parsed
        assert "total_duration_weeks" in parsed

        # Check content
        assert parsed["customer_info"]["company_name"] == "Test Corp"
        assert parsed["customer_info"]["industry"] == "Technology"
        assert parsed["customer_info"]["contact_person"] == "John Doe"
        assert parsed["requirements"]["scope"].startswith("Modernize")
        assert len(parsed["implementation_phases"]) == 2
        assert (
            parsed["implementation_phases"][0]["name"]
            == "Phase 1: Discovery & Planning"
        )
        assert parsed["implementation_phases"][0]["duration_weeks"] == 4
        assert parsed["implementation_phases"][1]["duration_weeks"] == 8
        assert parsed["total_duration_weeks"] == 12
        assert len(parsed["next_steps"]) == 3

    def test_save_outputs_default_filename(self, formatter, sample_proposal):
        """Test saving outputs with default filename generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = formatter.save_outputs(sample_proposal, temp_dir)

            # Check return value
            assert "markdown" in result
            assert "json" in result

            # Check files were created
            markdown_path = result["markdown"]
            json_path = result["json"]

            assert os.path.exists(markdown_path)
            assert os.path.exists(json_path)
            assert "proposal_test_corp" in os.path.basename(markdown_path)
            assert markdown_path.endswith(".md")
            assert json_path.endswith(".json")

            # Check file contents
            with open(markdown_path, "r", encoding="utf-8") as f:
                markdown_content = f.read()
            assert "# Business Proposal for Test Corp" in markdown_content

            with open(json_path, "r", encoding="utf-8") as f:
                json_content = json.load(f)
            assert json_content["customer_info"]["company_name"] == "Test Corp"

    def test_save_outputs_custom_filename(self, formatter, sample_proposal):
        """Test saving outputs with custom filename."""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_filename = "my_custom_proposal"
            result = formatter.save_outputs(sample_proposal, temp_dir, custom_filename)

            markdown_path = result["markdown"]
            json_path = result["json"]

            assert os.path.exists(markdown_path)
            assert os.path.exists(json_path)
            assert custom_filename in os.path.basename(markdown_path)
            assert custom_filename in os.path.basename(json_path)

    def test_save_outputs_creates_directory(self, formatter, sample_proposal):
        """Test that save_outputs creates output directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = os.path.join(temp_dir, "nested", "output")
            result = formatter.save_outputs(sample_proposal, nested_dir)

            assert os.path.exists(nested_dir)
            assert os.path.exists(result["markdown"])
            assert os.path.exists(result["json"])

    def test_filename_cleaning(self, formatter):
        """Test filename cleaning for special characters."""
        customer_info = CustomerInfo(
            company_name="Company & Associates, Inc.!",
            industry="Business",
            contact_person="John Doe",
        )
        requirements = ProjectRequirements(scope="Test", timeline="1 month")
        phases = []
        proposal = ProposalData(
            customer_info=customer_info,
            requirements=requirements,
            executive_summary="Test",
            what_success_looks_like="Test",
            implementation_phases=phases,
            investment_summary="Test",
            roi_analysis="Test",
            next_steps=[],
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            result = formatter.save_outputs(proposal, temp_dir)
            filename = os.path.basename(result["markdown"])

            # Should clean special characters
            assert "proposal_company" in filename.lower()
            assert "associates_inc" in filename.lower()
            assert "&" not in filename
            assert "!" not in filename
            assert "," not in filename

    def test_get_markdown_template(self, formatter):
        """Test markdown template retrieval."""
        template = formatter._get_markdown_template()

        assert isinstance(template, str)
        assert "# Business Proposal for {{ company_name }}" in template
        assert "{{ proposal.executive_summary }}" in template
        assert "{{ proposal.what_success_looks_like }}" in template
        assert "{% for phase in proposal.implementation_phases %}" in template
        assert "{{ proposal.investment_summary }}" in template
        assert "{{ proposal.roi_analysis }}" in template
        assert "{% for step in proposal.next_steps %}" in template

    def test_get_json_template(self, formatter):
        """Test JSON template retrieval."""
        template = formatter._get_json_template()
        assert template == "{}"

    def test_format_markdown_empty_phases(self, formatter):
        """Test Markdown formatting with empty implementation phases."""
        customer_info = CustomerInfo(
            company_name="Test Corp", industry="Tech", contact_person="John Doe"
        )
        requirements = ProjectRequirements(scope="Test", timeline="1 month")
        proposal = ProposalData(
            customer_info=customer_info,
            requirements=requirements,
            executive_summary="Test summary",
            what_success_looks_like="Success vision",
            implementation_phases=[],
            investment_summary="Investment details",
            roi_analysis="ROI details",
            next_steps=["Step 1", "Step 2"],
        )

        result = formatter.format_markdown(proposal)
        assert "**Total Project Duration:** 0 weeks" in result
        assert "1. Step 1" in result
        assert "2. Step 2" in result

    def test_format_json_with_none_values(self, formatter):
        """Test JSON formatting with None values in customer info."""
        customer_info = CustomerInfo(
            company_name="Test Corp",
            industry="Tech",
            contact_person="John Doe",
            email=None,
            phone=None,
        )
        requirements = ProjectRequirements(
            scope="Test",
            timeline="1 month",
            budget=None,
            technical_needs=[],
            key_deliverables=[],
        )
        proposal = ProposalData(
            customer_info=customer_info,
            requirements=requirements,
            executive_summary="Test",
            what_success_looks_like="Test",
            implementation_phases=[],
            investment_summary="Test",
            roi_analysis="Test",
            next_steps=[],
        )

        result = formatter.format_json(proposal)
        parsed = json.loads(result)

        assert parsed["customer_info"]["email"] is None
        assert parsed["customer_info"]["phone"] is None
        assert parsed["requirements"]["budget"] is None
        assert parsed["requirements"]["technical_needs"] == []
        assert parsed["requirements"]["key_deliverables"] == []
