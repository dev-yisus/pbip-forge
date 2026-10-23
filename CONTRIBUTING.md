# Contributing to pbip-forge

Thank you for your interest in contributing to **pbip-forge**! We welcome contributions from developers, data engineers, and AI practitioners.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/<your-username>/pbip-forge.git
   cd pbip-forge
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .
   ```

## Development Workflow

1. Create a descriptive feature branch:
   ```bash
   git checkout -b feat/support-custom-visuals
   ```
2. Implement your changes following standard Python conventions (PEP 8).
3. Ensure all unit tests pass:
   ```bash
   python -m unittest discover tests
   ```
4. If introducing new TMDL syntax or visual formats, add corresponding test cases in `tests/`.

## Pull Request Guidelines

- Provide a concise title and clear description of what changed.
- Reference any relevant issues (e.g., `Closes #12`).
- Ensure no sensitive information or unneeded artifacts are committed.
- All PRs are reviewed before merging into `main`.

## Reporting Bugs & Suggesting Enhancements

- Use the [Issue Tracker](https://github.com/dev-yisus/pbip-forge/issues).
- Provide a reproducible minimal example or dataset when reporting bugs.
