# Week 3 — Day 3

## Task(s) Assigned
Training workflow
Loss calculation
Optimizers
SGD
Adam
Learning rate
Epochs
Batch processing
Validation
Overfitting
Dropout
Regularization
Model checkpoints
Training visualization
Hands-on:
Train and evaluate a neural network.
Experiment with different parameters.

## What I Did
I used a Python virtual environment (venv) in VS Code to isolate the project requirements and installed the torch, torchvision, and matplotlib libraries. In a script named Tasksw3d3.py, I implemented the full workflow for neural network training in PyTorch. First, I read and partitioned the MNIST dataset into training, validation, and test sets. Next, I implemented a feed-forward neural network consisting of two layers with 128 units each, utilizing ReLU activation and a dropout rate of 0.3 for regularization. For the training setup, I used CrossEntropyLoss as the loss function and the Adam optimizer (with a learning rate of 0.001 and a weight decay of 1e-4 for L2 regularization). I trained the model for 10 epochs with a batch size of 64, running on the CPU, and tracked the training and validation loss and accuracy after every epoch. To ensure I retained the best-performing model, I set up automatic checkpointing to save best_model.pt whenever the validation loss decreased. Finally, I ran the script end-to-end and monitored the training progress directly in the terminal.

## Key Learnings
I watched the training and validation loss go down steadily with epochs (at epoch 6, the train loss was 0.3778 and the validation loss was 0.1553), and the validation accuracy increased from 95.2% to 97.9%—an indication that the model is learning and generalizing so far without overfitting. I acknowledged the importance of dropout and weight decay, specifically how they keep the gap between training and validation performance small. I also learned that model checkpointing is not just a "nice to have," because saving a checkpoint only when the validation loss improves helps avoid retaining a worse model if the network starts to overfit later in the training process. Additionally, I noted how directly the optimizer (Adam, in this case) determines the speed and smoothness of the loss decrease. Finally, I learned how to set up a clean, isolated Python environment and troubleshooted a couple of real-life setup problems (like a typo in the venv command and a hang in pip/ensurepip)—skills that are very useful beyond just machine learning!

## Files in this folder
- `Tasksw3d3.py` — main training script: builds, trains, and evaluates the neural network on MNIST, with configurable optimizer/learning rate/dropout/batch size.
- `best_model.pt` — saved checkpoint of the best-performing model (lowest validation loss) during training.
- `training_curves.png` -Contains Saved training curves as png.
