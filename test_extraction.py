from dotenv import load_dotenv

from src.ocr_service import OCRService
from src.extraction_service import ExtractionService
from src.evidence_validator import EvidenceValidator


load_dotenv()


ocr_service = OCRService()

extraction_service = ExtractionService()

evidence_validator = EvidenceValidator()


# ---------------------------------------
# STEP 1 — OCR
# ---------------------------------------

image_path = "samples/sia_badge.jpg"

ocr_lines = ocr_service.extract(
    image_path
)


print(
    "\n========== RAW OCR ==========\n"
)

for index, line in enumerate(ocr_lines):

    print(
        f"[L{index}] "
        f"{line['text']:<35}"
        f"{line['confidence']:.2%}"
)


# ---------------------------------------
# STEP 2 — STRUCTURED EXTRACTION
# ---------------------------------------

structured = extraction_service.extract(
    ocr_lines
)


print(
    "\n========== STRUCTURED EXTRACTION ==========\n"
)

print(
    structured.model_dump_json(
        indent=2
    )
)


# ---------------------------------------
# STEP 3 — EVIDENCE VALIDATION
# ---------------------------------------

flags = evidence_validator.validate(
    structured,
    ocr_lines,
)


print(
    "\n========== EVIDENCE VALIDATION ==========\n"
)

if flags:

    for flag in flags:

        print(
            f"[REVIEW] {flag}"
        )

else:

    print(
        "All evidence references are valid."
    )