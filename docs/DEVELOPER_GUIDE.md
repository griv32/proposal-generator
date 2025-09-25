# Developer Guide

Welcome to the AI-powered Proposal Generator development guide. This document provides comprehensive information for developers who want to understand, extend, or contribute to the project.

## Overview

- **Project Type**: AI-powered business document generator
- **Architecture**: Three-stage pipeline with modular components
- **Technologies**: Python, LangChain, OpenAI GPT-4, Pydantic, Jinja2
- **Input Processing**: Natural language transcript analysis
- **Output Generation**: Structured business proposals (Markdown + JSON)
- **CLI Support**: Command-line interface for batch processing

---

## Architecture

The system follows a **three-stage pipeline architecture**:

```
Transcript → TranscriptionProcessor → ProposalGenerator → OutputFormatter → Files
             ↓                      ↓                   ↓               ↓
           Extract Data          Generate Content     Format & Save   MD + JSON
```

### Component Overview

**Stage 1: Data Extraction**
- **TranscriptionProcessor** analyzes raw transcript text
- **Extracts** structured customer info and project requirements
- **Uses** AI prompts for intelligent parsing
- **Outputs** validated Pydantic models

**Stage 2: Content Generation**
- **ProposalGenerator** creates comprehensive business content
- **Generates** executive summary, success vision, phases, ROI analysis
- **Uses** AI for compelling, professional writing
- **Outputs** complete ProposalData structure

**Stage 3: Output Formatting**
- **OutputFormatter** transforms data into professional documents
- **Creates** Markdown proposals and JSON data exports
- **Uses** Jinja2 templates for consistent formatting
- **Saves** files with organized naming conventions

---

## Project Structure

```
proposal_generator/
├── docs/                    # Documentation files
├── src/                     # Source code
│   └── proposal_generator/
│       ├── __init__.py      # Package initialization
│       ├── models.py        # Pydantic data models
│       ├── workflow.py      # Main orchestration class
│       ├── transcription_processor.py  # Data extraction
│       ├── proposal_generator.py       # Content generation
│       ├── output_formatter.py         # Output formatting
│       └── cli.py                     # Command-line interface
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_models.py       # Model tests
│   └── test_cli.py          # CLI tests
├── outputs/                 # Generated proposals (created at runtime)
├── templates/               # Jinja2 templates (embedded in code)
├── pyproject.toml          # Project configuration
├── README.md               # Project overview
└── requirements.txt        # Python dependencies
```

### Key Directories

**Source Code (src/proposal_generator/)**
All core functionality is organized into focused modules:

- `workflow.py` - Main API entry point and orchestration
- `models.py` - Type-safe data structures with validation
- Processing pipeline components (`transcription_processor.py`, `proposal_generator.py`)
- `output_formatter.py` - Template-based document generation
- `cli.py` - Command-line interface implementation

**Tests (tests/)**
Comprehensive test coverage using pytest:

```python
# tests/conftest.py
import pytest
from proposal_generator import ProposalWorkflow

@pytest.fixture
def sample_transcript():
    return """
    Discovery call with TechCorp...
    Industry: Software Development
    Contact: Sarah Johnson...
    """

@pytest.fixture
def workflow():
    return ProposalWorkflow("gpt-3.5-turbo")  # Use cheaper model for tests

@pytest.fixture
def mock_openai_response():
    # Mock API responses for testing
    pass
```

### Module Dependencies

Understanding the dependency flow is crucial for development:

```python
# Core dependency chain:
cli.py → workflow.py → [transcription_processor.py, proposal_generator.py] → output_formatter.py
                    ↓
               models.py (used by all components)
```

---

## Development Setup

### Prerequisites

- **Python 3.8+** (recommended: 3.11 for optimal performance)
- **OpenAI API Key** with GPT-4 access
- **Git** for version control

### Installation Steps

```bash
# 1. Clone the repository
git clone <repository-url>
cd proposal_generator

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install in development mode
pip install -e .

# 5. Set up environment variables
export OPENAI_API_KEY="your-openai-api-key"

# 6. Verify installation
proposal-generator --version
```

### Development Environment

