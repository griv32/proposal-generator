import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from .transcription_processor import TranscriptionProcessor
from .proposal_generator import ProposalGenerator
from .output_formatter import OutputFormatter
from .models import ProposalData


class ProposalWorkflow:
    """Main workflow orchestration class for the proposal generation process."""

    def __init__(self, model_name: str = "gpt-4"):
        """Initialize the workflow with AI model."""
        # Load environment variables from .env file
        load_dotenv()
        self._check_api_key()
        self.model_name = model_name
        self.transcription_processor = TranscriptionProcessor(model_name)
        self.proposal_generator = ProposalGenerator(model_name)
        self.output_formatter = OutputFormatter()

    def _check_api_key(self):
        """Check if OpenAI API key is available."""
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please set your OpenAI API key before using this tool."
            )

    def process_transcript_text(
        self,
        transcript_text: str,
        output_folder: str = "./outputs",
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process transcript text and generate proposal.

        Args:
            transcript_text: The transcript text to process
            output_folder: Folder to save outputs (default: ./outputs)
            filename: Custom filename (default: generated from company name)

        Returns:
            Dict with processing results and file paths
        """
        try:
            print("Processing transcript...")
            print("=" * 50)

            # Extract customer info and requirements
            print("Step 1: Extracting customer information...")
            customer_info = self.transcription_processor.extract_customer_info(transcript_text)
            print(f"Extracted info for: {customer_info.company_name}")

            print("Step 2: Extracting project requirements...")
            requirements = self.transcription_processor.extract_project_requirements(
                transcript_text, customer_info
            )
            print(f"Requirements extracted: {requirements.scope[:100]}...")

            # Generate proposal
            print("Step 3: Generating comprehensive proposal...")
            proposal_data = self.proposal_generator.generate_proposal(customer_info, requirements)
            print(f"Generated proposal with {len(proposal_data.implementation_phases)} phases")

            # Format and save outputs
            print("Step 4: Formatting and saving outputs...")
            file_paths = self.output_formatter.save_outputs(
                proposal_data, output_folder, filename
            )

            print("Step 5: Process complete!")
            print(f"Files saved:")
            print(f"  - Markdown: {file_paths['markdown']}")
            print(f"  - JSON: {file_paths['json']}")

            return {
                "success": True,
                "customer_info": customer_info,
                "requirements": requirements,
                "proposal_data": proposal_data,
                "file_paths": file_paths,
                "total_duration_weeks": proposal_data.get_total_duration_weeks()
            }

        except Exception as e:
            error_msg = f"Error during processing: {str(e)}"
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }

    def process_transcript_file(
        self,
        file_path: str,
        output_folder: str = "./outputs",
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process transcript from file and generate proposal.

        Args:
            file_path: Path to transcript file
            output_folder: Folder to save outputs (default: ./outputs)
            filename: Custom filename (default: generated from company name)

        Returns:
            Dict with processing results and file paths
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Transcript file not found: {file_path}")

            # Read transcript file
            print(f"Reading transcript from: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                transcript_text = f.read().strip()

            if not transcript_text:
                raise ValueError("Transcript file is empty")

            # Process the transcript text
            return self.process_transcript_text(transcript_text, output_folder, filename)

        except Exception as e:
            error_msg = f"Error reading transcript file: {str(e)}"
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }