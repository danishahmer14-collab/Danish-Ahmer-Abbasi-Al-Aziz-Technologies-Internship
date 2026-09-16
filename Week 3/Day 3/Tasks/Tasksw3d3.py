import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import os

# 1. changed these to experiment Which one is better

CONFIG = {
    "optimizer": "adam",      # "sgd" or "adam"
    "learning_rate": 0.001,
    "batch_size": 64,
    "epochs": 10,
    "dropout_rate": 0.3,
    "weight_decay": 1e-4,      # L2 regularization strength
    "hidden_size": 128,
    "checkpoint_path": "best_model.pt",
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 2. DATA — MNIST handwritten digits, split into train/val/test

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

full_train = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_set = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

# Carve out a validation set from the training data (used to monitor overfitting)
train_size = int(0.9 * len(full_train))
val_size = len(full_train) - train_size
train_set, val_set = random_split(full_train, [train_size, val_size])

train_loader = DataLoader(train_set, batch_size=CONFIG["batch_size"], shuffle=True)
val_loader = DataLoader(val_set, batch_size=CONFIG["batch_size"], shuffle=False)
test_loader = DataLoader(test_set, batch_size=CONFIG["batch_size"], shuffle=False)


# 3. MODEL — a small feedforward network with dropout

class SimpleNN(nn.Module):
    def __init__(self, hidden_size=128, dropout_rate=0.3):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28 * 28, hidden_size)
        self.dropout1 = nn.Dropout(dropout_rate)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.dropout2 = nn.Dropout(dropout_rate)
        self.fc3 = nn.Linear(hidden_size, 10)  # 10 digit classes
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.flatten(x)
        x = self.relu(self.fc1(x))
        x = self.dropout1(x)        # dropout only affects training mode
        x = self.relu(self.fc2(x))
        x = self.dropout2(x)
        x = self.fc3(x)             # raw logits; loss fn applies softmax internally
        return x


model = SimpleNN(CONFIG["hidden_size"], CONFIG["dropout_rate"]).to(device)

# 4. LOSS + OPTIMIZER

criterion = nn.CrossEntropyLoss()  # standard for multi-class classification

if CONFIG["optimizer"] == "sgd":
    optimizer = optim.SGD(
        model.parameters(),
        lr=CONFIG["learning_rate"],
        momentum=0.9,
        weight_decay=CONFIG["weight_decay"],
    )
else:
    optimizer = optim.Adam(
        model.parameters(),
        lr=CONFIG["learning_rate"],
        weight_decay=CONFIG["weight_decay"],
    )


# 5. TRAIN / VALIDATE LOOP HELPERS

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
                loss.backward()      # backpropagation: compute gradients
                optimizer.step()     # optimizer step: update weights

            total_loss += loss.item() * images.size(0)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    return total_loss / total, correct / total


# 6. TRAINING LOOP — with checkpointing

history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}
best_val_loss = float("inf")

for epoch in range(1, CONFIG["epochs"] + 1):
    train_loss, train_acc = run_epoch(train_loader, training=True)
    val_loss, val_acc = run_epoch(val_loader, training=False)

    history["train_loss"].append(train_loss)
    history["val_loss"].append(val_loss)
    history["train_acc"].append(train_acc)
    history["val_acc"].append(val_acc)

    # Save checkpoint only when validation loss improves for best model so far
    improved = val_loss < best_val_loss
    if improved:
        best_val_loss = val_loss
        torch.save({
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "val_loss": val_loss,
            "config": CONFIG,
        }, CONFIG["checkpoint_path"])

    flag = " <- checkpoint saved" if improved else ""
    print(f"Epoch {epoch:2d}/{CONFIG['epochs']} | "
          f"train_loss={train_loss:.4f} train_acc={train_acc:.4f} | "
          f"val_loss={val_loss:.4f} val_acc={val_acc:.4f}{flag}")


# 7. FINAL TEST EVALUATION — load best checkpoint, evaluate once

checkpoint = torch.load(CONFIG["checkpoint_path"], map_location=device)
model.load_state_dict(checkpoint["model_state_dict"])
test_loss, test_acc = run_epoch(test_loader, training=False)
print(f"\nBest checkpoint from epoch {checkpoint['epoch']} "
      f"(val_loss={checkpoint['val_loss']:.4f})")
print(f"Final TEST performance -> loss={test_loss:.4f}, accuracy={test_acc:.4f}")


# 8. VISUALIZATION — loss & accuracy curves

epochs_range = range(1, CONFIG["epochs"] + 1)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(epochs_range, history["train_loss"], label="Train Loss")
axes[0].plot(epochs_range, history["val_loss"], label="Validation Loss")
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Loss")
axes[0].set_title("Loss over Epochs (watch for overfitting gap)")
axes[0].legend()

axes[1].plot(epochs_range, history["train_acc"], label="Train Accuracy")
axes[1].plot(epochs_range, history["val_acc"], label="Validation Accuracy")
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Accuracy")
axes[1].set_title("Accuracy over Epochs")
axes[1].legend()

plt.tight_layout()
plt.savefig("training_curves.png", dpi=150)
print("\nSaved training curves to training_curves.png")
print("Try changing CONFIG (optimizer, learning_rate, dropout_rate, batch_size) and re-run!")