**Recommended IDE Setup:**
- **VS Code** with Python extension
- **PyCharm Professional** for advanced debugging
- **Type checking**: mypy integration
- **Linting**: flake8, black formatter
- **Testing**: pytest with coverage reporting

**Environment Configuration:**
```bash
# .env file (create in project root)
OPENAI_API_KEY=your-actual-api-key
PYTHONPATH=/path/to/proposal_generator/src
```

**Git Hooks Setup:**
```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Hooks will run:
# - Code formatting (black)
# - Import sorting (isort)
# - Linting (flake8)
# - Type checking (mypy)
```

---

## Extension Patterns

### Adding New Content Sections

The system is designed for easy extension. Here's how to add new proposal sections:

**1. Extend Data Models**

```python
# In models.py
class ProposalData(BaseModel):
    # ... existing fields ...
    risk_analysis: str = Field(..., description="Project risk assessment")
    timeline_details: List[str] = Field(default_factory=list, description="Detailed timeline breakdown")
```

**2. Extend ProposalGenerator**

```python
# In proposal_generator.py - add private method
def _generate_risk_analysis(self, customer_info: CustomerInfo, requirements: ProjectRequirements) -> str:
    """Generate risk analysis section."""
    prompt_template = PromptTemplate(
        input_variables=["industry", "scope"],
        template="""
        Create a comprehensive risk analysis for this project:

        Industry: {industry}
        Project Scope: {scope}

        Analyze potential risks and mitigation strategies...
        """
    )

    response = self.llm.invoke(prompt_template.format(
        industry=customer_info.industry,
        scope=requirements.scope
    ))

    return response.content.strip()

# Update generate_proposal method
def generate_proposal(self, customer_info: CustomerInfo, requirements: ProjectRequirements) -> ProposalData:
    # ... existing code ...
    risk_analysis = self._generate_risk_analysis(customer_info, requirements)

    return ProposalData(
        # ... existing fields ...
        risk_analysis=risk_analysis
    )
```

**3. Update Templates**

```python
# In output_formatter.py - extend markdown template
def _get_markdown_template(self):
    return '''
    # Proposal for {{ company_name }}

    ... existing sections ...

    ## Risk Analysis

    {{ proposal.risk_analysis }}

    ... rest of template ...
    '''
```

### Custom Data Extractors

Create specialized extractors for different transcript types:

```python
# custom_extractors.py - New module
class TechnicalCallProcessor(TranscriptionProcessor):
    """Specialized processor for technical discovery calls."""

    def extract_technical_requirements(self, transcript: str) -> Dict[str, Any]:
        """Extract technical specifications and architecture requirements."""

        prompt_template = PromptTemplate(
            input_variables=["transcript"],
            template="""
            Analyze this technical discovery call for:
            - Technology stack preferences
            - Integration requirements
            - Performance requirements
            - Security considerations
            - Scalability needs

            Transcript: {transcript}
            """
        )

        response = self.llm.invoke(prompt_template.format(transcript=transcript))

        # Process and return structured technical data
        return self._parse_technical_response(response.content)
```

### Custom Output Formats

Extend the OutputFormatter for additional formats:

```python
# In output_formatter.py
class OutputFormatter:

    def format_powerpoint_outline(self, proposal_data: ProposalData) -> Dict[str, Any]:
        """Generate PowerPoint presentation outline."""
        return {
            "slides": [
                {
                    "title": "Executive Summary",
                    "content": proposal_data.executive_summary,
                    "slide_type": "title_content"
                },
                {
                    "title": "Implementation Roadmap",
                    "content": [phase.name for phase in proposal_data.implementation_phases],
                    "slide_type": "timeline"
                }
                # ... additional slides
            ]
        }

    def format_word_document(self, proposal_data: ProposalData) -> str:
        """Generate Word document using python-docx formatting."""
        # Implementation for Word document generation
        pass
```

### Custom AI Model Integration

Support different AI providers or models:

