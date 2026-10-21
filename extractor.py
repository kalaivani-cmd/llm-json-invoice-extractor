
import json
import re
from pathlib import Path

import ollama
from pydantic import ValidationError

from schemas import InvoiceData
from prompts import build_invoice_prompt


# Find the project folder
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "input_invoice.txt"
OUTPUT_DIR = BASE_DIR / "output"

# Local Ollama model
MODEL_NAME = "llama3.2:latest"


def parse_json_response(response_text: str) -> dict:
    """Convert the model response into a JSON dictionary."""

    if not response_text or not response_text.strip():
        raise ValueError("Ollama returned an empty response.")

    cleaned = response_text.strip()

    # Remove Markdown code fences if present
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    # Find and parse a JSON object
    decoder = json.JSONDecoder()

    for index, character in enumerate(cleaned):
        if character == "{":
            try:
                data, _ = decoder.raw_decode(cleaned[index:])

                if isinstance(data, dict):
                    return data

            except json.JSONDecodeError:
                continue

    raise ValueError(
        "Ollama did not return a valid JSON object. "
        "Check the model response and prompt."
    )


def extract_invoice(input_text: str) -> dict:
    """Extract invoice details using local Ollama and validate them."""

    if not input_text.strip():
        raise ValueError("The invoice input is empty.")

    prompt = build_invoice_prompt(input_text)

    print(f"Using local model: {MODEL_NAME}")

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract invoice information. "
                    "Return only one valid JSON object. "
                    "Do not include Markdown or explanations. "
                    "Use the exact field names required by the prompt. "
                    "Never invent missing invoice information."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        format="json",
        options={"temperature": 0},
    )

    response_text = response["message"]["content"]

    # Parse the model's JSON response
    extracted_data = parse_json_response(response_text)

    # Validate all required invoice fields
    invoice = InvoiceData.model_validate(extracted_data)

    # Return JSON-compatible data
    return invoice.model_dump(mode="json")


def main():
    try:
        if not INPUT_FILE.exists():
            raise FileNotFoundError(
                f"Input file not found: {INPUT_FILE}"
            )

        input_text = INPUT_FILE.read_text(encoding="utf-8")

        print("Reading invoice...")
        print("Extracting invoice using local Ollama...")

        result = extract_invoice(input_text)

        # Create the output folder
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Create a safe filename from the invoice number
        invoice_number = result["invoice_number"]
        safe_number = re.sub(
            r"[^A-Za-z0-9_-]",
            "_",
            invoice_number,
        )

        output_file = OUTPUT_DIR / f"invoice_{safe_number}.json"

        # Save the validated invoice
        output_file.write_text(
            json.dumps(result, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

        print("\nInvoice extracted successfully!")
        print("\nValidated invoice JSON:")
        print(json.dumps(result, indent=4))
        print(f"\nOutput saved to: {output_file}")

    except FileNotFoundError as error:
        print(f"\nFile error: {error}")

    except ValidationError as error:
        print("\nInvoice validation failed.")
        for item in error.errors():
            field = ".".join(str(part) for part in item["loc"])
            print(f"- {field}: {item['msg']}")

    except ValueError as error:
        print(f"\nExtraction error: {error}")

    except Exception as error:
        print(f"\nUnexpected error: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
