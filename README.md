LLM JSON Invoice Extractor

An AI-powered invoice data extraction application that converts unstructured invoice text and PDF documents into structured, validated JSON using a locally running Large Language Model (LLM).

Project Overview

Manually extracting invoice details from documents can be time-consuming and error-prone. This project automates the process by using a local AI model to identify important invoice fields, validate the extracted information, and return structured JSON data.

The application includes a web interface, a Python backend API, PDF processing, batch invoice extraction, and data validation.

Features

AI-powered extraction: Extract invoice information using Ollama and the Llama 3.2 model.

Text-based extraction: Convert invoice text into structured JSON.

PDF invoice processing: Upload text-based PDF invoices and extract their details.

Web interface: Use a modern web interface to submit invoice text or upload PDF files.

REST API: Process extraction requests through FastAPI endpoints.

Data validation: Validate extracted fields using Pydantic.

Batch processing: Process multiple invoice text files.

JSON output: Return structured invoice information in a consistent format.

Local AI processing: Run the language model on your own computer using Ollama.

Technology Stack

Component

Technology

Programming language

Python

AI model runtime

Ollama

Language model

Llama 3.2

Backend framework

FastAPI

Data validation

Pydantic

PDF processing

pypdf

API server

Uvicorn

Frontend

HTML, CSS, JavaScript

Output format

JSON

Extracted Invoice Fields

The application extracts the following fields:

invoice_number — Invoice identification number

customer_name — Customer or company name

total_amount — Total invoice amount

currency — Three-letter currency code, such as INR

due_date — Payment due date in ISO format (YYYY-MM-DD)

Example output:

{
  "invoice_number": "INV-3001",
  "customer_name": "Sunrise Technologies",
  "total_amount": 18500.0,
  "currency": "INR",
  "due_date": "2026-11-15"
}

The example contains fictional invoice data.

Application Workflow

The user enters invoice text or uploads a PDF through the web interface.

The FastAPI backend receives the request.

For PDF uploads, pypdf extracts the document's text.

The extracted text is sent to the locally running Ollama model.

The model identifies the invoice fields and generates structured data.

Pydantic validates the extracted values.

The application returns the validated invoice details as JSON.

Project Structure

llm-json-extractor/
├── app.py
├── extractor.py
├── pdf_extractor.py
├── batch_extractor.py
├── schemas.py
├── prompts.py
├── index.html
├── requirements.txt
├── input_invoice.txt
├── invoices/
├── pdf_invoices/
├── samples/
└── README.md

The invoices/, pdf_invoices/, and samples/ folders contain sample inputs. The exact files may vary as the project develops.

Prerequisites

Install the following before running the application:

Python

Git (optional, for version control)

Ollama

A supported local language model

Installation and Setup

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd llm-json-extractor

Replace YOUR_GITHUB_REPOSITORY_URL with your repository's actual URL.

2. Create a virtual environment

python -m venv .venv

Activate it on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

3. Install Python dependencies

pip install -r requirements.txt

4. Install and start Ollama

Install Ollama from its official website:

https://ollama.com/

Download the required model:

ollama pull llama3.2

Ensure Ollama is running before starting the application.

5. Start the backend

From the project directory, run:

uvicorn app:app --reload

The API should be available at:

http://127.0.0.1:8000

6. Open the API documentation

Visit:

http://127.0.0.1:8000/docs

Use the interactive API documentation to test the extraction endpoints.

7. Open the web interface

Open index.html in your browser, or use the VS Code Live Server extension.

Keep the backend and Ollama running while using the interface.

API Endpoints

Method

Endpoint

Purpose

GET

/

Check backend availability

POST

/extract

Extract invoice details from text

POST

/extract-pdf

Extract invoice details from a PDF

The interactive API documentation is available at /docs while the backend is running.

Current Limitations

The application is designed as a local prototype and is not automatically hosted online.

The local Ollama model must be installed and running.

Scanned PDFs containing images may require OCR, which is not currently included in the described workflow.

AI-generated values should be checked against the original invoice before business or financial use.

Extraction accuracy depends on the input quality, prompt design, and model output.

Future Enhancements

Add OCR support for scanned invoices.

Support additional invoice formats and languages.

Add invoice history and database storage.

Improve error handling and extraction confidence reporting.

Add authentication and secure deployment.

Support additional document types.

Learning Outcomes

This project demonstrates practical experience with:

Local LLM integration

Prompt engineering

REST API development

PDF text extraction

Structured data validation

JSON generation

Frontend and backend integration

Batch document processing

Git and GitHub version control

Author

Kalaivani V

AI and Data Science Student

License

Choose and add an appropriate open-source license before distributing this project publicly.