```python
# ai_models.py - New module
from abc import ABC, abstractmethod

class AIModelInterface(ABC):
    """Interface for AI model integrations."""

    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        pass

class AnthropicClaudeModel(AIModelInterface):
    """Integration with Anthropic Claude."""

    def __init__(self, api_key: str, model_name: str = "claude-3"):
        self.client = anthropic.Client(api_key=api_key)
        self.model_name = model_name

    def generate_text(self, prompt: str, **kwargs) -> str:
        response = self.client.messages.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text

# Update components to use interface
class ProposalGenerator:
    def __init__(self, ai_model: AIModelInterface):
        self.ai_model = ai_model
        # ... rest of implementation
```

### Plugin Architecture

Create a plugin system for extensibility:

```python
# plugins.py - New module
from typing import Protocol

class ProposalPlugin(Protocol):
    """Plugin interface for extending proposal generation."""

    def process_transcript(self, transcript: str) -> Dict[str, Any]:
        """Extract plugin-specific data from transcript."""
        ...

    def generate_content(self, data: Dict[str, Any]) -> str:
        """Generate plugin-specific content."""
        ...

    def get_template_section(self) -> str:
        """Return template section for plugin content."""
        ...

# Example industry-specific plugin
class FinancialServicesPlugin:
    """Plugin for financial services proposals."""

    def process_transcript(self, transcript: str) -> Dict[str, Any]:
        # Extract regulatory requirements, compliance needs
        pass

    def generate_content(self, data: Dict[str, Any]) -> str:
        # Generate compliance section, regulatory analysis
        pass

    def get_template_section(self) -> str:
        return '''
        ## Regulatory Compliance

        {{ plugin_content.financial_compliance }}
        '''
```

---

## Testing Guidelines

### Test Structure

Comprehensive testing strategy covering all components:

**Unit Tests**
```python
# tests/test_models.py
def test_customer_info_validation():
    """Test CustomerInfo model validation."""
    # Test valid data
    customer = CustomerInfo(
        company_name="Test Corp",
        industry="Technology",
        contact_person="John Doe"
    )
    assert customer.company_name == "Test Corp"

    # Test validation errors
    with pytest.raises(ValidationError):
        CustomerInfo(company_name="")  # Empty name should fail

def test_proposal_data_helper_methods():
    """Test ProposalData utility methods."""
    # Create test proposal with phases
    proposal = ProposalData(
        # ... required fields ...
        implementation_phases=[
            ImplementationPhase(name="Phase 1", activities=["Task 1"], duration_weeks=4, deliverables=[]),
            ImplementationPhase(name="Phase 2", activities=["Task 2"], duration_weeks=6, deliverables=[])
        ]
    )

    assert proposal.get_total_duration_weeks() == 10
    assert proposal.get_phase_names() == ["Phase 1", "Phase 2"]
```

**Integration Tests**
```python
# tests/test_workflow.py
@pytest.mark.integration
def test_full_workflow_integration(sample_transcript, tmp_path):
    """Test complete workflow from transcript to output files."""
    workflow = ProposalWorkflow("gpt-3.5-turbo")

    result = workflow.process_transcript_text(
        transcript_text=sample_transcript,
        output_folder=str(tmp_path),
        filename="test_proposal"
    )

    assert result["success"] is True
    assert "customer_info" in result
    assert "file_paths" in result

    # Verify files were created
    assert Path(result["file_paths"]["markdown"]).exists()
    assert Path(result["file_paths"]["json"]).exists()

    # Verify content structure
    with open(result["file_paths"]["json"]) as f:
        data = json.load(f)
        assert "customer_info" in data
        assert "executive_summary" in data
```

**Mock Testing for AI Calls**
```python
# tests/conftest.py
@pytest.fixture
def mock_openai_responses():
    """Mock OpenAI API responses for consistent testing."""
    return {
        "customer_extraction": {
            "company_name": "Test Company",
            "industry": "Technology",
            "contact_person": "John Smith",
            "email": "john@testcompany.com",
            "phone": null
        },
        "executive_summary": "This is a test executive summary...",
        # ... other mock responses
    }

# In test files
def test_customer_extraction_with_mock(mock_openai_responses):
    """Test customer extraction with mocked AI response."""
    processor = TranscriptionProcessor()

    # Mock the LLM response
    with patch.object(processor.llm, 'invoke') as mock_invoke:
        mock_invoke.return_value.content = json.dumps(mock_openai_responses["customer_extraction"])

        result = processor.extract_customer_info("test transcript")

        assert result.company_name == "Test Company"
        assert result.industry == "Technology"
```

