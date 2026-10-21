
import json
from pathlib import Path

from extractor import extract_invoice

BASE_DIR = Path(__file__).resolve().parent
INVOICES_DIR = BASE_DIR / "invoices"
OUTPUT_DIR = BASE_DIR / "output"


def main():
    if not INVOICES_DIR.exists():
        print("Error: The invoices folder was not found.")
        return

    invoice_files = sorted(INVOICES_DIR.glob("*.txt"))

    if not invoice_files:
        print("No invoice text files found.")
        return

    total = len(invoice_files)
    successful = 0
    failed = 0

    print(f"Found {total} invoice file(s).")

    for invoice_file in invoice_files:
        print(f"\nProcessing: {invoice_file.name}")

        try:
            input_text = invoice_file.read_text(encoding="utf-8")
            result = extract_invoice(input_text)

            invoice_number = result["invoice_number"]
            safe_number = "".join(
                char if char.isalnum() or char in "-_" else "_"
                for char in invoice_number
            )

            output_file = OUTPUT_DIR / f"invoice_{safe_number}.json"
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

            output_file.write_text(
                json.dumps(result, indent=4, ensure_ascii=False),
                encoding="utf-8",
            )

            successful += 1
            print(f"Success! Saved to: {output_file.name}")

        except Exception as error:
            failed += 1
            print(f"Failed to process {invoice_file.name}: {error}")

    print("\n" + "=" * 35)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 35)
    print(f"Total invoices:     {total}")
    print(f"Successful:         {successful}")
    print(f"Failed:             {failed}")
    print("=" * 35)


if __name__ == "__main__":
    main()
