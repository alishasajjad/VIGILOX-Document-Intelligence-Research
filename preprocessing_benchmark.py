from pathlib import Path
import csv
import unicodedata

import cv2
import numpy as np

from src.ocr_service import OCRService


# ============================================================
# CONFIG
# ============================================================

SAMPLES = {
    "samples/sia_badge.jpg": {
        "licence_number": "1099 4265 1706 9065",
        "expiry_date": "24 MAR 2021",
        "full_name": "M.GREEN",
    },

    "samples/id_card.jpg": {
        "id_number": "026205000366",
        "full_name": "PHAN VAN MANH",
        "date_of_birth": "23/08/2006",
    },

    "samples/guard_license.jpg": {
        "licence_number": "12345678",
        "expiry_date": "01/01/2026",
        "date_of_birth": "01/01/1990",
        "full_name": "SAMPLE,JANE",
    },
}


OUTPUT_DIR = Path("output/preprocessing_benchmark")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize text for comparison.

    Example:
        SAMPLE,JANE
        Sample Jane
        SAMPLE JANE

    all become roughly comparable.
    """

    text = unicodedata.normalize("NFKD", text)

    text = "".join(
        char
        for char in text
        if not unicodedata.combining(char)
    )

    text = text.upper()

    return "".join(
        char
        for char in text
        if char.isalnum()
    )


# ============================================================
# PREPROCESSING
# ============================================================

def grayscale(image):
    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


def threshold_otsu(image):
    gray = grayscale(image)

    _, binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return binary


def estimate_skew_angle(image):
    """
    Estimate small rotation using horizontal lines.
    """

    gray = grayscale(image)

    edges = cv2.Canny(
        gray,
        50,
        150,
        apertureSize=3
    )

    height, width = gray.shape

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=30,
        minLineLength=max(30, width // 4),
        maxLineGap=10
    )

    if lines is None:
        return 0.0

    angles = []

    for line in lines:
        x1, y1, x2, y2 = line[0]

        angle = np.degrees(
            np.arctan2(
                y2 - y1,
                x2 - x1
            )
        )

        # We only care about small horizontal skew
        if -15 <= angle <= 15:
            angles.append(angle)

    if not angles:
        return 0.0

    return float(np.median(angles))


def deskew(image):
    angle = estimate_skew_angle(image)

    print(
        f"Detected skew angle: {angle:.2f}°"
    )

    # Already almost straight
    if abs(angle) < 0.3:
        return image.copy()

    height, width = image.shape[:2]

    center = (
        width // 2,
        height // 2
    )

    matrix = cv2.getRotationMatrix2D(
        center,
        -angle,
        1.0
    )

    rotated = cv2.warpAffine(
        image,
        matrix,
        (width, height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)
    )

    return rotated


# ============================================================
# SAVE PREPROCESSED IMAGE
# ============================================================

def save_variant(
    image,
    document_name,
    variant_name
):

    directory = (
        OUTPUT_DIR
        / document_name
    )

    directory.mkdir(
        parents=True,
        exist_ok=True
    )

    path = (
        directory
        / f"{variant_name}.jpg"
    )

    cv2.imwrite(
        str(path),
        image
    )

    return path


# ============================================================
# OCR
# ============================================================

def run_ocr(
    ocr_service,
    image_path
):

    results = ocr_service.extract(
        str(image_path)
    )

    return results


# ============================================================
# EVALUATION
# ============================================================

def evaluate(
    results,
    ground_truth
):

    all_text = " ".join(
        item["text"]
        for item in results
    )

    normalized_output = normalize_text(
        all_text
    )

    field_results = {}

    correct_count = 0

    for field_name, expected in ground_truth.items():

        expected_normalized = normalize_text(
            expected
        )

        correct = (
            expected_normalized
            in normalized_output
        )

        if correct:
            correct_count += 1

        matched_confidence = None

        for item in results:

            line_normalized = normalize_text(
                item["text"]
            )

            if (
                expected_normalized
                in line_normalized
            ):

                matched_confidence = (
                    item["confidence"]
                )

                break

        field_results[field_name] = {
            "expected": expected,
            "correct": correct,
            "confidence": matched_confidence,
        }

    accuracy = (
        correct_count
        / len(ground_truth)
    )

    average_confidence = (
        sum(
            item["confidence"]
            for item in results
        )
        / len(results)
        if results
        else 0
    )

    return {
        "accuracy": accuracy,
        "average_confidence": average_confidence,
        "fields": field_results,
    }


# ============================================================
# PRINT RESULT
# ============================================================

def print_result(
    variant,
    results,
    evaluation
):

    print(
        "\n"
        + "=" * 70
    )

    print(
        f"VARIANT: {variant.upper()}"
    )

    print(
        "=" * 70
    )

    print("\nOCR OUTPUT:\n")

    for item in results:

        confidence = (
            item["confidence"]
        )

        status = (
            "OK"
            if confidence >= 0.90
            else "REVIEW"
        )

        print(
            f"{item['text']:<45}"
            f"{confidence:.2%} "
            f"[{status}]"
        )

    print(
        "\nCRITICAL FIELD EVALUATION:\n"
    )

    for field, info in (
        evaluation["fields"].items()
    ):

        status = (
            "CORRECT"
            if info["correct"]
            else "WRONG / MISSING"
        )

        confidence = (
            f"{info['confidence']:.2%}"
            if info["confidence"]
            is not None
            else "N/A"
        )

        print(
            f"{field:<20}"
            f"{status:<18}"
            f"Confidence: {confidence}"
        )

    print(
        "\nCritical Field Accuracy:",
        f"{evaluation['accuracy']:.2%}"
    )

    print(
        "Average OCR Confidence:",
        f"{evaluation['average_confidence']:.2%}"
    )


# ============================================================
# MAIN
# ============================================================

ocr = OCRService()

csv_rows = []


for sample_path, ground_truth in SAMPLES.items():

    print(
        "\n\n"
        + "#" * 80
    )

    print(
        f"DOCUMENT: {sample_path}"
    )

    print(
        "#" * 80
    )

    image = cv2.imread(
        sample_path
    )

    if image is None:

        print(
            f"Could not load: {sample_path}"
        )

        continue

    document_name = Path(
        sample_path
    ).stem


    # --------------------------------------------------------
    # Create preprocessing variants
    # --------------------------------------------------------

    variants = {
        "original": image,
        "grayscale": grayscale(image),
        "threshold": threshold_otsu(image),
        "deskew": deskew(image),
    }


    # --------------------------------------------------------
    # Run benchmark
    # --------------------------------------------------------

    for variant_name, variant_image in (
        variants.items()
    ):

        variant_path = save_variant(
            variant_image,
            document_name,
            variant_name
        )

        results = run_ocr(
            ocr,
            variant_path
        )

        evaluation = evaluate(
            results,
            ground_truth
        )

        print_result(
            variant_name,
            results,
            evaluation
        )


        # ----------------------------------------------------
        # CSV
        # ----------------------------------------------------

        csv_rows.append({
            "document": document_name,
            "variant": variant_name,

            "critical_field_accuracy":
                evaluation["accuracy"],

            "average_ocr_confidence":
                evaluation[
                    "average_confidence"
                ],
        })


# ============================================================
# SAVE CSV REPORT
# ============================================================

csv_path = (
    OUTPUT_DIR
    / "benchmark_summary.csv"
)

with open(
    csv_path,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "document",
            "variant",
            "critical_field_accuracy",
            "average_ocr_confidence",
        ],
    )

    writer.writeheader()

    writer.writerows(
        csv_rows
    )


print(
    "\n\nBenchmark complete."
)

print(
    f"CSV saved to: {csv_path}"
)