### Test Configuration

**pytest Configuration (pytest.ini)**
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --cov=src/proposal_generator
    --cov-report=html
    --cov-report=term-missing
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow-running tests
    ai_dependent: Tests requiring AI API calls
```

**Environment-specific Testing**
```python
# tests/conftest.py
import os
import pytest

@pytest.fixture(scope="session")
def openai_api_available():
    """Check if OpenAI API key is available for integration tests."""
    return os.getenv("OPENAI_API_KEY") is not None

@pytest.mark.skipif(not openai_api_available(), reason="OpenAI API key not available")
def test_real_ai_integration():
    """Test with real AI API calls (only when API key available)."""
    pass
```

**Running Tests**
```bash
# Run all tests
pytest

# Run only unit tests
pytest -m unit

# Run with coverage
pytest --cov=src/proposal_generator --cov-report=html

# Run integration tests (requires API key)
pytest -m integration

# Run specific test file
pytest tests/test_models.py -v
```

---

## Code Style & Standards

### Style Requirements

**Black Code Formatting**
```bash
# Format all code
black src/ tests/

# Check formatting
black --check src/ tests/
```

**Import Organization (isort)**
```python
# Standard library imports
import os
import json
from typing import Dict, List, Optional

# Third-party imports
import pytest
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

# Local imports
from .models import CustomerInfo, ProposalData
from .transcription_processor import TranscriptionProcessor
```

**Type Annotations**
All functions must include proper type hints:

```python
# Good - properly typed
def process_transcript(
    transcript: str,
    output_folder: str = "./outputs",
    filename: Optional[str] = None
) -> Dict[str, Any]:
    pass

# Bad - missing type hints
def process_transcript(transcript, output_folder="./outputs", filename=None):
    pass
```

**Documentation Standards**
```python
def extract_customer_info(self, transcript: str) -> CustomerInfo:
    """
    Extract customer information from discovery call transcript.

    Uses AI-powered analysis to identify and structure customer details
    including company information, industry, and contact details.

    Args:
        transcript: Raw transcript text from discovery call

    Returns:
        CustomerInfo: Validated customer information model

    Raises:
        ValueError: If transcript is empty or invalid
        ValidationError: If extracted data fails model validation

    Example:
        >>> processor = TranscriptionProcessor()
        >>> info = processor.extract_customer_info("Call with ABC Corp...")
        >>> print(info.company_name)  # "ABC Corp"
    """
```

### Error Handling Standards

**Consistent Error Patterns**
```python
# Good - specific, actionable errors
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please set your OpenAI API key before using this tool."
    )

# Good - proper exception chaining
try:
    data = json.loads(response_content)
except json.JSONDecodeError as e:
    raise ValueError(f"Failed to parse AI response as JSON: {e}") from e

# Bad - generic, unhelpful errors
if not api_key:
    raise Exception("API key error")
```

**Logging Standards**
```python
import logging

logger = logging.getLogger(__name__)

