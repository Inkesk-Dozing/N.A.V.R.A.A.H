# Contributing to N.A.V.R.A.A.H

Thank you for your interest in contributing to N.A.V.R.A.A.H (Navigation Assistant For Visually Restricted And Aided Humans)! We welcome contributions from everyone who wants to help make technology more accessible.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Questions and Support](#questions-and-support)

## Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors. We expect all participants to:

- Be respectful and considerate in communication
- Welcome newcomers and help them get started
- Be open to constructive feedback
- Focus on what is best for the community and project
- Show empathy towards other community members

## How Can I Contribute?

There are many ways to contribute to N.A.V.R.A.A.H:

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Screenshots or error messages (if applicable)
- Your environment details (OS, browser, version, etc.)

### Suggesting Enhancements

We welcome feature requests and enhancement suggestions:
- Use a clear and descriptive title
- Provide a detailed description of the suggested enhancement
- Explain why this enhancement would be useful
- Include examples or mockups if possible

### Contributing Code

We appreciate code contributions! See the sections below for our development workflow and guidelines.

### Improving Documentation

Documentation improvements are always welcome:
- Fix typos or clarify existing documentation
- Add missing documentation
- Translate documentation
- Create tutorials or examples

## Getting Started

### Prerequisites

Before you begin, ensure you have:
- Git installed on your local machine
- Access to a GitHub account
- Familiarity with the technologies used in this project

### Setting Up Your Development Environment

1. **Fork the Repository**
   
   Click the "Fork" button at the top right of the repository page.

2. **Clone Your Fork**
   
   ```bash
   git clone https://github.com/YOUR-USERNAME/N.A.V.R.A.A.H.git
   cd N.A.V.R.A.A.H
   ```

3. **Add Upstream Remote**
   
   ```bash
   git remote add upstream https://github.com/Inkesk-Dozing/N.A.V.R.A.A.H.git
   ```

4. **Install Dependencies**
   
   Follow the installation instructions in the README.md file.

## Development Workflow

1. **Create a Branch**
   
   Create a new branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   
   Use descriptive branch names:
   - `feature/` for new features
   - `bugfix/` for bug fixes
   - `docs/` for documentation changes
   - `refactor/` for code refactoring

2. **Make Your Changes**
   
   - Write clear, readable code
   - Follow the coding standards (see below)
   - Test your changes thoroughly
   - Update documentation as needed

3. **Keep Your Branch Updated**
   
   Regularly sync with the upstream repository:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

4. **Commit Your Changes**
   
   Follow our commit guidelines (see below):
   ```bash
   git add .
   git commit -m "type: brief description"
   ```

5. **Push Your Changes**
   
   ```bash
   git push origin feature/your-feature-name
   ```

## Coding Standards

### General Guidelines

- Write clean, readable, and maintainable code
- Use meaningful variable and function names
- Keep functions small and focused on a single task
- Comment complex logic, but write self-documenting code when possible
- Follow the existing code style in the project

### Accessibility Considerations

Since N.A.V.R.A.A.H focuses on accessibility:

- Ensure all UI elements are keyboard accessible
- Provide appropriate ARIA labels and roles
- Test with screen readers when possible
- Maintain sufficient color contrast ratios
- Provide text alternatives for non-text content
- Ensure responsive design works across devices

### Testing

- Write tests for new features and bug fixes
- Ensure all tests pass before submitting a pull request
- Aim for good test coverage of your code
- Include both unit tests and integration tests where appropriate

## Commit Guidelines

We follow conventional commit messages for clarity and consistency:

### Format

```
type(scope): subject

body (optional)

footer (optional)
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semi-colons, etc.)
- `refactor`: Code refactoring without changing functionality
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates, etc.

### Examples

```
feat(navigation): add voice command support

Add support for voice commands to control navigation features.
Implements basic voice recognition using Web Speech API.

Closes #123
```

```
fix(audio): resolve audio feedback loop

Fix issue where audio cues were causing feedback loop in certain
browsers. Added audio context management to prevent conflicts.

Fixes #456
```

## Pull Request Process

1. **Before Submitting**
   
   - Ensure your code follows the coding standards
   - Run all tests and make sure they pass
   - Update documentation if needed
   - Rebase your branch on the latest upstream/main

2. **Creating a Pull Request**
   
   - Use a clear and descriptive title
   - Fill out the pull request template completely
   - Reference any related issues
   - Provide context for your changes
   - Include screenshots or videos for UI changes

3. **Pull Request Template**

   ```markdown
   ## Description
   Brief description of your changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Other (please describe)

   ## Related Issues
   Closes #(issue number)

   ## Testing
   Describe how you tested your changes

   ## Accessibility Impact
   Describe any accessibility improvements or impacts

   ## Screenshots (if applicable)
   Add screenshots to help explain your changes
   ```

4. **Code Review**
   
   - Be responsive to feedback
   - Make requested changes promptly
   - Engage in constructive discussion
   - Update your pull request as needed

5. **After Approval**
   
   - A maintainer will merge your pull request
   - Your changes will be included in the next release
   - Thank you for your contribution!

## Issue Guidelines

### Creating an Issue

When creating an issue:

1. **Check Existing Issues**
   
   Search for existing issues to avoid duplicates.

2. **Use Issue Templates**
   
   Use the appropriate issue template when available.

3. **Provide Detailed Information**
   
   Include all relevant details to help us understand and reproduce the issue.

### Issue Labels

We use labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `accessibility`: Accessibility-related issues
- `priority: high/medium/low`: Priority level

## Questions and Support

### Getting Help

If you have questions:

- Check the documentation first
- Search existing issues and discussions
- Create a new issue with the `question` label
- Reach out to the maintainers

### Contact

For sensitive matters or private inquiries:
- Open an issue and tag the maintainers
- Check the repository for contact information

## Recognition

We value all contributions! Contributors will be:
- Listed in the project's contributors
- Mentioned in release notes for significant contributions
- Part of a welcoming and supportive community

## License

By contributing to N.A.V.R.A.A.H, you agree that your contributions will be licensed under the Apache License 2.0, the same license as the project.

---

Thank you for contributing to N.A.V.R.A.A.H and helping make navigation technology more accessible for everyone! 🚀
