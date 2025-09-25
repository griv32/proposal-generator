#!/usr/bin/env python3

from src.proposal_generator import ProposalWorkflow
import os
import sys
from pathlib import Path


# Example for file-based usage
def check_requirements():
    """Check if all requirements are met."""
    print("Checking requirements...")
    print("=" * 50)

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set.")
        print("   Please set your OpenAI API key before running.")
        return False
    else:
        print("✅ OPENAI_API_KEY is set")

    # Check for sample transcript file
    sample_file = "./sample_data/sample_transcript.txt"
    if not os.path.exists(sample_file):
        print(f"❌ Sample transcript file not found: {sample_file}")
        print("   Creating a sample file for demonstration...")
        create_sample_transcript_file(sample_file)
        print(f"✅ Sample transcript created at: {sample_file}")
    else:
        print(f"✅ Sample transcript file exists: {sample_file}")

    return True


def create_sample_transcript_file(file_path):
    """Create a sample transcript file."""
    sample_content = """Discovery Call Transcript - RetailMax Solutions

Date: November 15, 2024
Participants: Michael Chen (CTO, RetailMax Solutions), Jennifer Kim (Sales Director)

Michael: Thanks for taking the time to meet with us today. I'm Michael Chen, CTO at RetailMax Solutions. We're an e-commerce platform serving mid-market retailers.

Jennifer: Great to meet you, Michael. Can you tell me more about the challenges you're facing?

Michael: We're experiencing major performance issues with our current inventory management system. During peak seasons like Black Friday, our system can't handle the load, and we're losing sales due to overselling and stock discrepancies.

Our current system is built on legacy technology from 2018, and it's becoming a bottleneck. We have about 500 retail partners using our platform, and they manage over 100,000 SKUs collectively.

The main issues we need to solve:
- Real-time inventory synchronization across multiple sales channels
- Automated reorder point calculations
- Predictive analytics for demand forecasting
- Integration with existing ERP systems (SAP and Oracle)
- Mobile dashboard for on-the-go inventory management

We're looking to complete this project within 4-5 months, ideally launching before next year's peak season. Our budget is flexible, but we're looking at a range of $300,000 to $450,000.

Our technical environment is primarily AWS-based, using microservices architecture. We need the solution to integrate seamlessly with our existing APIs and maintain 99.9% uptime.

Key success metrics for us would be:
- Reducing inventory discrepancies by 95%
- Improving order fulfillment speed by 40%
- Enabling real-time visibility across all channels
- Supporting 10x traffic growth during peak periods

Jennifer: That's very comprehensive. What would be the biggest impact if we solve these challenges?

Michael: We estimate it could increase our revenue by 25-30% annually just from reduced stockouts and improved customer satisfaction. Our retail partners are also pressuring us to provide better inventory insights.

The solution needs to be scalable because we're planning to onboard 200 more retail partners next year.

Jennifer: Excellent. We'll prepare a detailed proposal covering all these requirements and schedule a follow-up meeting next week to discuss the implementation approach.

Michael: Perfect. Looking forward to seeing how you can help us transform our inventory management.
"""

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write sample content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(sample_content)


def main():
    """Run the file-based example with comprehensive error handling."""
    print("AI Proposal Generator - File-based Example")
    print("=" * 50)

    try:
        # Check requirements
        if not check_requirements():
            print("\nPlease resolve the requirements above and try again.")
            return

        print("\nStarting proposal generation...")

        # Initialize workflow
        workflow = ProposalWorkflow()

        # Process transcript file
        transcript_file = "./sample_data/sample_transcript.txt"
        result = workflow.process_transcript_file(
            file_path=transcript_file,
            output_folder="./outputs",
            filename="retailmax_proposal",
        )

        if result["success"]:
            print("\n" + "=" * 50)
            print("SUCCESS! Proposal generated successfully!")
            print("=" * 50)

            # Show file locations
            print(f"\n📁 Files created:")
            print(f"   • Markdown: {result['file_paths']['markdown']}")
            print(f"   • JSON: {result['file_paths']['json']}")

            # Show detailed summary
            customer = result["customer_info"]
            requirements = result["requirements"]

            print(f"\n📊 Proposal Summary:")
            print(f"   • Company: {customer.company_name}")
            print(f"   • Industry: {customer.industry}")
            print(f"   • Contact: {customer.contact_person}")
            if customer.email:
                print(f"   • Email: {customer.email}")

            print(f"\n🔧 Project Details:")
            print(f"   • Duration: {result['total_duration_weeks']} weeks")
            print(f"   • Phases: {len(result['proposal_data'].implementation_phases)}")
            if requirements.budget:
                print(f"   • Budget: {requirements.budget}")

            # Show phase breakdown
            print(f"\n📋 Implementation Phases:")
            for i, phase in enumerate(result["proposal_data"].implementation_phases, 1):
                print(f"   {i}. {phase.name} ({phase.duration_weeks} weeks)")
                for activity in phase.activities[:2]:  # Show first 2 activities
                    print(f"      • {activity}")
                if len(phase.activities) > 2:
                    print(
                        f"      • ... and {len(phase.activities) - 2} more activities"
                    )

            print(f"\n✅ Next Steps:")
            for i, step in enumerate(result["proposal_data"].next_steps, 1):
                print(f"   {i}. {step}")

        else:
            print(f"\n❌ Error: {result['error']}")
            return

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        return
    except Exception as e:
        print(f"\n❌ Unexpected error occurred:")
        print(f"   Error: {str(e)}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   • Ensure OPENAI_API_KEY is set correctly")
        print(f"   • Check your internet connection")
        print(f"   • Verify you have sufficient OpenAI API credits")
        print(f"   • Try running the example again")


def show_usage_guide():
    """Show usage guide and tips."""
    print("\n" + "=" * 50)
    print("USAGE GUIDE")
    print("=" * 50)

    print("\nFile-based Usage:")
    print("  python example_file_usage.py")

    print("\nText-based Usage:")
    print("  python example_usage.py")

    print("\nCLI Usage:")
    print(
        "  python -m src.proposal_generator.cli --input transcript.txt --output ./outputs"
    )

    print("\nCustom Usage:")
    print(
        "  python -m src.proposal_generator.cli --input transcript.txt --filename custom_name --model gpt-3.5-turbo"
    )


if __name__ == "__main__":
    main()
    show_usage_guide()
