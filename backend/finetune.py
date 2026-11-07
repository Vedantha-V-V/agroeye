# ============================================================
# AgroEye — ViT Fine-tuning on PlantVillage (CPU safe)
# Dataset : ./data/color  (class-named subfolders)
# Output  : ./finetuned_model/
# Run     : python finetune.py
# ============================================================

import os, time
from pathlib import Path
from datetime import datetime

import torch
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision import transforms
from PIL import Image
from transformers import (
    ViTForImageClassification,
    ViTImageProcessor,
    get_linear_schedule_with_warmup,
)
from torch.optim import AdamW
from sklearn.metrics import classification_report, accuracy_score
from tqdm import tqdm

# ── Config ────────────────────────────────────────────────────
DATA_DIR      = os.getenv("DATA_DIR",        "./data/color")
OUTPUT_DIR    = os.getenv("OUTPUT_DIR",      "./finetuned_model")
BASE_MODEL    = "google/vit-base-patch16-224"
EPOCHS        = 3
BATCH_SIZE    = 8       # safe for 16GB RAM on CPU
LR            = 2e-5
VAL_SPLIT     = 0.2
MAX_PER_CLASS = 400     # cap per class — keeps runtime under 4hrs on CPU
IMG_EXTS      = (".jpg", ".jpeg", ".png")
SEED          = 42

torch.manual_seed(SEED)

# ── Discover classes ──────────────────────────────────────────
data_path = Path(DATA_DIR)
classes   = sorted([d.name for d in data_path.iterdir() if d.is_dir()])
cls2idx   = {c: i for i, c in enumerate(classes)}
idx2cls   = {i: c for c, i in cls2idx.items()}
print(f"Classes found ({len(classes)}):")
for c in classes:
    print(f"  {c}")

# ── Dataset ───────────────────────────────────────────────────
processor = ViTImageProcessor.from_pretrained(BASE_MODEL)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=processor.image_mean, std=processor.image_std),
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=processor.image_mean, std=processor.image_std),
])


class PlantDataset(Dataset):
    def __init__(self, samples, transform):
        self.samples   = samples
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = Image.open(path).convert("RGB")
        return self.transform(img), label


# Collect samples (capped per class)
all_samples = []
for cls in classes:
    imgs = []
    for ext in IMG_EXTS:
        imgs += list((data_path / cls).glob(f"*{ext}"))
    imgs = imgs[:MAX_PER_CLASS]
    all_samples += [(p, cls2idx[cls]) for p in imgs]

print(f"\nTotal samples: {len(all_samples)}")

# Train / val split
val_size   = int(len(all_samples) * VAL_SPLIT)
train_size = len(all_samples) - val_size
train_raw, val_raw = random_split(all_samples, [train_size, val_size],
                                  generator=torch.Generator().manual_seed(SEED))

train_ds = PlantDataset(list(train_raw), transform)
val_ds   = PlantDataset(list(val_raw),   val_transform)

train_dl = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=0)
val_dl   = DataLoader(val_ds,   batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

print(f"Train: {len(train_ds)} | Val: {len(val_ds)}")

# ── Model ─────────────────────────────────────────────────────
print(f"\nLoading base model: {BASE_MODEL}")
model = ViTForImageClassification.from_pretrained(
    BASE_MODEL,
    num_labels=len(classes),
    id2label=idx2cls,
    label2id=cls2idx,
    ignore_mismatched_sizes=True,
)
model.train()

# ── Optimizer + scheduler ─────────────────────────────────────
optimizer = AdamW(model.parameters(), lr=LR)
total_steps = len(train_dl) * EPOCHS
scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=total_steps // 10,
    num_training_steps=total_steps
)

# ── Training loop ─────────────────────────────────────────────
print(f"\nStarting fine-tuning — {EPOCHS} epochs on CPU")
print(f"ETA: ~2-4 hours. Started at {datetime.now().strftime('%H:%M:%S')}\n")

for epoch in range(EPOCHS):
    model.train()
    total_loss, correct, total = 0, 0, 0
    loop = tqdm(train_dl, desc=f"Epoch {epoch+1}/{EPOCHS}")

    for imgs, labels in loop:
        optimizer.zero_grad()
        outputs = model(pixel_values=imgs, labels=labels)
        loss    = outputs.loss
        loss.backward()
        optimizer.step()
        scheduler.step()

        total_loss += loss.item()
        preds       = outputs.logits.argmax(-1)
        correct    += (preds == labels).sum().item()
        total      += labels.size(0)
        loop.set_postfix(loss=f"{loss.item():.4f}",
                         acc=f"{correct/total:.3f}")

    # ── Validation ────────────────────────────────────────────
    model.eval()
    y_true, y_pred = [], []
    with torch.no_grad():
        for imgs, labels in tqdm(val_dl, desc="Validating"):
            outputs = model(pixel_values=imgs)
            preds   = outputs.logits.argmax(-1)
            y_true.extend(labels.tolist())
            y_pred.extend(preds.tolist())

    val_acc = accuracy_score(y_true, y_pred)
    print(f"\nEpoch {epoch+1} — Val Accuracy: {val_acc:.4f} ({val_acc*100:.2f}%)\n")

# ── Save model ────────────────────────────────────────────────
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
model.save_pretrained(OUTPUT_DIR)
processor.save_pretrained(OUTPUT_DIR)
print(f"Model saved to: {OUTPUT_DIR}")

# ── Final classification report ───────────────────────────────
report = classification_report(y_true, y_pred,
                                target_names=[idx2cls[i] for i in range(len(classes))],
                                zero_division=0)
acc    = accuracy_score(y_true, y_pred)

header = f"""
AgroEye — Fine-tuned Classification Report
Base Model : {BASE_MODEL}
Dataset    : {DATA_DIR}
Classes    : {len(classes)}
Epochs     : {EPOCHS}
Val Accuracy: {acc:.4f} ({acc*100:.2f}%)
Generated  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}
"""
output = header + report
print(output)

with open("finetuned_classification_report.txt", "w") as f:
    f.write(output)
print("Report saved to: finetuned_classification_report.txt")