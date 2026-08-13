from paddleocr import PaddleOCR


class OCRService:

    def __init__(self):

        self.ocr = PaddleOCR(
            lang="en",
            device="cpu",
            enable_mkldnn=False,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=True,
        )

    def extract(self, image_path: str):

        results = self.ocr.predict(image_path)

        extracted_lines = []

        for result in results:

            data = result.json["res"]

            texts = data["rec_texts"]
            scores = data["rec_scores"]
            boxes = data["rec_boxes"]

            for text, score, box in zip(
                texts,
                scores,
                boxes
            ):

                bbox = (
                    box.tolist()
                    if hasattr(box, "tolist")
                    else box
                )

                extracted_lines.append({
                    "text": text,
                    "confidence": float(score),
                    "bbox": bbox
                })

        return extracted_lines