import json
import os
from pathlib import Path
from typing import Any, Dict

from jinja2 import Template

from .models import ProposalData


class OutputFormatter:
    """Formats proposal data into various output formats using Jinja2 templates."""

    def __init__(self):
        """Initialize the formatter with default templates."""
        self.markdown_template = self._get_markdown_template()
        self.json_template = self._get_json_template()

    def format_markdown(
        self, proposal_data: ProposalData, company_name: str = None
    ) -> str:
        """Format proposal data as Markdown."""
        if company_name is None:
            company_name = proposal_data.customer_info.company_name

        template = Template(self.markdown_template)
        return template.render(
            proposal=proposal_data,
            company_name=company_name,
            total_weeks=proposal_data.get_total_duration_weeks(),
        )

    def format_json(self, proposal_data: ProposalData) -> str:
        """Format proposal data as JSON."""
        # Convert to dict for JSON serialization
        proposal_dict = {
            "customer_info": {
                "company_name": proposal_data.customer_info.company_name,
                "industry": proposal_data.customer_info.industry,
                "contact_person": proposal_data.customer_info.contact_person,
                "email": proposal_data.customer_info.email,
                "phone": proposal_data.customer_info.phone,
            },
            "requirements": {
                "scope": proposal_data.requirements.scope,
                "timeline": proposal_data.requirements.timeline,
                "budget": proposal_data.requirements.budget,
                "technical_needs": proposal_data.requirements.technical_needs,
                "key_deliverables": proposal_data.requirements.key_deliverables,
            },
            "executive_summary": proposal_data.executive_summary,
            "what_success_looks_like": proposal_data.what_success_looks_like,
            "implementation_phases": [
                {
                    "name": phase.name,
                    "activities": phase.activities,
                    "duration_weeks": phase.duration_weeks,
                    "deliverables": phase.deliverables,
                }
                for phase in proposal_data.implementation_phases
            ],
            "investment_summary": proposal_data.investment_summary,
            "roi_analysis": proposal_data.roi_analysis,
            "next_steps": proposal_data.next_steps,
            "total_duration_weeks": proposal_data.get_total_duration_weeks(),
        }

        return json.dumps(proposal_dict, indent=2, ensure_ascii=False)

    def save_outputs(
        self,
        proposal_data: ProposalData,
        output_folder: str = "./outputs",
        filename: str = None,
    ) -> Dict[str, str]:
        """Save both Markdown and JSON outputs to files."""
        # Create output folder if it doesn't exist
        Path(output_folder).mkdir(parents=True, exist_ok=True)

        # Generate filename if not provided
        if filename is None:
            company_name = proposal_data.customer_info.company_name
            # Clean company name for filename
            clean_name = "".join(
                c for c in company_name if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            clean_name = clean_name.replace(" ", "_").lower()
            filename = f"proposal_{clean_name}"

        # Generate outputs
        markdown_content = self.format_markdown(proposal_data)
        json_content = self.format_json(proposal_data)

        # Save files
        markdown_path = os.path.join(output_folder, f"{filename}.md")
        json_path = os.path.join(output_folder, f"{filename}.json")

        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        with open(json_path, "w", encoding="utf-8") as f:
            f.write(json_content)

        return {
            "markdown": os.path.abspath(markdown_path),
            "json": os.path.abspath(json_path),
        }

    def _get_markdown_template(self) -> str:
        """Get the default Markdown template."""
        return """# Business Proposal for {{ company_name }}

## Executive Summary

{{ proposal.executive_summary }}

## What Success Looks Like

{{ proposal.what_success_looks_like }}

## Implementation Plan

**Total Project Duration:** {{ total_weeks }} weeks

{% for phase in proposal.implementation_phases %}
### {{ phase.name }}
**Duration:** {{ phase.duration_weeks }} weeks

**Activities:**
{% for activity in phase.activities %}
- {{ activity }}
{% endfor %}

**Deliverables:**
{% for deliverable in phase.deliverables %}
- {{ deliverable }}
{% endfor %}

{% endfor %}

## Investment Summary

{{ proposal.investment_summary }}

## ROI Analysis

{{ proposal.roi_analysis }}

## Next Steps

{% for step in proposal.next_steps %}
{{ loop.index }}. {{ step }}
{% endfor %}

---

**Contact Information:**
- Company: {{ proposal.customer_info.company_name }}
- Contact: {{ proposal.customer_info.contact_person }}
{% if proposal.customer_info.email %}- Email: {{ proposal.customer_info.email }}{% endif %}
{% if proposal.customer_info.phone %}- Phone: {{ proposal.customer_info.phone }}{% endif %}

*Generated by AI Proposal Generator*
"""

    def _get_json_template(self) -> str:
        """Get the default JSON template (not used since we generate dict directly)."""
        return "{}"
