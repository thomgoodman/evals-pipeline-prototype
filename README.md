# Automated Evaluation Tests

![Tests Status](https://github.com/thomgoodman/evals-pipeline-prototype/actions/workflows/python-tests.yml/badge.svg)

An example framework for automated evaluation of AI assistant responses using OpenAI's API. This repository provides tools to systematically test AI model behaviors, detect hallucinations, and measure response quality across various scenarios.

## 📋 Features

- Automated evaluation of AI assistant responses
- Customizable test scenarios and expectations
- Hallucination detection tests
- Quiz generation evaluation
- CI/CD integration via GitHub Actions
- Detailed test reporting

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/automated-evals.git
   cd automated-evals
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## 🔬 Running Tests

### Basic Test Suite

```bash
pytest test_assistant.py -v
```

### Advanced Test Options

Run specific test modules:
```bash
pytest test_hallucinations.py -v
pytest test_release_evals.py -v
pytest test_app.py -v
```

Run tests with dataset:
```bash
python test_with_dataset.py
```

Generate and save evaluation artifacts:
```bash
python save_eval_artifacts.py
```

### Unit Tests

The project includes comprehensive unit tests in `test_app.py` that verify:

- File operations: Tests for the `read_file_into_string` function with success and error scenarios
- Quiz generation: Tests for category validation using mock OpenAI responses
- Error handling: Tests for handling unknown quiz categories
- All tests use proper mocking to avoid actual API calls

Run the unit tests with:
```bash
pytest test_app.py -v
```

## 📊 Test Structure

- `test_assistant.py`: Basic assistant response tests
- `test_hallucinations.py`: Tests for detecting incorrect information
- `test_release_evals.py`: Comprehensive release qualification tests
- `test_with_dataset.py`: Dataset-based evaluation tests
- `test_app.py`: Unit tests for the core app functionality
  - Tests for file reading functionality (`read_file_into_string`)
  - Quiz category validation tests
  - Error handling for unknown categories
  - Mock testing with LangChain components
- `app.py`: Core assistant chain implementation
- `quiz_bank.txt`: Knowledge base for quiz generation tests

## 🔄 CI/CD Integration

This repository includes GitHub Actions workflows that automatically run tests on:
- Every push to the main branch
- All pull requests

### Setting up GitHub Actions

1. Go to your GitHub repository
2. Navigate to "Settings" > "Secrets and variables" > "Actions"
3. Create a new repository secret named `OPENAI_API_KEY` with your API key
4. Push to trigger the workflow

## 🧪 Testing Approach

### Unit Testing Strategy

The unit tests in `test_app.py` use Python's `unittest.mock` library with `MagicMock` to isolate code functionality:

- **Dependency Isolation**: All external dependencies (OpenAI API, file system) are mocked to focus testing on core logic
- **Mock Control**: Tests precisely control inputs and outputs of dependencies to create predictable test scenarios
- **Behavior Verification**: Tests verify both return values and that functions interact with dependencies correctly

For example, when testing the assistant chain:
1. A `MagicMock` replaces the LangChain components and controls responses
2. Tests verify the function correctly processes both valid and invalid categories
3. System message construction is verified to contain proper instructions

Unit tests focus on core functionality, while integration and end-to-end testing is handled by `test_assistant.py` and `test_release_evals.py`.

## 📝 License

[MIT License](LICENSE)

## 📬 Contact

For questions and feedback, please open an issue in the GitHub repository.