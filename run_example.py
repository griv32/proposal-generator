#!/usr/bin/env python3
"""
Interactive setup and example runner for the Proposal Generator.
This script helps users get started quickly.
"""

import os
import sys
from pathlib import Path

def show_welcome():
    print("🚀 AI Proposal Generator - Interactive Setup")
    print("=" * 50)

    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not found!")
        print("   You need to set your OpenAI API key to use this tool.")
        print("   Get your key from: https://platform.openai.com/api-keys")

        # Interactive setup for API key
        print("\n🔧 Setup Options:")
        print("1. Set API key temporarily (this session only)")
        print("2. Get instructions for permanent setup")
        print("3. Exit and set up manually")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            api_key = input("Enter your OpenAI API key: ").strip()
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                print("✅ API key set for this session!")
            else:
                print("❌ Invalid API key. Exiting.")
                sys.exit(1)
        elif choice == "2":
            show_setup_instructions()
            sys.exit(0)
        else:
            print("Please set up your API key and try again.")
            sys.exit(0)
    else:
        print("✅ OPENAI_API_KEY is configured!")

def show_setup_instructions():
    print("\n📋 Permanent Setup Instructions:")
    print("=" * 50)

    print("\nOption 1: Environment file (.env)")
    print("  1. Create a .env file in your project root")
    print("  2. Add: OPENAI_API_KEY=your_key_here")
    print("  3. Load it: pip install python-dotenv")

    print("\nOption 2: System environment variable")
    print("  macOS/Linux:")
    print("    export OPENAI_API_KEY=your_key_here")
    print("    # Add to ~/.bashrc or ~/.zshrc for permanence")

    print("  Windows:")
    print("    set OPENAI_API_KEY=your_key_here")
    print("    # Or use System Properties > Environment Variables")

def show_example_menu():
    print("\n🎯 Choose an example to run:")
    print("=" * 30)
    print("1. Text-based example (embedded transcript)")
    print("2. File-based example (reads from sample file)")
    print("3. Show usage guide only")
    print("4. Exit")

    while True:
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            print("\n🔄 Running text-based example...")
            try:
                import example_usage
                example_usage.main()
            except ImportError:
                print("❌ Could not import example_usage module")
            except Exception as e:
                print(f"❌ Error running text example: {str(e)}")
            break

        elif choice == "2":
            print("\n🔄 Running file-based example...")
            try:
                import example_file_usage
                example_file_usage.main()
            except ImportError:
                print("❌ Could not import example_file_usage module")
            except Exception as e:
                print(f"❌ Error running file example: {str(e)}")
            break

        elif choice == "3":
            show_usage_guide()
            break

        elif choice == "4":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter 1-4.")

def show_usage_guide():
    print("\n📖 Usage Guide")
    print("=" * 50)

    print("\n🎯 Ways to use the Proposal Generator:")

    print("\n1. Python Examples:")
    print("   python example_usage.py          # Text-based example")
    print("   python example_file_usage.py     # File-based example")
    print("   python run_example.py            # This interactive script")

    print("\n2. Command Line Interface:")
    print("   python -m src.proposal_generator.cli --input transcript.txt")
    print("   python -m src.proposal_generator.cli --input transcript.txt --output ./my_outputs")
    print("   python -m src.proposal_generator.cli --input transcript.txt --filename custom")

    print("\n3. Direct Python Usage:")
    print("""
   from src.proposal_generator import ProposalWorkflow

   workflow = ProposalWorkflow()
   result = workflow.process_transcript_file('transcript.txt')
   """)

    print("\n⚙️  Available CLI Options:")
    print("   --input, -i     : Path to transcript file (required)")
    print("   --output, -o    : Output folder (default: ./outputs)")
    print("   --filename, -f  : Custom filename prefix")
    print("   --model, -m     : AI model to use (default: gpt-4)")
    print("   --debug         : Enable debug output")
    print("   --version       : Show version information")

def main():
    """Main interactive setup function."""
    try:
        show_welcome()
        show_example_menu()

    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        print("Run this script again when you're ready!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    main()