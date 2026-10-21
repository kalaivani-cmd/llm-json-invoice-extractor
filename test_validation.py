
from pydantic import ValidationError
from schemas import InvoiceData


valid_invoice = {
    "invoice_number": "INV-1001",
    "customer_name": "ABC Technologies",
    "total_amount": 12500.0,
    "currency": "INR",
    "due_date": "2026-11-15",
}


def test_invoice(description, data, should_pass):
    print(f"\nTest: {description}")

    try:
        InvoiceData.model_validate(data)
        if should_pass:
            print("PASS: Valid invoice accepted.")
        else:
            print("FAIL: Invalid invoice was accepted.")

    except (ValidationError, ValueError) as error:
        if should_pass:
            print(f"FAIL: Valid invoice rejected: {error}")
        else:
            print("PASS: Invalid invoice rejected.")


# Test 1: Valid invoice
test_invoice(
    "Valid invoice",
    valid_invoice,
    True,
)

# Test 2: Negative amount
negative_amount = {
    **valid_invoice,
    "total_amount": -500.0,
}
test_invoice(
    "Negative amount",
    negative_amount,
    False,
)

# Test 3: Invalid currency
invalid_currency = {
    **valid_invoice,
    "currency": "INDIA",
}
test_invoice(
    "Invalid currency",
    invalid_currency,
    False,
)

# Test 4: Missing invoice number
missing_number = {
    key: value
    for key, value in valid_invoice.items()
    if key != "invoice_number"
}
test_invoice(
    "Missing invoice number",
    missing_number,
    False,
)

# Test 5: Invalid date
invalid_date = {
    **valid_invoice,
    "due_date": "not-a-date",
}
test_invoice(
    "Invalid date",
    invalid_date,
    False,
)
