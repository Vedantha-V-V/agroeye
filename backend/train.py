# ============================================================
# AgroEye — Model Fine-Tuning
# ============================================================
from transformers import AutoFeatureExtractor, AutoModelForImageClassification, TrainingArguments, Trainer
import torch

# ============================================================
# Configuration
# ============================================================
# --- Dataset Path ---
# Path to the pre-processed dataset created by prepare_dataset.py
PROCESSED_DATA_DIR = 'processed_tomato_leaf_dataset'

# --- Model Configuration ---
BASE_MODEL_NAME = "google/vit-base-patch16-224"
FINETUNED_MODEL_NAME = "finetuned_model"

# --- Training Parameters ---
EPOCHS = 10
BATCH_SIZE = 32
LEARNING_RATE = 2e-5


# ============================================================
# 1. Load Pre-processed Dataset
# ============================================================
print(f"Loading pre-processed dataset from: {PROCESSED_DATA_DIR}")
try:
    train_dataset = torch.load(f"{PROCESSED_DATA_DIR}_train.pt")
    val_dataset = torch.load(f"{PROCESSED_DATA_DIR}_val.pt")
except FileNotFoundError:
    print("\n[Error] Processed dataset not found!")
    print("Please run `python prepare_dataset.py` first to generate the dataset.")
    exit()

# Get the class names and mappings from the loaded dataset
labels = train_dataset.features["label"].names
id2label = {i: label for i, label in enumerate(labels)}
label2id = {label: i for i, label in id2label.items()}
print(f"Found {len(labels)} classes: {labels}")


# ============================================================
# 2. Define Data Collator
# ============================================================
# The data collator is responsible for creating batches of data.
# Since our data is already tensorized, this is straightforward.
def collate_fn(examples):
    pixel_values = torch.stack([example["pixel_values"] for example in examples])
    labels = torch.tensor([example["label"] for example in examples])
    return {"pixel_values": pixel_values, "labels": labels}


# ============================================================
# 3. Load and Configure the Model for Fine-Tuning
# ============================================================
print("Loading pre-trained ViT model for fine-tuning...")
model = AutoModelForImageClassification.from_pretrained(
    BASE_MODEL_NAME,
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id,
    ignore_mismatched_sizes=True, # This is important for transfer learning
)

# We need the feature extractor for the tokenizer, but not for transforms
feature_extractor = AutoFeatureExtractor.from_pretrained(BASE_MODEL_NAME)


# ============================================================
# 4. Define Training Arguments and Trainer
# ============================================================
print("Configuring training...")
training_args = TrainingArguments(
    output_dir=f"./{FINETUNED_MODEL_NAME}",
    per_device_train_batch_size=BATCH_SIZE,
    evaluation_strategy="steps",
    num_train_epochs=EPOCHS,
    fp16=True if torch.cuda.is_available() else False,
    save_steps=100,
    eval_steps=100,
    logging_steps=10,
    learning_rate=LEARNING_RATE,
    save_total_limit=2,
    remove_unused_columns=False,
    push_to_hub=False,
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=collate_fn,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=feature_extractor, # The tokenizer is the feature extractor
)


# ============================================================
# 5. Start Training
# ============================================================
print("Starting fine-tuning...")
trainer.train()

print("\nFine-tuning complete.")
trainer.save_model(FINETUNED_MODEL_NAME)
print(f"Fine-tuned model saved to ./{FINETUNED_MODEL_NAME}")

