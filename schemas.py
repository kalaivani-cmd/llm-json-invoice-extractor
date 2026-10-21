
from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InvoiceData(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True
    )

    invoice_number: str = Field(min_length=1)
    customer_name: str = Field(min_length=1)
    total_amount: float = Field(ge=0)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    due_date: date

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value
