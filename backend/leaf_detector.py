import os
from pathlib import Path
from PIL import Image

class LeafDetector:
    """
    Lightweight leaf/foliage presence detector.
    Filters out background frames (bare ground, hands, walls, sky, equipment)
    before sending images to the disease classification model.
    """
    def __init__(self, yolo_path: Path | None = None):
        self.yolo_model = None
        self.yolo_path = yolo_path
        self._init_yolo()

    def _init_yolo(self):
        if self.yolo_path and self.yolo_path.exists():
            try:
                from ultralytics import YOLO
                self.yolo_model = YOLO(str(self.yolo_path))
                print(f"[LEAF DETECTOR] Loaded YOLO model from {self.yolo_path}")
            except Exception as e:
                print(f"[LEAF DETECTOR] YOLO model not active ({e}); using color/texture foliage filter.")

    def check_plant_pixels(self, img: Image.Image) -> tuple[bool, float]:
        """
        Fast plant pixel analysis based on Excess Green Index (ExG)
        and diseased/chlorotic foliar spectral range.
        Operates on an ultra-compact thumbnail (64x64) for instant execution.
        """
        small = img.convert("RGB").resize((64, 64), Image.Resampling.BILINEAR)
        pixels = list(small.getdata())
        total_pixels = len(pixels)
        plant_pixels = 0

        for r, g, b in pixels:
            # 1. Healthy green leaf: Excess Green Index (ExG = 2G - R - B)
            exg = 2 * g - r - b
            if exg > 15 and g > 35:
                plant_pixels += 1
                continue

            # 2. Diseased/yellow-brown leaf tissue (blight, mosaic, rust, chlorosis)
            # High green and red, distinct yellowing ratio above blue
            if r > 45 and g > 40 and (r + g) > (2.1 * (b + 1)) and abs(r - g) < 70:
                plant_pixels += 1
                continue

        ratio = plant_pixels / total_pixels
        # If at least 3.5% of pixels exhibit leaf spectral characteristics
        return ratio >= 0.035, round(ratio, 4)

    def is_leaf_present(self, img: Image.Image) -> tuple[bool, float, str]:
        """
        Returns (has_leaf: bool, confidence/score: float, reason: str).
        """
        has_foliage, ratio = self.check_plant_pixels(img)
        if not has_foliage:
            return False, ratio, "no_foliage_detected"

        # If YOLO object detector is available, check for detected leaf boxes
        if self.yolo_model is not None:
            try:
                results = self.yolo_model.predict(img, conf=0.15, verbose=False)
                if results and len(results) > 0 and len(results[0].boxes) > 0:
                    best_conf = float(results[0].boxes.conf.max().item())
                    return True, round(best_conf, 3), "yolo_leaf_box"
                else:
                    return False, ratio, "yolo_no_leaf_box"
            except Exception:
                pass

        return True, ratio, "foliage_detected"
