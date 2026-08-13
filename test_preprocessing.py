from pathlib import Path

import cv2
from paddleocr import PaddleOCR


IMAGE_PATH = "samples/id_card.jpg"

output_dir = Path("output/preprocessing")
output_dir.mkdir(parents=True, exist_ok=True)


# -----------------------------
# Load original image
# -----------------------------

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise FileNotFoundError(
        f"Image not found: {IMAGE_PATH}"
    )

print("Original shape:", image.shape)


# -----------------------------
# Upscale image 3x
# -----------------------------

upscaled = cv2.resize(
    image,
    None,
    fx=3,
    fy=3,
    interpolation=cv2.INTER_CUBIC,
)

upscaled_path = output_dir / "id_card_3x.jpg"

cv2.imwrite(
    str(upscaled_path),
    upscaled
)

print("Upscaled shape:", upscaled.shape)


# -----------------------------
# Initialize PaddleOCR
# -----------------------------

ocr = PaddleOCR(
    lang="vi",
    device="cpu",
    enable_mkldnn=False,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)


def run_ocr(image_path, title):

    print(f"\n========== {title} ==========\n")

    results = ocr.predict(str(image_path))

    for result in results:

        data = result.json["res"]

        texts = data["rec_texts"]
        scores = data["rec_scores"]

        for text, score in zip(texts, scores):

            status = (
                "OK"
                if score >= 0.90
                else "REVIEW"
            )

            print(
                f"{text:<45}"
                f"Confidence: {score:.2%} "
                f"[{status}]"
            )


# Original image
run_ocr(
    IMAGE_PATH,
    "ORIGINAL"
)

# 3x image
run_ocr(
    upscaled_path,
    "UPSCALED 3X"
)