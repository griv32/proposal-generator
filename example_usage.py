#!/usr/bin/env python3

import os

from src.proposal_generator import ProposalWorkflow


# Example transcript text
def get_sample_transcript():
    """Sample transcript for demonstration."""
    return """
        Hello everyone, thank you for joining our discovery call.

        Today I'm speaking with Sarah Johnson from TechCorp, a fintech company based in San Francisco. Sarah is the Head of Product Development and she's looking to modernize their customer onboarding system.

        Sarah mentioned that they're experiencing significant bottlenecks in their current manual process. New customers are taking 7-10 days to get fully onboarded, and this is creating friction in their user experience.

        The scope they're looking for includes:
        - Automated document verification system
        - Digital identity verification
        - Integration with their existing CRM system
        - Mobile-first user interface
        - Real-time status tracking for customers

        They have a timeline of 3-4 months for this project and are looking to launch by Q2 next year. The budget range they mentioned is between $150,000 to $200,000.

        Their technical team uses React for frontend and Node.js for backend. They need the solution to integrate with Salesforce and their existing authentication system.

        Key deliverables they're expecting:
        - Reduced onboarding time from 7-10 days to 24-48 hours
        - 90% automation of document processing
        - Mobile app with full functionality
        - Real-time dashboard for customer service team
        - Comprehensive testing and documentation

        Sarah emphasized that success for them means dramatically improving customer satisfaction scores and reducing the load on their customer service team.

        Next steps: We'll prepare a detailed proposal and schedule a follow-up meeting early next week.
        """


def main():
    """Run the text-based example."""
    print("AI Proposal Generator - Text Example")
    print("=" * 50)

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key before running this example.")
        return

    try:
        # Initialize workflow
        workflow = ProposalWorkflow()

        # Process transcript text
        result = workflow.process_transcript_text(
            transcript_text=get_sample_transcript(),
            output_folder="./outputs",
            filename="techcorp_example",
        )

        if result["success"]:
            print("\nSuccess! Example proposal generated.")
            print("Files created:")
            print(f"  - Markdown: {result['file_paths']['markdown']}")
            print(f"  - JSON: {result['file_paths']['json']}")

            # Show summary
            customer = result["customer_info"]
            print("\nGenerated proposal for:")
            print(f"  - Company: {customer.company_name}")
            print(f"  - Industry: {customer.industry}")
            print(f"  - Contact: {customer.contact_person}")
            print(f"  - Project Duration: {result['total_duration_weeks']} weeks")

        else:
            print(f"Error: {result['error']}")

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        print("Please check your API key and try again.")


if __name__ == "__main__":
    main()
