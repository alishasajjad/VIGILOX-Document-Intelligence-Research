from typing import Literal

from pydantic import BaseModel, ConfigDict


class ExtractedField(BaseModel):

    # Groq strict JSON Schema requirement:
    # additionalProperties: false
    model_config = ConfigDict(
        extra="forbid"
    )

    # Required field, but value can be null
    value: str | None

    # Required field
    source_line_ids: list[str]


class DocumentExtraction(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    document_type: Literal[
        "sia_badge",
        "id_card",
        "guard_license",
        "unknown",
    ]

    full_name: ExtractedField

    licence_number: ExtractedField

    id_number: ExtractedField

    expiry_date: ExtractedField

    date_of_birth: ExtractedField

    issue_date: ExtractedField

    issuer: ExtractedField