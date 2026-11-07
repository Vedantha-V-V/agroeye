# ============================================================
# AgroEye — Classification Report Generator
# Runs inference on PlantVillage dataset using cached ViT model
# Outputs report to console + classification_report.txt
# Run: python evaluate.py
# ============================================================

import os, glob, time
from pathlib import Path
from datetime import datetime

from PIL import Image
from transformers import pipeline, AutoImageProcessor, AutoModelForImageClassification
from sklearn.metrics import classification_report, accuracy_score
from tqdm import tqdm

# ── Config ────────────────────────────────────────────────────
DATA_DIR     = os.getenv("DATA_DIR","./data/color")
MODEL_NAME   = os.getenv("VIT_MODEL","./finetuned_model")
MODEL_CACHE  = os.getenv("MODEL_CACHE_DIR","./finetuned_model")
REPORT_FILE  = "classification_report.txt"
FRAME_SIZE   = (224, 224)
IMG_EXTS     = ("*.jpg", "*.jpeg", "*.png")

CLASSES = [
    "Potato_Early_blight",
    "Potato_healthy",
    "Potato_Late_blight",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_healthy",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites Two-spotted_spider_mite",
    "Tomato_Target_Spot",
    "Tomato_Tomato_mosaic_virus",
    "Tomato_Tomato_Yellow_Leaf_Curl_Virus",
]

# ── Load model from cache ─────────────────────────────────────
print(f"Loading model: {MODEL_NAME}")
from transformers import AutoImageProcessor, AutoModelForImageClassification

processor = AutoImageProcessor.from_pretrained(MODEL_NAME, cache_dir=MODEL_CACHE)
model     = AutoModelForImageClassification.from_pretrained(MODEL_NAME, cache_dir=MODEL_CACHE)

clf = pipeline(
    "image-classification",
    model=model,
    image_processor=processor,
    device=-1
)
print("Model loaded.\n")

# ── Label map: folder name → model output label ──────────────
LABEL_MAP = {
    "Potato_Early_blight":                          "Potato___Early_Blight",
    "Potato_healthy":                               "Potato___Healthy",
    "Potato_Late_blight":                           "Potato___Late_Blight",
    "Tomato_Bacterial_spot":                        "Tomato___Bacterial_Spot",
    "Tomato_Early_blight":                          "Tomato___Early_Blight",
    "Tomato_healthy":                               "Tomato___Healthy",
    "Tomato_Late_blight":                           "Tomato___Late_Blight",
    "Tomato_Leaf_Mold":                             "Tomato___Leaf_Mold",
    "Tomato_Septoria_leaf_spot":                    "Tomato___Septoria_Leaf_Spot",
    "Tomato_Spider_mites Two-spotted_spider_mite":  "Tomato___Spider_Mites Two-spotted_Spider_Mite",
    "Tomato_Target_Spot":                           "Tomato___Target_Spot",
    "Tomato_Tomato_mosaic_virus":                   "Tomato___Tomato_Mosaic_Virus",
    "Tomato_Tomato_Yellow_Leaf_Curl_Virus":         "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
}

# ── Collect images ────────────────────────────────────────────
samples = []  # (image_path, true_label)
for cls in CLASSES:
    cls_dir = Path(DATA_DIR) / cls
    if not cls_dir.exists():
        print(f"WARNING: folder not found — {cls_dir}")
        continue
    for ext in IMG_EXTS:
        for img_path in cls_dir.glob(ext):
            samples.append((img_path, cls))

print(f"Total images found: {len(samples)}")
if not samples:
    raise RuntimeError(f"No images found in {DATA_DIR}")

# ── Run inference ─────────────────────────────────────────────
y_true, y_pred = [], []
errors = 0

for img_path, true_label in tqdm(samples, desc="Inferring"):
    try:
        img  = Image.open(img_path).convert("RGB").resize(FRAME_SIZE, Image.LANCZOS)
        top  = clf(img, top_k=1)[0]
        # Match predicted label to closest class name
        pred = top["label"]
        y_true.append(true_label)
        y_pred.append(pred)
    except Exception as e:
        errors += 1
        continue

print(f"\nInference complete. Errors skipped: {errors}")

# ── Generate report ───────────────────────────────────────────
# Get union of all labels that actually appeared
all_labels = sorted(set(y_true) | set(y_pred))

report = classification_report(
    y_true, y_pred,
    labels=all_labels,
    zero_division=0
)
acc = accuracy_score(y_true, y_pred)

header = f"""
AgroEye — Classification Report
Model   : {MODEL_NAME}
Dataset : {DATA_DIR}
Classes : {len(CLASSES)}
Images  : {len(samples)}
Errors  : {errors}
Overall Accuracy: {acc:.4f} ({acc*100:.2f}%)
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}
"""

output = header + report

# Console
print(output)

# File
with open(REPORT_FILE, "w") as f:
    f.write(output)

print(f"Report saved to: {REPORT_FILE}")