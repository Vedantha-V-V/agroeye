# ============================================================
# AgroEye — Dataset Preparation and Augmentation
# ============================================================
from datasets import load_dataset
from transformers import AutoFeatureExtractor
from torchvision.transforms import ToTensor
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
import numpy as np
import torch
import os
from torchvision.utils import save_image

# ============================================================
# Configuration
# ============================================================
# --- Paths ---
# Input: Path to your folder of CROPPED leaf images, organized by class.
RAW_DATA_DIR = 'Tomato Leaf Disease Dataset/TomatoDataset'
# Output: Where to save the processed, augmented dataset.
PROCESSED_DATA_DIR = 'processed_tomato_leaf_dataset'

# --- Model ---
# The feature extractor from the base model determines normalization stats.
BASE_MODEL_NAME = "wambugu71/crop_leaf_diseases_vit"


# ============================================================
# 1. Load Raw Dataset
# ============================================================
def get_subset_indices(dataset, num_samples_per_class=5):
    """Gets indices for a balanced subset of the dataset."""
    indices = []
    # Group indices by class label
    label_to_indices = {label: [] for label in range(len(dataset.features['label'].names))}
    for i, label in enumerate(dataset['label']):
        if len(label_to_indices[label]) < num_samples_per_class:
            label_to_indices[label].append(i)

    # Flatten the list of indices
    for label_indices in label_to_indices.values():
        indices.extend(label_indices)
    
    print(f"Created a subset with {len(indices)} images ({num_samples_per_class} from each of the {len(label_to_indices)} classes).")
    return indices

print(f"Loading raw image data from: {RAW_DATA_DIR}")
# Load the dataset from the image folder
dataset = load_dataset("imagefolder", data_dir=RAW_DATA_DIR, split="train")
dataset = Dataset.from_list(list(dataset))

# --- Create a small subset for presentation ---
subset_indices = get_subset_indices(dataset, num_samples_per_class=5)
dataset = dataset.select(subset_indices)
# ---------------------------------------------

# Split into training and validation sets
dataset = dataset.train_test_split(test_size=0.2, seed=42)
print(f"Dataset split into {len(dataset['train'])} training and {len(dataset['test'])} validation samples.")


# ============================================================
# 2. Define Augmentation and Preprocessing
# ============================================================
print("Setting up data augmentation and preprocessing pipelines...")
feature_extractor = AutoFeatureExtractor.from_pretrained(BASE_MODEL_NAME)
normalize = A.Normalize(mean=feature_extractor.image_mean, std=feature_extractor.image_std)

# Define the transformations for training (with augmentation) and validation (resizing only)
train_transforms = A.Compose(
    [
        A.RandomResizedCrop(height=feature_extractor.size['height'], width=feature_extractor.size['width']),
        A.HorizontalFlip(p=0.5),
        A.Rotate(limit=45, p=0.5),
        A.RandomBrightnessContrast(p=0.5),
        A.MotionBlur(p=0.5),
        A.Perspective(p=0.5),
        A.CoarseDropout(max_holes=8, max_height=8, max_width=8, p=0.5),
        A.GaussNoise(p=0.5),
        A.OneOf([
            A.RandomRain(p=1),
            A.RandomFog(p=1),
            A.RandomSunFlare(p=1),
        ], p=0.5),
        normalize,
        ToTensorV2(),
    ]
)

val_transforms = A.Compose(
    [
        A.Resize(height=feature_extractor.size['height'], width=feature_extractor.size['width']),
        normalize,
        ToTensorV2(),
    ]
)

def apply_train_transforms(examples):
    """Apply augmentation and preprocessing to training examples."""
    images = [np.array(image.convert("RGB")) for image in examples["image"]]
    examples["pixel_values"] = [train_transforms(image=image)["image"] for image in images]
    return examples

def apply_val_transforms(examples):
    """Apply preprocessing to validation examples."""
    images = [np.array(image.convert("RGB")) for image in examples["image"]]
    examples["pixel_values"] = [val_transforms(image=image)["image"] for image in images]
    return examples

