import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset, random_split
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

from model import BasicCNN, CIFAR10_MEAN, CIFAR10_STD, CLASS_NAMES

CONFIG = {
    "learning_rate": 0.001,
    "batch_size": 64,
    "epochs": 15,
    "dropout_rate": 0.3,
    "weight_decay": 1e-4,
    "checkpoint_path": "checkpoints/best_model.pt",
}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


# Data + augmentation (train only; val/test stay unaugmented for a fair read)

train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize(CIFAR10_MEAN, CIFAR10_STD),
])
eval_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(CIFAR10_MEAN, CIFAR10_STD),
])

full_train_aug = datasets.CIFAR10(root="./data", train=True, download=True, transform=train_transform)
full_train_eval = datasets.CIFAR10(root="./data", train=True, download=True, transform=eval_transform)
test_set = datasets.CIFAR10(root="./data", train=False, download=True, transform=eval_transform)

train_size = int(0.9 * len(full_train_aug))
val_size = len(full_train_aug) - train_size
train_idx, val_idx = random_split(range(len(full_train_aug)), [train_size, val_size])

train_set = Subset(full_train_aug, train_idx.indices)
val_set = Subset(full_train_eval, val_idx.indices)

train_loader = DataLoader(train_set, batch_size=CONFIG["batch_size"], shuffle=True)
val_loader = DataLoader(val_set, batch_size=CONFIG["batch_size"], shuffle=False)
test_loader = DataLoader(test_set, batch_size=CONFIG["batch_size"], shuffle=False)


# Model, loss, optimizer

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
        torch.save({
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "val_loss": val_loss,
            "val_acc": val_acc,
            "config": CONFIG,
        }, CONFIG["checkpoint_path"])

    flag = " <- checkpoint saved" if improved else ""
    print(f"Epoch {epoch:2d}/{CONFIG['epochs']} | "
          f"train_loss={train_loss:.4f} train_acc={train_acc:.4f} | "
          f"val_loss={val_loss:.4f} val_acc={val_acc:.4f}{flag}")


# Final test evaluation using the best checkpoint

checkpoint = torch.load(CONFIG["checkpoint_path"], map_location=device)
model.load_state_dict(checkpoint["model_state_dict"])
test_loss, test_acc = run_epoch(test_loader, training=False)
print(f"\nBest checkpoint from epoch {checkpoint['epoch']} (val_loss={checkpoint['val_loss']:.4f})")
print(f"Final TEST performance -> loss={test_loss:.4f}, accuracy={test_acc:.4f}")


# Save results: curves + metrics.json (the "Training results" deliverable)

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
plt.savefig("results/training_curves.png", dpi=150)

metrics = {
    "final_test_loss": test_loss,
    "final_test_accuracy": test_acc,
    "best_epoch": checkpoint["epoch"],
    "best_val_loss": checkpoint["val_loss"],
    "best_val_accuracy": checkpoint["val_acc"],
    "config": CONFIG,
    "class_names": CLASS_NAMES,
    "history": history,
}
with open("results/metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("\nSaved results/training_curves.png and results/metrics.json")
print(f"Trained model saved to {CONFIG['checkpoint_path']}")
print("You're ready to run the web app: streamlit run app.py")