def process_transcript_text(self, transcript: str) -> Dict[str, Any]:
    """Process transcript with proper logging."""
    logger.info("Starting transcript processing")

    try:
        logger.debug(f"Transcript length: {len(transcript)} characters")

        # Processing steps...
        customer_info = self._extract_customer_info(transcript)
        logger.info(f"Extracted customer info for: {customer_info.company_name}")

        return {"success": True, "data": result}

    except Exception as e:
        logger.error(f"Transcript processing failed: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
```

---

## Contributing Workflow

### Development Process

**1. Issue Creation**
- Use GitHub issues for bug reports and feature requests
- Include detailed reproduction steps for bugs
- Provide clear use cases and requirements for features

**2. Branch Strategy**
```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/new-content-section

# Work on your changes...
git add .
git commit -m "feat: add risk analysis section to proposals"

# Push and create pull request
git push origin feature/new-content-section
```

**3. Commit Message Standards**
```bash
# Format: <type>(<scope>): <description>
feat(generator): add ROI analysis section
fix(cli): handle empty transcript files gracefully
docs(api): update API reference with new methods
test(models): add validation tests for ProposalData
refactor(formatter): simplify template rendering logic
```

**4. Pull Request Process**
- Fill out PR template completely
- Include tests for new functionality
- Update documentation for API changes
- Ensure all CI checks pass
- Request review from core maintainers

**Code Review Checklist:**
- [ ] Code follows style guidelines (black, isort, flake8)
- [ ] All tests pass including new test coverage
- [ ] Documentation updated for public API changes
- [ ] Error handling follows project patterns
- [ ] Type hints are complete and accurate
- [ ] No sensitive information in commit history

### Release Process

**Version Management**
```bash
# Update version in multiple places:
# 1. src/proposal_generator/__init__.py
__version__ = "0.2.0"

# 2. pyproject.toml
version = "0.2.0"

# 3. Create git tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

**Release Notes Template**
```markdown
# Release v0.2.0

## New Features
- Added risk analysis section to proposals
- Support for custom AI model providers
- Enhanced CLI with debug mode

## Bug Fixes
- Fixed empty transcript file handling
- Resolved template rendering edge cases

## Breaking Changes
- Updated ProposalData model structure (migration guide below)

## Migration Guide
... detailed migration instructions ...
```

---

## Performance Optimization

### Caching Strategies

**AI Response Caching**
```python
# utils/cache.py
from functools import lru_cache
import hashlib

class AIResponseCache:
    """Cache AI responses to reduce API calls during development."""

    def __init__(self):
        self.cache = {}

    def get_cache_key(self, prompt: str, model: str) -> str:
        """Generate cache key from prompt and model."""
        content = f"{model}:{prompt}"
        return hashlib.md5(content.encode()).hexdigest()

    @lru_cache(maxsize=100)
    def get_cached_response(self, cache_key: str) -> Optional[str]:
        """Retrieve cached response."""
        return self.cache.get(cache_key)
```

**Template Compilation Caching**
```python
# In output_formatter.py
from jinja2 import Environment, BaseLoader

class OutputFormatter:
    def __init__(self):
        # Pre-compile templates for better performance
        self.env = Environment(loader=BaseLoader())
        self._compiled_templates = {
            'markdown': self.env.from_string(self._get_markdown_template()),
            'json': self.env.from_string(self._get_json_template())
        }

    def format_markdown(self, proposal_data: ProposalData) -> str:
        """Use pre-compiled template for faster rendering."""
        return self._compiled_templates['markdown'].render(
            proposal=proposal_data,
            total_weeks=proposal_data.get_total_duration_weeks()
        )
```

### Batch Processing Optimization

**Concurrent Processing**
```python
# batch_processor.py
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

class BatchProposalProcessor:
    """Process multiple transcripts concurrently."""

    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers
        self.workflow = ProposalWorkflow()

    async def process_batch(self, transcript_files: List[str]) -> List[Dict[str, Any]]:
        """Process multiple transcript files concurrently."""

        loop = asyncio.get_event_loop()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            tasks = [
                loop.run_in_executor(
                    executor,
                    self.workflow.process_transcript_file,
                    file_path
                )
                for file_path in transcript_files
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
```

### Memory Management

**Efficient Data Handling**
```python
def process_large_transcript(self, transcript_path: str) -> Dict[str, Any]:
    """Process large transcript files efficiently."""

    # Read file in chunks to avoid memory issues
    def read_in_chunks(file_path: str, chunk_size: int = 8192) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = []
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                content.append(chunk)
        return ''.join(content)

    # Process with memory cleanup
    try:
        transcript = read_in_chunks(transcript_path)
        result = self.process_transcript_text(transcript)

        # Clean up large variables
        del transcript

        return result

    except MemoryError:
        logger.error("Insufficient memory to process large transcript")
        return {"success": False, "error": "File too large to process"}
```

This developer guide provides a comprehensive foundation for understanding and extending the Proposal Generator system. The modular architecture, extensive testing framework, and clear extension patterns make it easy to customize the system for specific business needs while maintaining code quality and reliability.