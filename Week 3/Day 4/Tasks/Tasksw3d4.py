import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

# PART 1 — OpenCV: Load and Process Images

print("=" * 60)
print("PART 1: OpenCV image preprocessing demo")
print("=" * 60)


synthetic_img = np.zeros((200, 300, 3), dtype=np.uint8)
cv2.rectangle(synthetic_img, (30, 30), (150, 150), (0, 140, 255), -1)   # filled rectangle (BGR)
cv2.circle(synthetic_img, (220, 100), 60, (255, 100, 0), -1)            # filled circle
cv2.putText(synthetic_img, "CV Demo", (60, 190), cv2.FONT_HERSHEY_SIMPLEX,
            0.8, (255, 255, 255), 2)

#  Resizing 
resized = cv2.resize(synthetic_img, (128, 128), interpolation=cv2.INTER_LINEAR)
print(f"Original shape: {synthetic_img.shape} -> Resized shape: {resized.shape}")

#  Normalization (min-max to [0, 1]) 
normalized = resized.astype(np.float32) / 255.0
print(f"Pixel range before normalization: [{resized.min()}, {resized.max()}]")
print(f"Pixel range after normalization:  [{normalized.min():.2f}, {normalized.max():.2f}]")

# --- Grayscale conversion ---
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

# --- Blurring (noise reduction / smoothing) ---
blurred = cv2.GaussianBlur(resized, (7, 7), 0)

# --- Edge detection (classical feature extraction) ---
edges = cv2.Canny(gray, threshold1=50, threshold2=150)

# Save a side-by-side comparison so you can see every step
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
titles = ["Resized (BGR->RGB)", "Grayscale", "Gaussian Blur", "Canny Edges"]
images = [
    cv2.cvtColor(resized, cv2.COLOR_BGR2RGB),
    gray,
    cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB),
    edges,
]
cmaps = [None, "gray", None, "gray"]
for ax, title, img, cmap in zip(axes, titles, images, cmaps):
    ax.imshow(img, cmap=cmap)
    ax.set_title(title)
    ax.axis("off")
plt.tight_layout()
plt.savefig("opencv_preprocessing_demo.png", dpi=150)
print("Saved OpenCV preprocessing demo to opencv_preprocessing_demo.png\n")


# PART 2 — Basic Image Classification System (CNN on CIFAR-10)

print("=" * 60)
print("PART 2: Training a basic CNN image classifier")
print("=" * 60)

CONFIG = {
    "learning_rate": 0.001,
    "batch_size": 64,
    "epochs": 8,
    "dropout_rate": 0.3,
    "weight_decay": 1e-4,
    "checkpoint_path": "best_cnn_model.pt",
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

CLASS_NAMES = ["airplane", "automobile", "bird", "cat", "deer",
               "dog", "frog", "horse", "ship", "truck"]


train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616)),
])
eval_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616)),
])

full_train = datasets.CIFAR10(root="./data", train=True, download=True, transform=train_transform)
# Separate copy with eval transform for the validation split (no augmentation on val data)
full_train_eval = datasets.CIFAR10(root="./data", train=True, download=True, transform=eval_transform)
test_set = datasets.CIFAR10(root="./data", train=False, download=True, transform=eval_transform)

train_size = int(0.9 * len(full_train))
val_size = len(full_train) - train_size
train_indices, val_indices = random_split(range(len(full_train)), [train_size, val_size])

train_set = torch.utils.data.Subset(full_train, train_indices.indices)
val_set = torch.utils.data.Subset(full_train_eval, val_indices.indices)

train_loader = DataLoader(train_set, batch_size=CONFIG["batch_size"], shuffle=True)
val_loader = DataLoader(val_set, batch_size=CONFIG["batch_size"], shuffle=False)
test_loader = DataLoader(test_set, batch_size=CONFIG["batch_size"], shuffle=False)


#  A basic CNN Model
class BasicCNN(nn.Module):
    def __init__(self, dropout_rate=0.3):
        super().__init__()
        # Feature extraction: Conv -> ReLU -> Pool, twice
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)  # halves spatial size each time
        self.relu = nn.ReLU()

        # After two 2x2 pools: 32x32 -> 16x16 -> 8x8, with 64 channels
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(64 * 8 * 8, 256)
        self.dropout = nn.Dropout(dropout_rate)
        self.fc2 = nn.Linear(256, 10)  # 10 CIFAR-10 classes

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))   # feature map 1
        x = self.pool(self.relu(self.conv2(x)))   # feature map 2
        x = self.flatten(x)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x


model = BasicCNN(CONFIG["dropout_rate"]).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=CONFIG["learning_rate"],
                        weight_decay=CONFIG["weight_decay"])


def run_epoch(loader, training: bool):
    model.train() if training else model.eval()
    total_loss, correct, total = 0.0, 0, 0
    context = torch.enable_grad() if training else torch.no_grad()
    with context:
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            if training:
                optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            if training:
                loss.backward()
                optimizer.step()
            total_loss += loss.item() * images.size(0)
            correct += (outputs.argmax(dim=1) == labels).sum().item()
            total += labels.size(0)
    return total_loss / total, correct / total


# Training loop with checkpointing 
history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}
best_val_loss = float("inf")

for epoch in range(1, CONFIG["epochs"] + 1):
    train_loss, train_acc = run_epoch(train_loader, training=True)
    val_loss, val_acc = run_epoch(val_loader, training=False)

    history["train_loss"].append(train_loss)
    history["val_loss"].append(val_loss)
    history["train_acc"].append(train_acc)
    history["val_acc"].append(val_acc)

    improved = val_loss < best_val_loss
    if improved:
        best_val_loss = val_loss
        torch.save({"epoch": epoch, "model_state_dict": model.state_dict(),
                    "val_loss": val_loss, "config": CONFIG}, CONFIG["checkpoint_path"])

    flag = " <- checkpoint saved" if improved else ""
    print(f"Epoch {epoch:2d}/{CONFIG['epochs']} | "
          f"train_loss={train_loss:.4f} train_acc={train_acc:.4f} | "
          f"val_loss={val_loss:.4f} val_acc={val_acc:.4f}{flag}")

#  Final test evaluation using the best checkpoint 
checkpoint = torch.load(CONFIG["checkpoint_path"], map_location=device)
model.load_state_dict(checkpoint["model_state_dict"])
test_loss, test_acc = run_epoch(test_loader, training=False)
print(f"\nBest checkpoint from epoch {checkpoint['epoch']} (val_loss={checkpoint['val_loss']:.4f})")
print(f"Final TEST performance -> loss={test_loss:.4f}, accuracy={test_acc:.4f}")

# Visualization 
epochs_range = range(1, CONFIG["epochs"] + 1)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].plot(epochs_range, history["train_loss"], label="Train Loss")
axes[0].plot(epochs_range, history["val_loss"], label="Validation Loss")
axes[0].set_xlabel("Epoch"); axes[0].set_ylabel("Loss")
axes[0].set_title("Loss over Epochs"); axes[0].legend()

axes[1].plot(epochs_range, history["train_acc"], label="Train Accuracy")
axes[1].plot(epochs_range, history["val_acc"], label="Validation Accuracy")
axes[1].set_xlabel("Epoch"); axes[1].set_ylabel("Accuracy")
axes[1].set_title("Accuracy over Epochs"); axes[1].legend()

plt.tight_layout()
plt.savefig("cnn_training_curves.png", dpi=150)
print("\nSaved training curves to cnn_training_curves.png")
print("Try changing CONFIG or the CNN architecture (filters, kernel size, pooling) and re-run!")