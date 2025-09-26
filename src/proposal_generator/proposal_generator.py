from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from .models import CustomerInfo, ImplementationPhase, ProjectRequirements, ProposalData


class ProposalGenerator:
    """Generates comprehensive business proposals using AI."""

    def __init__(self, model_name: str = "gpt-4"):
        self.llm = ChatOpenAI(model_name=model_name)
        self.llm.temperature = 0.2

    def generate_proposal(
        self, customer_info: CustomerInfo, requirements: ProjectRequirements
    ) -> ProposalData:
        """Generate a complete business proposal."""

        # Generate individual components
        executive_summary = self._generate_executive_summary(
            customer_info, requirements
        )
        what_success_looks_like = self._generate_success_vision(
            customer_info, requirements
        )
        implementation_phases = self._generate_implementation_phases(
            customer_info, requirements
        )
        investment_summary = self._generate_investment_summary(
            customer_info, requirements
        )
        roi_analysis = self._generate_roi_analysis(customer_info, requirements)
        next_steps = self._generate_next_steps(customer_info, requirements)

        return ProposalData(
            customer_info=customer_info,
            requirements=requirements,
            executive_summary=executive_summary,
            what_success_looks_like=what_success_looks_like,
            implementation_phases=implementation_phases,
            investment_summary=investment_summary,
            roi_analysis=roi_analysis,
            next_steps=next_steps,
        )

    def _generate_executive_summary(
        self, customer_info: CustomerInfo, requirements: ProjectRequirements
    ) -> str:
        """Generate executive summary section."""
        prompt_template = PromptTemplate(
            input_variables=["company_name", "industry", "scope"],
            template="""
            Create a compelling executive summary for a business proposal.

            Client: {company_name} in the {industry} industry
            Project Scope: {scope}

            Write a professional executive summary that:
            - Clearly articulates the client's challenges and opportunities
            - Positions our solution as the ideal fit
            - Highlights key benefits and outcomes
            - Maintains a confident but not overselling tone

            Keep it concise but compelling, around 150-200 words.
            """,
        )

        response = self.llm.invoke(
            prompt_template.format(
                company_name=customer_info.company_name,
                industry=customer_info.industry,
                scope=requirements.scope,
            )
        )
        return response.content.strip()

    def _generate_success_vision(
        self, customer_info: CustomerInfo, requirements: ProjectRequirements
    ) -> str:
        """Generate 'What Success Looks Like' section."""
        prompt_template = PromptTemplate(
            input_variables=["company_name", "scope", "deliverables"],
            template="""
            Create a "What Success Looks Like" section for {company_name}.

            Project Scope: {scope}
            Key Deliverables: {deliverables}

            Paint a vivid picture of the successful project outcome:
            - Specific, measurable results the client will see
            - How their business operations will improve
            - The competitive advantages they'll gain
            - Long-term benefits and growth potential

            Make it inspiring but realistic. Use bullet points for clarity.
            """,
        )

        response = self.llm.invoke(
            prompt_template.format(
                company_name=customer_info.company_name,
                scope=requirements.scope,
                deliverables=", ".join(requirements.key_deliverables)
                or "Not specified",
            )
        )
        return response.content.strip()

    def _generate_implementation_phases(
        self, customer_info: CustomerInfo, requirements: ProjectRequirements
    ) -> list[ImplementationPhase]:
        """Generate implementation phases with activities and timelines."""
        prompt_template = PromptTemplate(
            input_variables=["company_name", "scope", "timeline", "technical_needs"],
            template="""
            Create a detailed implementation plan for {company_name}.

            Project Scope: {scope}
            Timeline: {timeline}
            Technical Needs: {technical_needs}

            Create 3-5 logical project phases. For each phase, provide:
            1. Phase name
            2. List of specific activities (3-5 activities per phase)
            3. Duration in weeks (must be a whole number)
            4. Key deliverables for that phase

            Return as JSON in this exact format:
            {{
                "phases": [
                    {{
                        "name": "Phase 1: Discovery & Planning",
                        "activities": ["Activity 1", "Activity 2", "Activity 3"],
                        "duration_weeks": 2,
                        "deliverables": ["Deliverable 1", "Deliverable 2"]
                    }}
                ]
            }}

            Ensure duration_weeks are realistic and add up to a reasonable total timeline.
            """,
        )

        response = self.llm.invoke(
            prompt_template.format(
                company_name=customer_info.company_name,
                scope=requirements.scope,
                timeline=requirements.timeline,
                technical_needs=", ".join(requirements.technical_needs)
                or "None specified",
            )
        )

        try:
            import json

            phases_data = json.loads(response.content.strip())

            phases = []
            for phase_data in phases_data["phases"]:
                phase = ImplementationPhase(
                    name=phase_data["name"],
                    activities=phase_data["activities"],
                    duration_weeks=int(phase_data["duration_weeks"]),
                    deliverables=phase_data.get("deliverables", []),
                )
                phases.append(phase)

            return phases
        except Exception:
            # Fallback to a default structure if parsing fails
            return [
                ImplementationPhase(
                    name="Phase 1: Discovery & Planning",
                    activities=[
                        "Initial consultation",
                        "Requirements analysis",
                        "Project planning",
                    ],
                    duration_weeks=2,
                    deliverables=["Project plan", "Requirements document"],
                ),
                ImplementationPhase(
                    name="Phase 2: Development & Implementation",
                    activities=["Core development", "Integration", "Testing"],
                    duration_weeks=6,
                    deliverables=["Functional system", "Test results"],
                ),
                ImplementationPhase(
                    name="Phase 3: Deployment & Training",
                    activities=[
                        "System deployment",
                        "User training",
                        "Go-live support",
                    ],
                    duration_weeks=2,
                    deliverables=[
                        "Live system",
                        "User documentation",
                        "Training materials",
                    ],
                ),
            ]

    def _generate_investment_summary(
        self, customer_info: CustomerInfo, requirements: ProjectRequirements
    ) -> str:
        """Generate investment and pricing summary."""
        prompt_template = PromptTemplate(
            input_variables=["company_name", "scope", "budget"],
            template="""
            Create an investment summary for {company_name}.

            Project Scope: {scope}
            Budget Context: {budget}

            Create a professional investment summary that:
            - Positions the investment as value-driven
            - Explains what's included in the engagement
            - Addresses typical pricing concerns
            - Suggests next steps for detailed pricing

            Don't include specific numbers unless budget was mentioned.
            Focus on value and ROI potential.
            """,
        )

        response = self.llm.invoke(
            prompt_template.format(
                company_name=customer_info.company_name,
                scope=requirements.scope,
                budget=requirements.budget or "Not specified",
            )
        )
        return response.content.strip()

    def _generate_roi_analysis(
        self, customer_info: CustomerInfo, requirements: ProjectRequirements
    ) -> str:
        """Generate ROI analysis section."""
        prompt_template = PromptTemplate(
            input_variables=["company_name", "industry", "scope"],
            template="""
            Create an ROI analysis for {company_name} in the {industry} industry.

            Project Scope: {scope}

            Analyze potential return on investment by covering:
            - Cost savings opportunities
            - Revenue generation potential
            - Efficiency improvements
            - Competitive advantages
            - Risk mitigation benefits

            Use industry-specific insights where possible.
            Be realistic but compelling about ROI potential.
            """,
        )

        response = self.llm.invoke(
            prompt_template.format(
                company_name=customer_info.company_name,
                industry=customer_info.industry,
                scope=requirements.scope,
            )
        )
        return response.content.strip()

    def _generate_next_steps(
        self, customer_info: CustomerInfo, requirements: ProjectRequirements
    ) -> list[str]:
        """Generate next steps for moving forward."""
        return [
            "Review and approve this proposal",
            "Schedule a project kickoff meeting",
            "Finalize contract terms and timeline",
            "Begin Phase 1: Discovery & Planning",
        ]
