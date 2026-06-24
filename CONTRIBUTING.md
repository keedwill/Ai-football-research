# Contributing to AI Football Research System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## 🤝 Code of Conduct

This project follows a standard code of conduct:

- **Be Respectful**: Treat everyone with respect and kindness
- **Be Collaborative**: Work together constructively
- **Be Patient**: Help newcomers and be open to learning
- **Be Professional**: Keep discussions focused and productive

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- Basic knowledge of FastAPI and React

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-football-research.git
   cd ai-football-research
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/ai-football-research.git
   ```

## 💻 Development Setup

### Backend Setup

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate    # macOS/Linux
pip install -r requirements.txt
cp .env.example .env
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Running Tests

```bash
cd backend
pytest
python test_architecture.py
python test_frontend_integration.py
```

## 📝 How to Contribute

### Types of Contributions

We welcome:

- 🐛 **Bug Fixes**: Fix issues and improve stability
- ✨ **Features**: Add new capabilities
- 📚 **Documentation**: Improve docs and examples
- 🎨 **UI/UX**: Enhance frontend design
- ⚡ **Performance**: Optimize code and queries
- 🧪 **Tests**: Increase test coverage

### Contribution Workflow

1. **Check Issues**: Look for existing issues or create a new one
2. **Discuss**: Comment on the issue to discuss your approach
3. **Create Branch**: Create a feature branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make Changes**: Write clean, tested code
5. **Commit**: Write clear commit messages
   ```bash
   git commit -m "Add: feature description"
   ```
6. **Push**: Push your branch to your fork
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Pull Request**: Open a PR against `main` branch

## 📐 Coding Standards

### Python (Backend)

- **Style**: Follow PEP 8
- **Type Hints**: Use type annotations for all functions
- **Docstrings**: Document all public functions
- **Imports**: Group imports (standard, third-party, local)
- **Line Length**: Max 88 characters (Black formatter)

**Example:**

```python
from typing import Optional

def get_team_form(team_name: str) -> Optional[str]:
    """
    Retrieve recent form for a football team.

    Args:
        team_name: Name of the team to analyze

    Returns:
        Form string (e.g., "WWDLW") or None if not found
    """
    # Implementation here
    pass
```

### JavaScript/React (Frontend)

- **Style**: Use Prettier for formatting
- **Components**: Functional components with hooks
- **Naming**: PascalCase for components, camelCase for variables
- **Props**: Destructure props in function parameters
- **Comments**: JSDoc comments for complex functions

**Example:**

```javascript
/**
 * Displays match analysis results
 * @param {Object} props - Component props
 * @param {Object} props.result - Analysis data
 * @param {string} props.error - Error message if any
 */
function ResultDisplay({ result, error }) {
  // Implementation here
}
```

### Architecture Principles

- **Layer Separation**: Keep API, Service, Agent, Tools layers distinct
- **Single Responsibility**: Each function/class has one clear purpose
- **DRY**: Don't repeat yourself - use constants and utilities
- **Error Handling**: Use custom exceptions, not generic ones
- **Logging**: Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)

## 🧪 Testing Guidelines

### Write Tests For:

- ✅ New features
- ✅ Bug fixes
- ✅ Edge cases
- ✅ Error conditions

### Test Structure

```python
def test_feature_name():
    """Test description explaining what is being tested."""
    # Arrange
    input_data = "test input"

    # Act
    result = function_to_test(input_data)

    # Assert
    assert result == expected_output
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
python test_api.py

# Run with coverage
pytest --cov=app --cov-report=html
```

## 🔄 Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### PR Description Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing

Describe how you tested the changes

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added and passing
```

### Review Process

1. **Automated Checks**: CI/CD will run tests
2. **Code Review**: Maintainers will review your code
3. **Feedback**: Address any requested changes
4. **Approval**: Once approved, your PR will be merged

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, include:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Numbered steps to reproduce
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python/Node version, etc.
- **Screenshots**: If applicable
- **Logs**: Relevant error messages

**Template:**

```markdown
### Bug Description

Clear description here

### Steps to Reproduce

1. Step one
2. Step two
3. Step three

### Expected Behavior

What should happen

### Actual Behavior

What actually happens

### Environment

- OS: Windows 11
- Python: 3.11.5
- Node: 18.16.0

### Additional Context

Any other relevant information
```

### Feature Requests

When requesting features, include:

- **Problem**: What problem does this solve?
- **Solution**: Proposed solution
- **Alternatives**: Alternative solutions considered
- **Additional Context**: Mockups, examples, etc.

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

## 💬 Questions?

If you have questions:

1. Check existing issues and documentation
2. Search for similar questions
3. Open a new issue with the "question" label
4. Join discussions in existing issues

## 🎉 Thank You!

Thank you for contributing to AI Football Research System! Your efforts help make this project better for everyone.

---

**Happy Coding! ⚽**
