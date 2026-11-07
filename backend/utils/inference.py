import torch
import torch.nn.functional as F
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
from config.config import MODEL_NAME


class TomatoDiseaseModel:

    def __init__(self):
        print("Loading model...")

        self.processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
        self.model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)

        self.model.eval()

        self.labels = self.model.config.id2label

        print("Model loaded")

    def predict(self, frame):

        image = Image.fromarray(frame)

        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)

        probs = F.softmax(outputs.logits, dim=-1)

        pred_idx = torch.argmax(probs).item()

        label = self.labels[pred_idx]

        confidence = probs[0][pred_idx].item()

        return label, confidence

    def _extract_disease_stage(self, label):
        lowered = label.lower()

        if "healthy" in lowered:
            return "healthy"
        if "early" in lowered:
            return "early"
        if "late" in lowered:
            return "late"
        if "severe" in lowered:
            return "severe"

        return "detected"

    def _extract_disease_level(self, stage):
        # 0 to 4 severity scale for frontend color-coding.
        if stage == "healthy":
            return 0
        if stage == "early":
            return 1
        if stage == "detected":
            return 2
        if stage == "late":
            return 3
        if stage == "severe":
            return 4

        return 2

    def _extract_crop_name(self, label):
        crop_part = label.split("___", 1)[0]
        return crop_part.replace("_", " ").strip().title()

    def _clean_disease_name(self, label):
        disease_part = label.split("___", 1)[-1]
        return disease_part.replace("_", " ").strip().title()

    def predict_structured(self, frame):
        label, confidence = self.predict(frame)
        stage = self._extract_disease_stage(label)
        disease_name = self._clean_disease_name(label)
        has_disease = stage != "healthy" and disease_name.lower() != "healthy"

        return {
            "crop_name": self._extract_crop_name(label),
            "disease_name": disease_name,
            "disease_label": label,
            "disease_stage": stage,
            "disease_level": self._extract_disease_level(stage),
            "has_disease": has_disease,
            "confidence": round(confidence, 4),
            "metric": "probability",
        }