import numpy as np

np.random.seed(42)


# 1. Activation functions and their derivatives (needed for backprop)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(a):
    # a is the already-computed sigmoid output: sigmoid'(x) = a * (1 - a)
    return a * (1 - a)


def relu(x):
    return np.maximum(0, x)


def relu_derivative(x):
    return (x > 0).astype(float)


# 2. Data: XOR problem
#    input layer size = 2, output layer size = 1
X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])          # 4 samples, 2 features each

y = np.array([[0],
              [1],
              [1],
              [0]])             # XOR labels

# 3. Network architecture
#    Input(2) to Hidden(4, Sigmoid) to  Output(1, Sigmoid)
input_size = 2
hidden_size = 4
output_size = 1

# Weights & biases are the LEARNABLE PARAMETERS.
# Small random init breaks symmetry so neurons learn different things.
W1 = np.random.randn(input_size, hidden_size)          # weights: input -> hidden
b1 = np.zeros((1, hidden_size))                        # bias for hidden layer
W2 = np.random.randn(hidden_size, output_size)          # weights: hidden -> output
b2 = np.zeros((1, output_size))                        # bias for output layer

# 4. Forward propagation
def forward(X):
    z1 = X @ W1 + b1        # weighted sum into hidden layer
    a1 = sigmoid(z1)         # activation (see note above on ReLU vs Sigmoid here)
    z2 = a1 @ W2 + b2        # weighted sum into output layer
    a2 = sigmoid(z2)         # Sigmoid activation -> probability output
    cache = (z1, a1, z2, a2)
    return a2, cache

# 5. Loss function: Binary Cross-Entropy
def compute_loss(y_true, y_pred):
    eps = 1e-8  # avoid log(0)
    return -np.mean(y_true * np.log(y_pred + eps) +
                     (1 - y_true) * np.log(1 - y_pred + eps))

# 6. Backpropagation: compute how much each weight/bias contributed to loss

def backward(X, y, cache):
    z1, a1, z2, a2 = cache
    m = X.shape[0]  # batch size

    # dL/dz2 for BCE loss + sigmoid output simplifies nicely to (a2 - y)
    dz2 = (a2 - y) / m
    dW2 = a1.T @ dz2
    db2 = np.sum(dz2, axis=0, keepdims=True)

    da1 = dz2 @ W2.T
    dz1 = da1 * sigmoid_derivative(a1)  # chain rule through the hidden activation
    dW1 = X.T @ dz1
    db1 = np.sum(dz1, axis=0, keepdims=True)

    return dW1, db1, dW2, db2

# 7. Training loop: gradient descent over epochs
learning_rate = 1.0
epochs = 10000
batch_size = 4  # here it's the whole dataset ("full-batch" gradient descent)

loss_history = []

for epoch in range(epochs):
    # --- forward pass ---
    y_pred, cache = forward(X)
    loss = compute_loss(y, y_pred)
    loss_history.append(loss)

    # --- backward pass (compute gradients) ---
    dW1, db1, dW2, db2 = backward(X, y, cache)

    # --- gradient descent update ---
    W1 -= learning_rate * dW1
    b1 -= learning_rate * db1
    W2 -= learning_rate * dW2
    b2 -= learning_rate * db2

    if epoch % 1000 == 0:
        print(f"Epoch {epoch:5d} | Loss: {loss:.4f}")

# 8. Results

print("\nFinal predictions after training:")
final_preds, _ = forward(X)
for inputs, true_label, pred in zip(X, y, final_preds):
    print(f"Input: {inputs} | True: {true_label[0]} | "
          f"Predicted: {pred[0]:.4f} -> {round(pred[0])}")

