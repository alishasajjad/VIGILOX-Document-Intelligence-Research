from src.ocr_service import OCRService


ocr = OCRService()

test_images = [
    "samples/sia_badge.jpg",
    "samples/id_card.jpg",
    "samples/guard_license.jpg",
]


for image_path in test_images:

    print("\n" + "=" * 60)
    print(f"IMAGE: {image_path}")
    print("=" * 60)

    results = ocr.extract(image_path)

    for field in results:

        status = (
            "OK"
            if field["confidence"] >= 0.90
            else "REVIEW"
        )

        print(
            f"{field['text']:<35}"
            f"{field['confidence']:.2%} "
            f"[{status}]"
        )


# from paddleocr import PaddleOCR

# ocr = PaddleOCR(
#     lang="vi",
#     device="cpu",
#     enable_mkldnn=False,
#     use_doc_orientation_classify=False,
#     use_doc_unwarping=False,
#     use_textline_orientation=True,
# )

# image_path = "samples/id_card.jpg"

# results = ocr.predict(image_path)

# for result in results:

#     data = result.json["res"]

#     texts = data["rec_texts"]
#     scores = data["rec_scores"]

#     print("\n========== OCR RESULT ==========\n")

#     for text, score in zip(texts, scores):

#         status = "OK"

#         if score < 0.80:
#             status = "REVIEW"

#         print(
#             f"{text:<35} "
#             f"Confidence: {score:.2%} "
#             f"[{status}]"
#         )

#     result.save_to_img("output")
#     result.save_to_json("output")


# from paddleocr import PaddleOCR

# ocr = PaddleOCR(
#     lang="en",
#     device="cpu",
#     enable_mkldnn=False,
#     use_doc_orientation_classify=False,
#     use_doc_unwarping=False,
#     use_textline_orientation=False,
# )

# image_path = "samples/sia_badge.jpg"

# results = ocr.predict(image_path)

# for result in results:
#     result.print()
#     result.save_to_img("output")
#     result.save_to_json("output")