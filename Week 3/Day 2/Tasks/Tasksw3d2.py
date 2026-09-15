import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split

torch.manual_seed(42)
np.random.seed(42)


# use a GPU automatically if one is available, else fall back

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


# 1. Create a small synthetic dataset: two interleaving moon-shaped classes

def make_moons(n_samples=300, noise=0.15):
    n_per_class = n_samples // 2
    theta1 = np.linspace(0, np.pi, n_per_class)
    x1 = np.stack([np.cos(theta1), np.sin(theta1)], axis=1)

    theta2 = np.linspace(0, np.pi, n_per_class)
    x2 = np.stack([1 - np.cos(theta2), 1 - np.sin(theta2) - 0.5], axis=1)

    X = np.vstack([x1, x2]).astype(np.float32)
    X += np.random.normal(scale=noise, size=X.shape).astype(np.float32)
    y = np.array([0] * n_per_class + [1] * n_per_class, dtype=np.int64)

    # shuffle
    idx = np.random.permutation(len(X))
    return X[idx], y[idx]


X, y = make_moons(n_samples=400, noise=0.15)


# 2. Dataset wraps the raw data and defines how to fetch one sample

class MoonsDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.from_numpy(X)          # tensors, the core data structure
        self.y = torch.from_numpy(y)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


full_dataset = MoonsDataset(X, y)

# Train / validation split (80 / 20)
train_size = int(0.8 * len(full_dataset))
val_size = len(full_dataset) - train_size
train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])


# 3. DataLoaders handle batching and shuffling 
batch_size = 16
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)


# 4. Model: subclass nn.Module
#    Input(2) -> Hidden(16, ReLU) -> Hidden(16, ReLU) -> Output(2 classes)

class SimpleNet(nn.Module):
    def __init__(self, input_size=2, hidden_size=16, num_classes=2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_classes),
        )

    def forward(self, x):
        return self.net(x)  # returns raw logits (no softmax here -- the loss does that)


model = SimpleNet().to(device)
print(model)

# 5. Loss function and optimizer

criterion = nn.CrossEntropyLoss()              # combines log-softmax + NLL loss
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 6. Training loop + validation loop

def evaluate(loader):
    """Validation loop: no gradient tracking, model in eval mode."""
    model.eval()
    total_loss, correct, total = 0.0, 0, 0
    with torch.no_grad():
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            logits = model(xb)
            loss = criterion(logits, yb)
            total_loss += loss.item() * xb.size(0)
            preds = logits.argmax(dim=1)
            correct += (preds == yb).sum().item()
            total += xb.size(0)
    return total_loss / total, correct / total


epochs = 50
history = {"train_loss": [], "val_loss": [], "val_acc": []}

for epoch in range(epochs):
    model.train()  # training mode (matters for layers like dropout/batchnorm)
    running_loss = 0.0

    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)

        optimizer.zero_grad()        # clear gradients from the previous step
        logits = model(xb)           # forward pass
        loss = criterion(logits, yb) # compute loss
        loss.backward()              # backpropagation (autograd computes gradients)
        optimizer.step()             # gradient descent update

        running_loss += loss.item() * xb.size(0)

    train_loss = running_loss / train_size
    val_loss, val_acc = evaluate(val_loader)

    history["train_loss"].append(train_loss)
    history["val_loss"].append(val_loss)
    history["val_acc"].append(val_acc)

    if epoch % 5 == 0 or epoch == epochs - 1:
        print(f"Epoch {epoch:3d} | Train Loss: {train_loss:.4f} | "
              f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2%}")


# 7. Saving and loading the model

save_path = "simple_net.pt"
torch.save(model.state_dict(), save_path)
print(f"\nModel saved to {save_path}")

# Demonstrate loading it back into a fresh model instance
loaded_model = SimpleNet().to(device)
loaded_model.load_state_dict(torch.load(save_path, map_location=device))
loaded_model.eval()

val_loss, val_acc = evaluate(val_loader)
print(f"Reloaded model -> Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2%}")


# 8. Optional: plot training curves and decision boundary

try:
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    axes[0].plot(history["train_loss"], label="Train Loss")
    axes[0].plot(history["val_loss"], label="Val Loss")
    axes[0].set_title("Loss over Epochs")
    axes[0].set_xlabel("Epoch")
    axes[0].legend()

    # Decision boundary
    xx, yy = np.meshgrid(
        np.linspace(X[:, 0].min() - 0.5, X[:, 0].max() + 0.5, 200),
        np.linspace(X[:, 1].min() - 0.5, X[:, 1].max() + 0.5, 200),
    )
    grid = torch.from_numpy(np.c_[xx.ravel(), yy.ravel()].astype(np.float32)).to(device)
    with torch.no_grad():
        preds = model(grid).argmax(dim=1).cpu().numpy().reshape(xx.shape)

    axes[1].contourf(xx, yy, preds, alpha=0.3, cmap="coolwarm")
    axes[1].scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm", edgecolors="k", s=15)
    axes[1].set_title("Learned Decision Boundary")

    plt.tight_layout()
    plt.savefig("pytorch_training_curves.png")
    print("Saved plots to pytorch_training_curves.png")
except ImportError:
    pass