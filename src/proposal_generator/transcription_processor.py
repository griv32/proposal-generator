from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from .models import CustomerInfo, ProjectRequirements


class TranscriptionProcessor:
    """Processes transcript text and extracts structured data using AI."""

    def __init__(self, model_name: str = "gpt-4"):
        self.llm = ChatOpenAI(model_name=model_name)
        self.llm.temperature = 0.3

    def extract_customer_info(self, transcript: str) -> CustomerInfo:
        """Extract customer information from transcript."""
        prompt_template = PromptTemplate(
            input_variables=["transcript"],
            template="""
            Analyze the following discovery call transcript and extract customer information.

            Transcript:
            {transcript}

            Extract the following information:
            - Company name
            - Industry sector
            - Primary contact person name
            - Email address (if mentioned)
            - Phone number (if mentioned)

            Return the information in this JSON format:
            {{
                "company_name": "Company Name Here",
                "industry": "Industry Here",
                "contact_person": "Contact Name Here",
                "email": "email@example.com or null",
                "phone": "phone number or null"
            }}

            If any information is not clearly mentioned, use your best judgment based on context.
            """,
        )

        response = self.llm.invoke(prompt_template.format(transcript=transcript))

        try:
            # Parse the JSON response
            import json
            import re

            response_text = response.content.strip()

            # Extract JSON from response if it's wrapped in text
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(0)
            else:
                json_text = response_text

            customer_data = json.loads(json_text)

            # Clean up null strings
            for key in customer_data:
                if customer_data[key] == "null" or customer_data[key] == "":
                    customer_data[key] = None

            return CustomerInfo(**customer_data)
        except Exception as e:
            # Debug info for troubleshooting
            print(f"DEBUG: AI Response was: {response.content[:200]}...")
            raise ValueError(f"Failed to parse customer information: {str(e)}")

    def extract_project_requirements(
        self, transcript: str, customer_info: CustomerInfo
    ) -> ProjectRequirements:
        """Extract project requirements from transcript."""
        prompt_template = PromptTemplate(
            input_variables=["transcript", "company_name"],
            template="""
            Analyze the following discovery call transcript for {company_name} and extract project requirements.

            Transcript:
            {transcript}

            Extract the following information:
            - Project scope and main objectives
            - Timeline expectations or constraints
            - Budget range or budget constraints (if mentioned)
            - Technical requirements and needs
            - Key deliverables expected

            Return the information in this JSON format:
            {{
                "scope": "Detailed project scope and objectives",
                "timeline": "Timeline information",
                "budget": "Budget information or null if not mentioned",
                "technical_needs": ["Technical need 1", "Technical need 2"],
                "key_deliverables": ["Deliverable 1", "Deliverable 2"]
            }}

            Focus on what the client actually needs and mentioned during the call.
            Be specific and actionable in your extraction.
            """,
        )

        response = self.llm.invoke(
            prompt_template.format(
                transcript=transcript, company_name=customer_info.company_name
            )
        )

        try:
            import json
            import re

            response_text = response.content.strip()

            # Extract JSON from response if it's wrapped in text
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(0)
            else:
                json_text = response_text

            requirements_data = json.loads(json_text)

            # Clean up null strings and ensure lists
            if requirements_data.get("budget") == "null":
                requirements_data["budget"] = None
            if not isinstance(requirements_data.get("technical_needs"), list):
                requirements_data["technical_needs"] = []
            if not isinstance(requirements_data.get("key_deliverables"), list):
                requirements_data["key_deliverables"] = []

            return ProjectRequirements(**requirements_data)
        except Exception as e:
            # Debug info for troubleshooting
            print(f"DEBUG: AI Response was: {response.content[:200]}...")
            raise ValueError(f"Failed to parse project requirements: {str(e)}")
