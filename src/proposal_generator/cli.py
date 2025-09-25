#!/usr/bin/env python3

import argparse
import os
import sys

from dotenv import load_dotenv

from .workflow import ProposalWorkflow


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="AI-powered Proposal Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--input", "-i", required=True, type=str, help="Path to transcript file"
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="./outputs",
        help="Output folder path (default: ./outputs)",
    )

    parser.add_argument(
        "--filename",
        "-f",
        type=str,
        help="Custom filename prefix (default: generated from company name)",
    )

    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="gpt-4",
        help="AI model to use (default: gpt-4)",
    )

    parser.add_argument(
        "--version", action="store_true", help="Show version information"
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    return parser


def main() -> None:
    """Main CLI entry point."""
    # Load environment variables from .env file
    load_dotenv()

    parser = create_parser()
    args = parser.parse_args()

    # Handle version
    if args.version:
        print("AI Proposal Generator v0.1.0")
        sys.exit(0)

    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)

    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key before running.")
        sys.exit(1)

    try:
        # Initialize workflow
        workflow = ProposalWorkflow(model_name=args.model)

        print("Starting proposal generation...")
        print(f"Input file: {args.input}")
        print(f"Output folder: {args.output}")

        # Process transcript
        result = workflow.process_transcript_file(
            file_path=args.input, output_folder=args.output, filename=args.filename
        )

        if result["success"]:
            print("\nSuccess! Proposal generated successfully.")
            print("Files created:")
            print(f"  - Markdown: {result['file_paths']['markdown']}")
            print(f"  - JSON: {result['file_paths']['json']}")

            # Show summary
            if args.debug:
                customer = result["customer_info"]
                print("\nSummary:")
                print(f"  - Company: {customer.company_name}")
                print(f"  - Industry: {customer.industry}")
                print(f"  - Contact: {customer.contact_person}")
                print(f"  - Total Duration: {result['total_duration_weeks']} weeks")

        else:
            print(f"\nError: {result['error']}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        if args.debug:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
