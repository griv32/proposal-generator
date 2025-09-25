# Sample Data

This directory contains example data files for testing and demonstration.

## Contents

**discovery_call_transcript.txt** - A realistic sample discovery call transcript featuring RetailMax Solutions, a fictional retail company looking to modernize their legacy systems and improve operations. The transcript covers key discussion points including budget, timeline, technical requirements, and success criteria.

## Usage

### 1. File-based Example

Run the included example:

- **File**: `example_file_usage.py` (recommended)
- **Transcript**: RetailMax Solutions discovery call
- **Features**: Complete proposal generation with:
  - Budget considerations ($200K-$500K range)
  - Timeline requirements (6-month delivery)
  - Technical specifications
  - ROI analysis with projected savings
  - Compliance requirements
  - Success metrics and KPIs

## File Structure

### discovery_call_transcript.txt

Contains a sample 9-minute discovery call with:

- **Participants**: Sales Rep and CTO from RetailMax Solutions
- **Company context**: Mid-sized retail company
- **Pain points**: Legacy systems, manual processes, security concerns
- **Requirements**:
  - Modernization of POS systems
  - Inventory management improvements
  - Security compliance (PCI DSS)
  - Performance improvements (99.9% uptime)
  - Staff training requirements

### Using the File

```python
# Load the sample transcript
from proposal_generator import ProposalWorkflow

workflow = ProposalWorkflow()
result = workflow.process_transcription_to_proposal(
    transcription_file_path="sample_data/discovery_call_transcript.txt",
    output_folder="./proposals"
)
```

### Direct Usage

```bash
# CLI usage with sample data
proposal-generator --input sample_data/discovery_call_transcript.txt --output ./proposals
```

## Expected Outputs

When you run examples with this data:

1. **Customer Analysis**
   - Company: RetailMax Solutions
   - Industry: Retail
   - Key stakeholder: John Mitchell (CTO)
   - Budget range: $200K-$500K
   - Timeline: 6 months

2. **Generated Proposal**
   - Executive summary with compelling ROI
   - Technical requirements breakdown
   - Implementation phases (3-4 stages)
   - Investment breakdown (CAPEX/OPEX)
   - Success metrics and KPIs

3. **Output Files**
   - `proposal.md` - Formatted proposal document
   - `proposal.json` - Structured data format
   - Complete with professional formatting

## Notes

- The transcript contains entirely fictional content generated for demonstration purposes
- All company names, person names, and business scenarios are completely fictitious
- Any resemblance to actual persons or companies is purely coincidental
- Designed to showcase the full capabilities of the proposal generation system