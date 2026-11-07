
# AI Text Analyzer

A Python application that uses the OpenAI API
to analyze text and return structured results.

## Features

- Text summarization
- Sentiment analysis
- Keyword extraction
- Topic identification
- Text classification
- Structured JSON output
- Pydantic validation
- Token usage tracking
- Latency tracking
- Error handling

## Technologies

- Python
- OpenAI Responses API
- Pydantic
- python-dotenv
- tiktoken

## Installation

Clone the repository or download the project.

Create a virtual environment:

python -m venv venv

Activate the environment:

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Configure your .env file:

OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-mini

## Run the application

python main.py

## Output

The application returns:

- Summary
- Sentiment
- Confidence
- Keywords
- Topics
- Category
- Token usage
- Request ID
- Execution time

The analysis is also saved to:

analysis_result.json
