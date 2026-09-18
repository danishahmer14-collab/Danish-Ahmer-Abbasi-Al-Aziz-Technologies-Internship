# Week 3 — Day 5

## Task(s) Assigned
Complete Week 3 Revision Review:
Neural networks
Deep learning
PyTorch
Tensors
Training loops
Loss functions
Optimizers
Overfitting
CNNs
OpenCV
Image classification
Friday Deliverables:
Trained model
Working application
GitHub repository
README.md
Training results
Project demonstration

## What I Did
Firstly, I designed my own environment and then combined all the work from Week 3 (Days 1-4) into one end-to-end Capstone Project: a CIFAR-10 image classifier with a live web app. I organized the project as a clean repository with separated concerns: model.py for the CNN model, shared between training and inference to ensure they always stay in sync; utils.py for OpenCV-based image preprocessing (resizing, converting BGR to RGB, normalization) of the images uploaded to the web app; train.py for the full training pipeline, including data loading, augmentation, training/validation loops, checkpointing, and results export; and app.py for a Streamlit web app to make live predictions. I included the setup and dependencies in a requirements.txt file and addressed some setup problems from last week. To prevent overfitting, I applied data augmentation (random flips and crops), dropout, and weight decay when training the CNN for 15 epochs on the CIFAR-10 dataset. I then verified that the deliverables were correctly created, including the trained model (checkpoints/best_model.pt), training curves (results/training_curves.png), and training metrics (results/metrics.json). I tested the live web app by launching app.py using Streamlit and uploading sample images, which successfully displayed the predictions and confidence scores. Finally, I created and completed the README.md file.

## Key Learnings
seeing all these concepts come together in one project was a major highlight: tensors, the training loop, loss/optimizers, and overfitting control were all integrated into train.py rather than existing as isolated ideas. I realized the importance of keeping the model file (model.py) separate from the web app (app.py) and training script (train.py); in real projects, the web app and the training script should never use different model definitions. I also learned that consistent preprocessing is essential—the app must resize and normalize incoming images in the exact same way it was done during training; otherwise, the predictions will be meaningless. This project demonstrated that training curves and validation metrics are not just for reporting, but are actual signals indicating whether the model fits the data too well and whether the saved checkpoint is reliable. I gained practical experience taking a trained model and making it useful and tangible through a live app, rather than just printing out accuracy numbers—a major part of what constitutes an ML project being truly "done." Overall, I participated in the entire project workflow, ranging from environment setup and training to packaging a GitHub-ready repository with full documentation.

## Files in this folder
- `model.py` — CNN architecture definition (2 conv+pool blocks + fully connected classifier head).
- `utils.py` — OpenCV image preprocessing utilities used by the web app.
- `train.py` — training script; produces the trained model and training results.
- `app.py` — Streamlit web application for live image classification.
- `requirements.txt` — project dependencies.
- `checkpoints/best_model.pt` — trained model weights (best validation loss checkpoint).
- `results/training_curves.png` — loss and accuracy curves across training epochs.
- `results/metrics.json` — final test accuracy/loss and training configuration.
- `ProjectPresentation.ppt` Contains presentation of my project.
