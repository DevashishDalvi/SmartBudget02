import re
from datetime import date as type_date
from datetime import datetime
from typing import Optional, Self

import pandas as pd
from pydantic import BaseModel, Field, field_validator, model_validator

# ---------- Utility cleaners ----------


def clean_text(value: str | None) -> Optional[str]:
    """
    Input is sanitized to have no aditional space after string
    """
    if value is None:
        return None
    value = str(value).strip()
    return value if value else None


def parse_quantity(value: int | None) -> Optional[int]:
    """
    Excel often stores quantities as:
    - strings like "3"
    - floats like 3.0
    - blanks or junk
    """
    if value is None:
        return None

    try:
        return int(float(str(value).strip()))
    except Exception as exc:
        raise ValueError(f"Invalid quantity: {value}") from exc


def parse_price(value: float | None) -> Optional[float]:
    """
    Handles:
    - "$10.50"
    - "10.5"
    - blank cells
    """
    if value is None:
        return None

    try:
        # Remove any non-numeric symbols except dot & minus
        clean = re.sub(r"[^\d.\-]", "", str(value))
        return float(clean)
    except Exception as exc:
        raise ValueError(f"Invalid price: {value}") from exc


# ---------- Row Model ----------


class TransactionRow(BaseModel):
    """
    Represents a single cleaned row from the Excel sheet.
    """

    date: type_date = Field(..., alias="Date")
    item: Optional[str] = Field(None, alias="Item")
    category: Optional[str] = Field(None, alias="Category")
    quantity: Optional[int] = Field(None, alias="Quantity")
    price: Optional[float] = Field(None, alias="Price")
    note: Optional[str] = Field(None, alias="Note")
    payment_method: Optional[str] = Field(None, alias="Payment Method")

    # ----- Config -----
    model_config = {
        "populate_by_name": True,
        "extra": "ignore",  # <-- THIS DROPS "Unnamed: x" COLUMNS
    }

    # ---------- Field-level validators ----------

    @field_validator("item", "category", "note", "payment_method", mode="before")
    @classmethod
    def clean_strings(cls, v: str) -> str | None:
        return clean_text(v)

    @field_validator("quantity", mode="before")
    @classmethod
    def validate_quantity(cls, v: int | None) -> int | None:
        return parse_quantity(v)

    @field_validator("price", mode="before")
    @classmethod
    def validate_price(cls, v: float | None) -> float | None:
        return parse_price(v)

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, v: str) -> type_date:
        """
        Handles:
        - pandas Timestamp
        - Excel datetime strings
        - naive ISO strings
        """
        if isinstance(v, datetime):
            return v

        try:
            return type_date.fromisoformat(str(v))
        except Exception as exc:
            raise ValueError(f"Invalid date: {v}") from exc

    # ---------- Row-level validation ----------

    @model_validator(mode="after")
    def check_required_business_rules(self) -> Self:
        """
        Example business rules:
        """
        if not self.item and not self.note:
            raise ValueError("Either Item or Note must be provided")

        if self.quantity is not None and self.quantity < 0:
            raise ValueError("Quantity cannot be negative")

        if self.price is not None and self.price < 0:
            raise ValueError("Price cannot be negative")

        return self


if __name__ == "__main__":
    raw_expense_df = pd.read_excel(
        "data/Budget 2025-26.xlsx", sheet_name="Expense Tracker"
    )
    cleaned_df = raw_expense_df.loc[:, ~raw_expense_df.columns.str.match(r"^Unnamed")]
    record = raw_expense_df.to_dict(orient="records")

    valid_rows = []
    errors = []

    for i, row in enumerate(record):
        try:
            validated = TransactionRow.model_validate(row)
            valid_rows.append(validated)
        except Exception as e:
            errors.append({"row": i, "error": str(e), "data": row})

    # print(valid_rows, errors)
