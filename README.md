# Proposal Generator

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![UV](https://img.shields.io/badge/uv-compatible-green.svg)](https://github.com/astral-sh/uv)

**Turn your discovery call transcripts into professional business proposals in seconds.**

Proposal Generator uses AI to automatically analyze discovery call transcriptions and generate comprehensive, well-structured business proposals. Simply provide a transcript, and get back a professional proposal with ROI analysis, implementation phases, timeline, and investment details.

## What You Get

Every generated proposal includes:

- **Executive Summary** with compelling title and customer needs analysis
- **ROI Analysis** with projected returns and business impact
- **Detailed Scope** (in-scope, out-of-scope, assumptions, dependencies)
- **Implementation Phases** with activities and duration
- **Timeline & Investment** breakdown (CAPEX/OPEX)
- **Professional formatting** in Markdown and JSON

---

## Quick Start (3 Steps)

### 1. Download & Setup

```bash
# Clone the repository
git clone https://github.com/griv32/proposal-generator.git
cd proposal-generator

# Set your OpenAI API key
export OPENAI_API_KEY='your-openai-api-key'
```

### 2. Prepare Your Transcript

Create a text file with your discovery call transcript:

```bash
# Create your transcript file
echo "Sales Rep: What challenges are you facing?
Customer: We need to modernize our legacy systems.
Budget is around $200,000 and timeline is 6 months.
We need better security and 99% uptime." > my_transcript.txt
```

### 3. Generate Your Proposal

**Option A: Using UV (Recommended - Fastest)**
```bash
# Install dependencies and run - UV handles everything automatically
uv run proposal-generator --input my_transcript.txt --output ./proposals
```

**Option B: Direct Runner (After dependency setup)**
```bash
# First install dependencies
uv sync
# Then run directly
uv run python run_proposal_generator.py --input my_transcript.txt --output ./proposals
```

**Option C: Traditional pip Installation**
```bash
# Install in development mode, then run
pip install -e .
proposal-generator --input my_transcript.txt --output ./proposals
```

**Done!** Your proposal is ready in the `./proposals` folder.

---

## Try the Built-in Examples

We've included ready-to-run examples so you can see the tool in action immediately:

### Super Quick Start (Interactive)
```bash
# Interactive setup with guided prompts
uv run python run_example.py
# OR
python run_example.py
```
This script will help you set up your API key and choose which example to run.

### Manual Setup
**First-time setup:** You need an OpenAI API key. Get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

**Quick start:**
```bash
# Set your API key and run an example
export OPENAI_API_KEY='your-key-here'
uv run python example_file_usage.py
# OR
python example_file_usage.py
```

**Or create a .env file (recommended):**
```bash
echo "OPENAI_API_KEY=your-key-here" > .env
uv run python example_file_usage.py
# OR
python example_file_usage.py
```

### Example 1: File-based (Recommended for real use)
```bash
# Uses the included sample discovery call transcript
uv run python example_file_usage.py
# OR
python example_file_usage.py
```

This example reads from `sample_data/discovery_call_transcript.txt` (a realistic 9-minute call with RetailMax Solutions) and generates a complete proposal. **The examples include helpful error messages and setup instructions if your API key isn't configured.**

### Example 2: Text-based (Good for testing)
```bash
# Has the transcript embedded in the code
uv run python example_usage.py
# OR
python example_usage.py
```

This example shows how to generate proposals programmatically with embedded transcription text.

---

## Command Line Options

```bash
# Basic usage
proposal-generator --input transcript.txt

# Custom output location and filename
proposal-generator --input transcript.txt --output ./my-proposals --filename client_proposal

# Use different AI model (cheaper/faster)
proposal-generator --input transcript.txt --model gpt-3.5-turbo

# See all options
proposal-generator --help
```

## Python API Usage

```python
from proposal_generator import ProposalWorkflow

# Initialize
workflow = ProposalWorkflow()

# From file
result = workflow.process_transcription_to_proposal(
    transcription_file_path="transcript.txt",
    output_folder="./proposals"
)

# From text string
result = workflow.generate_from_text(
    transcription_text="Your call transcript here...",
    output_folder="./proposals"
)

if result["success"]:
    print(f"Proposal generated: {result['output_files']['markdown']}")
    print(f"Customer: {result['extracted_info']['customer_info']['company_name']}")
else:
    print(f"Error: {result['error']}")
```

---

## What Makes a Good Transcript?

For best results, include:

- **Customer Details**: Company name, industry, contact person
- **Business Pain Points**: Current challenges and problems
- **Requirements**: Technical needs, compliance requirements
- **Project Scope**: What they want to achieve
- **Constraints**: Budget range, timeline, dependencies
- **Success Criteria**: How they define project success
- **Stakeholders**: Decision makers and team members

**Example transcript structure:**
```
Sales Rep: What's your biggest challenge?
Customer (CTO, TechCorp): We have legacy systems causing downtime...

Sales Rep: What's your budget and timeline?
Customer: Around $500K budget, need completion by Q2 2025...

Sales Rep: What would success look like?
Customer: 99.9% uptime and SOC 2 compliance...
```

---

## Configuration

### Required: OpenAI API Key

**Option 1: Environment Variable**
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

**Option 2: .env File**
```bash
# Create .env file in project root
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### Optional Settings
```bash
export OPENAI_MODEL='gpt-4'          # Default: gpt-4
export LOG_LEVEL='INFO'              # Default: INFO
```

---

## Requirements

- **Python 3.9+** (required for modern LangChain)
- **OpenAI API Key** with available credits
- **Internet connection** for API calls

---

## Output Files

The tool generates two files:

1. **`proposal.md`** - Human-readable proposal in Markdown format
2. **`proposal.json`** - Structured data for integration with other tools

Both files contain the complete proposal with all sections and can be easily shared or further processed.

---

## Troubleshooting

**"Error: Input file does not exist"**
- Make sure your transcript file path is correct
- Try using the sample: `sample_data/discovery_call_transcript.txt`

**"Error: OpenAI API key is required"**
- Set your API key: `export OPENAI_API_KEY='your-key'`
- Or create a `.env` file with your key

**Pydantic or LangChain warnings**
- These are normal and don't affect functionality
- The latest version uses modern LangChain patterns

---

## Documentation

- **[Complete Documentation](docs/)** - API reference, developer guide, and examples
- **[API Reference](docs/API.md)** - Detailed documentation for all classes and methods
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Architecture, extension patterns, and contribution guidelines
- **[Security Guidelines](SECURITY.md)** - API key protection and security best practices

## Support & Contributing

- **Report Issues**: [GitHub Issues](https://github.com/griv32/proposal-generator/issues)
- **Get Help**: [GitHub Discussions](https://github.com/griv32/proposal-generator/discussions)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **License**: GPL v3

---

## Disclaimer

The transcription files and text used in examples contain entirely fictional content generated for demonstration purposes only. All company names, person names, business scenarios, and details are completely fictitious and do not represent, reference, or relate to any real individuals, companies, or business situations. Any resemblance to actual persons, living or dead, or actual companies is purely coincidental.

---

**Ready to transform your discovery calls into winning proposals?**

[Get started in 3 steps](#quick-start-3-steps) or [try the examples](#try-the-built-in-examples) right now!