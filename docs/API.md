# API Reference

Complete API reference for the AI-powered Proposal Generator, a tool that converts discovery call transcripts into professional business proposals.

## Overview

- **Primary Classes**: ProposalWorkflow, TranscriptionProcessor, ProposalGenerator, OutputFormatter
- **Data Models**: CustomerInfo, ProjectRequirements, ProposalData, ImplementationPhase
- **Main Features**: AI-powered text processing, structured data extraction, template-based output
- **Dependencies**: LangChain, OpenAI GPT-4, Pydantic models, Jinja2 templates
- **Pipeline**: TranscriptionProcessor → ProposalGenerator → OutputFormatter
- **Output Formats**: Markdown proposals, JSON data structures
- **CLI Interface**: Command-line tool with file processing capabilities

---

## ProposalWorkflow

### Description

**Class Path**: `src.proposal_generator.workflow.ProposalWorkflow`

Main orchestration class that coordinates the entire proposal generation pipeline.

#### Constructor

```python
ProposalWorkflow(
    model_name: str = "gpt-4"
)
```

**Parameters**:
- `model_name` (str): AI model name. Defaults to "gpt-4"

**Raises**:
- `ValueError`: When OPENAI_API_KEY environment variable is not set

##### process_transcript_text()

```python
process_transcript_text(
    transcript_text: str,
    output_folder: str = "./outputs",
    filename: Optional[str] = None
) -> Dict[str, Any]
```

Process transcript text and generate complete business proposal.

**Parameters**:
- `transcript_text` (str): Raw transcript content to process
- `output_folder` (str): Directory for saving output files. Defaults to "./outputs"
- `filename` (Optional[str]): Custom filename prefix. Generated from company name if None

**Returns**:
Dict containing:
```python
{
    "success": bool,
    "customer_info": CustomerInfo,
    "requirements": ProjectRequirements,
    "proposal_data": ProposalData,
    "file_paths": {"markdown": str, "json": str},
    "total_duration_weeks": int
    # OR if error occurs:
    "error": str
}
```

**Example Usage**:
```python
from proposal_generator import ProposalWorkflow

workflow = ProposalWorkflow()
result = workflow.process_transcript_text(
    transcript_text="Discovery call transcript...",
    output_folder="./proposals",
    filename="client_proposal"
)

if result["success"]:
    print(f"Generated proposal for: {result['customer_info'].company_name}")
    print(f"Files saved to: {result['file_paths']}")
```

##### process_transcript_file()

```python
process_transcript_file(
    file_path: str,
    output_folder: str = "./outputs",
    filename: Optional[str] = None
) -> Dict[str, Any]
```

Process transcript from file and generate proposal.

**Parameters**:
- `file_path` (str): Path to transcript file
- `output_folder` (str): Directory for output files
- `filename` (Optional[str]): Custom filename prefix

**Returns**: Same format as process_transcript_text()

**Raises**:
- `FileNotFoundError`: When transcript file doesn't exist
- `ValueError`: When transcript file is empty

**Example Usage**:
```python
result = workflow.process_transcript_file(
    file_path="./transcripts/discovery_call.txt",
    output_folder="./client_proposals",
    filename="abc_corp_proposal"
)
```

---

### TranscriptionProcessor

**Class Path**: `src.proposal_generator.transcription_processor.TranscriptionProcessor`

Processes transcript text and extracts structured customer and project data using AI.

#### Constructor

```python
TranscriptionProcessor(model_name: str = "gpt-4")
```

**Parameters**:
- `model_name` (str): AI model for processing

#### Methods

##### extract_customer_info()

```python
extract_customer_info(transcript: str) -> CustomerInfo
```

Extract customer information from discovery call transcript.

**Parameters**:
- `transcript` (str): Raw transcript content

**Returns**: CustomerInfo object with extracted data

**Example Usage**:
```python
processor = TranscriptionProcessor()
customer_info = processor.extract_customer_info(transcript)

print(f"Company: {customer_info.company_name}")
print(f"Industry: {customer_info.industry}")
print(f"Contact: {customer_info.contact_person}")
```

##### extract_project_requirements() *(Private)*

```python
extract_project_requirements(transcript: str, customer_info: CustomerInfo) -> ProjectRequirements
```

Extract project requirements and specifications from transcript.

**Parameters**:
- `transcript` (str): Raw transcript content
- `customer_info` (CustomerInfo): Previously extracted customer data

