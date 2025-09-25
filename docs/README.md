# Documentation

Welcome to the Proposal Generator documentation! This directory contains comprehensive guides for users, developers, and contributors.

## Documentation Structure

### For Users
- **[Main README](../README.md)** - Quick start guide and basic usage
- **[Examples](../example_file_usage.py)** - Ready-to-run examples

### For Developers
- **[API Documentation](API.md)** - Complete reference for all classes and methods
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Architecture, extension patterns, and contribution guidelines

### For Contributors
- **[Contributing Guidelines](../CONTRIBUTING.md)** - How to contribute to the project
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Technical implementation details

## Quick Navigation

| I want to... | Go to |
|--------------|--------|
| **Get started quickly** | [Main README](../README.md#quick-start-3-steps) |
| **Run examples** | [Interactive Setup](../run_example.py) |
| **Understand the API** | [API Documentation](API.md) |
| **Extend the system** | [Developer Guide](DEVELOPER_GUIDE.md#extending-the-system) |
| **See the architecture** | [Developer Guide](DEVELOPER_GUIDE.md#architecture-overview) |
| **Contribute code** | [Contributing Guidelines](../CONTRIBUTING.md) |
| **Report issues** | [GitHub Issues](https://github.com/yourusername/proposal-generator/issues) |

## Documentation Highlights

### Complete API Reference
- All classes, methods, and parameters documented
- Code examples for every major function
- Error handling patterns
- Type hints and return values

### Architecture Deep-Dive
- Three-stage pipeline explanation
- Design decisions and trade-offs
- Data flow diagrams
- Extension patterns

### Developer Resources
- Setup instructions
- Testing guidelines
- Code style requirements
- CI/CD pipeline information

## Development Workflow

```bash
# 1. Setup development environment
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 2. Run examples to verify setup
python run_example.py

# 3. Explore the API
python -c "from proposal_generator import ProposalWorkflow; help(ProposalWorkflow)"

# 4. Read the documentation
# Start with API.md for technical reference
# Then DEVELOPER_GUIDE.md for architecture details
```

## Community

- **Questions?** Open a [Discussion](https://github.com/yourusername/proposal-generator/discussions)
- **Bug Reports:** Create an [Issue](https://github.com/yourusername/proposal-generator/issues)
- **Feature Requests:** Start with a [Discussion](https://github.com/yourusername/proposal-generator/discussions)
- **Contributions:** Read [CONTRIBUTING.md](../CONTRIBUTING.md) first

## Documentation Updates

This documentation is maintained alongside the codebase. When contributing:

1. **API changes** → Update `API.md`
2. **Architecture changes** → Update `DEVELOPER_GUIDE.md`
3. **New features** → Update relevant documentation
4. **Examples** → Keep code examples in sync

---

**Happy coding!**

*Last updated: 2024-09-25*