# Apply the transformations to the respective splits
# We remove the original 'image' column as it's no longer needed
train_dataset_processed = dataset["train"].map(
    apply_train_transforms,
    batched=True,
    remove_columns=["image"],
    batch_size=32,  # Reduce batch size to lower memory usage
    writer_batch_size=1000,
)
val_dataset_processed = dataset["test"].map(
    apply_val_transforms,
    batched=True,
    remove_columns=["image"],
    batch_size=32,
    writer_batch_size=1000,
)

# Set the format to PyTorch tensors
train_dataset_processed.set_format("torch")
val_dataset_processed.set_format("torch")

print("Data processing complete.")


# ============================================================
# 3. Save Processed Dataset to Disk
# ============================================================
print(f"Saving processed dataset to: {PROCESSED_DATA_DIR}")
# The processed datasets are dictionaries, so we can save them easily
torch.save(train_dataset_processed, f"{PROCESSED_DATA_DIR}_train.pt")
torch.save(val_dataset_processed, f"{PROCESSED_DATA_DIR}_val.pt")

# ============================================================
# 4. Save Sample Augmented Images for Manual Inspection
# ============================================================
print("\nSaving sample augmented images for inspection...")
SAMPLE_SAVE_DIR = 'augmented_samples'
os.makedirs(SAMPLE_SAVE_DIR, exist_ok=True)

# Get mean and std for denormalization
mean = torch.tensor(feature_extractor.image_mean).view(3, 1, 1)
std = torch.tensor(feature_extractor.image_std).view(3, 1, 1)

# --- Define individual augmentations to showcase ---
augmentations_to_showcase = {
    "rotation": A.Rotate(limit=45, p=1),
    "scale_variation": A.RandomResizedCrop(height=feature_extractor.size['height'], width=feature_extractor.size['width'], p=1),
    "brightness_contrast": A.RandomBrightnessContrast(p=1),
    "motion_blur": A.MotionBlur(p=1),
    "perspective": A.Perspective(p=1),
    "occlusion": A.CoarseDropout(max_holes=8, max_height=32, max_width=32, p=1),
    "noise": A.GaussNoise(p=1),
    "weather_rain": A.RandomRain(p=1),
    "weather_fog": A.RandomFog(p=1),
    "weather_sunflare": A.RandomSunFlare(p=1),
}

# --- Get original images to apply augmentations on ---
original_images = [dataset["train"][i]["image"].convert("RGB") for i in range(min(5, len(dataset["train"])))]

# --- Apply and save each augmentation ---
for aug_name, aug_transform in augmentations_to_showcase.items():
    print(f"  - Saving samples for: {aug_name}")
    aug_dir = os.path.join(SAMPLE_SAVE_DIR, aug_name)
    os.makedirs(aug_dir, exist_ok=True)

    # Create a transform pipeline for this specific augmentation
    # We need to convert to numpy array for albumentations, then to tensor
    transform_pipeline = A.Compose([
        aug_transform,
        A.Resize(height=feature_extractor.size['height'], width=feature_extractor.size['width']),
        normalize,
        ToTensorV2()
    ])

    for i, original_image in enumerate(original_images):
        # Albumentations works with numpy arrays
        image_np = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)
        
        # Apply the transformation
        augmented = transform_pipeline(image=image_np)
        image_tensor = augmented['image']

        # Denormalize the image for saving
        denormalized_image = image_tensor.float() * std + mean
        
        # Save the image
        save_path = os.path.join(aug_dir, f"sample_{i+1}.png")
        save_image(denormalized_image, save_path)

print(f"\nSaved sample images to the '{SAMPLE_SAVE_DIR}' directory, organized by augmentation type.")


print("\nDataset preparation finished successfully!")
print(f"Training set saved to: {PROCESSED_DATA_DIR}_train.pt")
print(f"Validation set saved to: {PROCESSED_DATA_DIR}_val.pt")
print("You can now run train.py to start model training.")