**Returns**: ProjectRequirements object containing:
```python
ProjectRequirements(
    scope="Project objectives and scope",
    timeline="Expected timeline",
    budget="Budget constraints",
    technical_needs=["requirement1", "requirement2"],
    key_deliverables=["deliverable1", "deliverable2"]
)
```

---

### ProposalGenerator

**Class Path**: `src.proposal_generator.proposal_generator.ProposalGenerator`

Generates comprehensive business proposals using AI-powered content creation.

#### Constructor

```python
ProposalGenerator(model_name: str = "gpt-4")
```

**Parameters**:
- `model_name` (str): AI model for proposal generation

#### Methods

##### generate_proposal()

```python
generate_proposal(customer_info: CustomerInfo, requirements: ProjectRequirements) -> ProposalData
```

Generate complete business proposal with all sections.

**Parameters**:
- `customer_info` (CustomerInfo): Customer data from extraction phase
- `requirements` (ProjectRequirements): Project requirements from extraction

**Returns**: Complete ProposalData object

**Example Usage**:
```python
generator = ProposalGenerator()
proposal = generator.generate_proposal(customer_info, requirements)

print(f"Executive Summary: {proposal.executive_summary}")
print(f"Success Vision: {proposal.what_success_looks_like}")
print(f"Implementation Phases: {len(proposal.implementation_phases)}")
```

##### generate_proposal() *(Private Methods)*

The following private methods are called internally during proposal generation:

- `_generate_executive_summary()`: Creates compelling executive summary
- `_generate_success_vision()`: Defines what success looks like
- `_generate_implementation_phases()`: Creates detailed project phases
- `_generate_investment_summary()`: Generates pricing and investment summary
- `_generate_roi_analysis()`: Creates ROI analysis and projections
- `_generate_next_steps()`: Defines immediate next steps

---

### OutputFormatter

**Class Path**: `src.proposal_generator.output_formatter.OutputFormatter`

Formats proposal data into various output formats using Jinja2 templates.

#### Constructor

```python
OutputFormatter()
```

Initializes formatter with built-in Markdown and JSON templates.

#### Methods

##### format_markdown()

```python
format_markdown(proposal_data: ProposalData, company_name: str = None) -> str
```

Format proposal data as professional Markdown document.

**Parameters**:
- `proposal_data` (ProposalData): Complete proposal data
- `company_name` (str): Override company name. Uses data from proposal if None

**Returns**: Formatted Markdown string

##### format_json()

```python
format_json(proposal_data: ProposalData) -> str
```

Format proposal data as structured JSON.

**Parameters**:
- `proposal_data` (ProposalData): Complete proposal data

**Returns**: JSON string representation

##### save_outputs()

```python
save_outputs(proposal_data: ProposalData, output_folder: str = "./outputs", filename: str = None) -> Dict[str, str]
```

Save formatted proposal to both Markdown and JSON files.

**Parameters**:
- `proposal_data` (ProposalData): Complete proposal data
- `output_folder` (str): Directory for saving files
- `filename` (str): Custom filename prefix

**Returns**: Dictionary with file paths:
```python
{
    "markdown": "/path/to/proposal.md",
    "json": "/path/to/proposal.json"
}
```

---

## Data Models

**Module Path**: `src.proposal_generator.models`

Pydantic-based data models for type safety and validation.

### CustomerInfo

Represents customer information extracted from discovery calls.

```python
class CustomerInfo(BaseModel):
    company_name: str          # Name of client company
    industry: str              # Industry sector
    contact_person: str        # Primary contact name
    email: Optional[str]       # Contact email
    phone: Optional[str]       # Contact phone
```

### ProjectRequirements

Contains project requirements and specifications.

```python
class ProjectRequirements(BaseModel):
    scope: str                        # Project scope and objectives
    timeline: str                     # Expected timeline
    budget: Optional[str]             # Budget range or constraints
    technical_needs: List[str]        # Technical requirements
    key_deliverables: List[str]       # Main deliverables
```

### ImplementationPhase

Individual phase of project implementation.

```python
class ImplementationPhase(BaseModel):
    name: str                   # Phase name
    activities: List[str]       # Activities in this phase
    duration_weeks: int         # Duration in weeks (must be numeric)
    deliverables: List[str]     # Phase deliverables
```

### ProposalData

Complete proposal data structure containing all generated content.

