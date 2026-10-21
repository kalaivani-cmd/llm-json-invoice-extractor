
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from pypdf import PdfReader
from io import BytesIO

from extractor import extract_invoice


app = FastAPI(title="LLM Invoice Extractor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvoiceRequest(BaseModel):
    invoice_text: str = Field(min_length=1)


@app.get("/")
def home():
    return {
        "message": "LLM JSON Extractor API is running!"
    }


@app.post("/extract")
def extract(request: InvoiceRequest):
    try:
        result = extract_invoice(request.invoice_text)
        return {
            "success": True,
            "invoice": result,
        }

    except ValidationError as error:
        raise HTTPException(
            status_code=422,
            detail=error.errors(include_url=False),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Invoice extraction failed: {error}",
        )
    
@app.post("/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    try:
        pdf_bytes = await file.read()
        reader = PdfReader(BytesIO(pdf_bytes))

        invoice_text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        ).strip()

        if not invoice_text:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the PDF."
            )

        result = extract_invoice(invoice_text)

        return {
            "success": True,
            "invoice": result
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"PDF extraction failed: {error}"
        )
    finally:
        await file.close()
