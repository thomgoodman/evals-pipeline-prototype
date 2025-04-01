# Automated Evaluation Tests

This repository contains automated tests for evaluating an AI assistant's responses.

## Running Tests Locally

1. Clone the repository
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run tests:
   ```
   pytest test_assistant.py -v
   ```

## GitHub Actions Setup

The repository includes a GitHub Actions workflow that runs tests automatically on every push to main and on pull requests.

To set up GitHub Actions:

1. Go to your GitHub repository
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Add a secret with name `OPENAI_API_KEY` and your OpenAI API key as the value
5. Commit and push to trigger the workflow 