```python
class ProposalData(BaseModel):
    customer_info: CustomerInfo              # Customer information
    requirements: ProjectRequirements        # Project requirements
    executive_summary: str                   # Executive summary section
    what_success_looks_like: str            # Success vision
    implementation_phases: List[ImplementationPhase]  # Project phases
    investment_summary: str                  # Investment summary
    roi_analysis: str                        # ROI analysis
    next_steps: List[str]                   # Next steps

    # Helper methods:
    def get_total_duration_weeks(self) -> int
    def get_phase_names(self) -> List[str]
```

---

## CLI Interface

**Module Path**: `src.proposal_generator.cli`

### Command Usage

```bash
proposal-generator --input transcript.txt --output ./proposals --filename custom_name --model gpt-3.5-turbo
```

Command-line interface for processing transcript files and generating proposals.

**Arguments**:
- `--input`, `-i`: Path to transcript file (required)
- `--output`, `-o`: Output folder path (default: "./outputs")
- `--filename`, `-f`: Custom filename prefix (default: generated from company)
- `--model`, `-m`: AI model to use (default: "gpt-4")
- `--version`: Show version information
- `--debug`: Enable debug output

**Exit Codes**:
- 0: Success
- 1: Error (file not found, API key missing, processing failure)

---

## Error Handling

### Common Exceptions

- **ValueError**: OPENAI_API_KEY not set, empty transcript file
- **FileNotFoundError**: Transcript file doesn't exist
- **ValidationError**: Invalid data model structure
- **APIError**: OpenAI API communication failures

### Error Handling Pattern

```python
try:
    workflow = ProposalWorkflow()
    result = workflow.process_transcript_text(transcript)

    if not result["success"]:
        print(f"Processing failed: {result['error']}")
        return

    # Handle successful result
    proposal_data = result["proposal_data"]

except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Validation and Input Sanitization

All data models use Pydantic validation:

```python
from pydantic import ValidationError

try:
    customer_info = CustomerInfo(
        company_name="ABC Corp",
        industry="Technology",
        contact_person="John Smith"
    )
except ValidationError as e:
    print(f"Data validation failed: {e}")
```

---

## Usage Examples

### Basic Text Processing

```python
# Import the main workflow
from proposal_generator import ProposalWorkflow

# Initialize workflow
workflow = ProposalWorkflow()

# Process transcript text
transcript = """
    Discovery call with ABC Corp...
    Industry: Technology
    Contact: John Smith...
"""

result = workflow.process_transcript_text(
    transcript_text=transcript,
    output_folder="./outputs",
    filename="abc_corp"
)

if result["success"]:
    print("Success!")
    print(f"Generated proposal for: {result['customer_info'].company_name}")
    print(f"Files: {result['file_paths']}")
else:
    print(f"Error: {result['error']}")
```

### File Processing Example

```python
# Process from file
result = workflow.process_transcript_file(
    file_path="./transcripts/discovery_call.txt",
    output_folder="./client_proposals",
    filename="project_alpha"
)
```

### Using Individual Components

```python
from proposal_generator.transcription_processor import TranscriptionProcessor
from proposal_generator.proposal_generator import ProposalGenerator
from proposal_generator.output_formatter import OutputFormatter

# Step-by-step processing
processor = TranscriptionProcessor("gpt-4")
generator = ProposalGenerator("gpt-4")
formatter = OutputFormatter()

# Extract data
customer_info = processor.extract_customer_info(transcript)
requirements = processor.extract_project_requirements(transcript, customer_info)

# Generate proposal
proposal_data = generator.generate_proposal(customer_info, requirements)

# Format output
markdown_content = formatter.format_markdown(proposal_data)
json_content = formatter.format_json(proposal_data)
```

### Command Line Usage - Advanced Examples

```bash
# Basic usage
proposal-generator --input transcript.txt

# Custom output location and filename
proposal-generator --input call.txt --output ./client_proposals --filename acme_proposal

# Using different AI model
proposal-generator --input transcript.txt --model gpt-3.5-turbo

# Debug mode for troubleshooting
proposal-generator --input transcript.txt --debug

# Check version
proposal-generator --version
```

---

## Configuration

### Environment Variables

Required environment variables:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### Model Configuration

Supported models:
- `gpt-4` (default, recommended)
- `gpt-3.5-turbo` (faster, lower cost)

Temperature settings are optimized per component:
- TranscriptionProcessor: 0.3 (balanced creativity/accuracy)
- ProposalGenerator: 0.2 (more focused/consistent output)