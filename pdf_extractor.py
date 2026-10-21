
from pathlib import Path
import json
import re

from pypdf import PdfReader
from extractor import extract_invoice

BASE_DIR = Path(__file__).resolve().parent
PDF_FILE = BASE_DIR / "pdf_invoices" / "sample_invoice.pdf"
OUTPUT_DIR = BASE_DIR / "output"


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract readable text from a PDF invoice."""

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    pages_text = []

    for page in reader.pages:
        pages_text.append(page.extract_text() or "")

    extracted_text = "\n".join(pages_text).strip()

    if not extracted_text:
        raise ValueError(
            "No text found. This PDF may be scanned and require OCR."
        )

    return extracted_text


def main():
    try:
        print("Reading PDF invoice...")
        invoice_text = extract_pdf_text(PDF_FILE)

        print("Sending extracted text to local Ollama AI...")
        result = extract_invoice(invoice_text)

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        invoice_number = result["invoice_number"]
        safe_number = re.sub(
            r"[^A-Za-z0-9_-]", "_", invoice_number
        )

        output_file = OUTPUT_DIR / f"invoice_{safe_number}.json"
        output_file.write_text(
            json.dumps(result, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

        print("\nPDF invoice extracted and validated successfully!")
        print(json.dumps(result, indent=4))
        print(f"\nJSON saved to: {output_file}")

    except Exception as error:
        print(f"\nError: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
