# Contributing to Proposal Generator

Thank you for your interest in contributing! This project welcomes contributions from everyone.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- OpenAI API key for testing
- Familiarity with LangChain and Pydantic

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/proposal-generator.git
   cd proposal-generator
   ```

2. **Set up development environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

4. **Verify setup**
   ```bash
   python example_file_usage.py
   ```

## Development Workflow

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to all public methods
- Keep functions focused and well-named

### Testing

```bash
# Run tests (if available)
python -m pytest

# Run examples to verify functionality
python example_file_usage.py
python example_usage.py
```

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code patterns
   - Update documentation as needed
   - Test your changes thoroughly

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

4. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Types of Contributions

### Bug Reports

When filing a bug report, please include:
- Python version
- Operating system
- Steps to reproduce
- Error messages
- Sample input that causes the issue

### Feature Requests

For feature requests, please:
- Describe the use case
- Explain why this would be valuable
- Provide examples if possible
- Consider backwards compatibility

### Code Contributions

Areas where we welcome contributions:
- Bug fixes
- Performance improvements
- Documentation improvements
- New output formats
- Additional AI model support
- Enhanced error handling

## Code Guidelines

### Architecture

The project follows a three-stage pipeline:
1. **TranscriptionProcessor** - Extracts structured data from text
2. **ProposalGenerator** - Creates proposal content using AI
3. **OutputFormatter** - Formats output in multiple formats

### Key Principles

- **Single Responsibility** - Each class has one clear purpose
- **Configuration** - Use environment variables for settings
- **Error Handling** - Provide clear, actionable error messages
- **Type Safety** - Use Pydantic models for data validation

### Adding New Features

1. **Analysis Phase** - Understand the existing codebase
2. **Design Phase** - Plan how your feature fits in
3. **Implementation** - Write clean, tested code
4. **Documentation** - Update relevant docs
5. **Testing** - Ensure everything works

## Documentation

When making changes that affect user-facing functionality:

1. **Update API docs** - Modify `docs/API.md`
2. **Update developer guide** - Modify `docs/DEVELOPER_GUIDE.md`
3. **Update examples** - Keep code examples current
4. **Update README** - Reflect any new features or changes

## Pull Request Process

1. **Fill out the PR template** completely
2. **Reference any related issues** using keywords like "Fixes #123"
3. **Provide clear description** of what changed and why
4. **Include test results** or example output
5. **Update documentation** as needed

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Examples still work
- [ ] No API keys or secrets in commits
- [ ] Backwards compatibility considered

## Getting Help

- **Questions?** Open a Discussion
- **Stuck?** Check existing Issues
- **Want to chat?** Start a Discussion

## Recognition

Contributors will be acknowledged in:
- Release notes
- Contributors section
- Git commit history

Thank you for helping make Proposal Generator better!