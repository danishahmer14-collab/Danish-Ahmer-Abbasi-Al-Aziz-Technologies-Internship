# Week 3 — Day 4

## Task(s) Assigned
Introduction to Computer Vision
Images as data
Image preprocessing
Image resizing
Normalization
OpenCV
Image classification
CNN concepts
Convolution
Filters
Pooling
Feature extraction
Object detection overview
Image augmentation
Hands-on:
Load and process images using OpenCV.
Build a basic image classification system.

## What I Did
Firstly, I created my own environment, then I learned how images are represented as data—grids of pixel values (height × width × channels)—and that OpenCV loads color images in a default BGR format. I investigated image pre-processing methods, such as resizing images to a fixed input size and normalizing the pixel values (scaling 0 to 255 down to a small, consistent range) to stabilize training. I wrote a Python script named Tasksw3d4.py, consisting of two parts. For Part 1 (OpenCV), I created a sample image and applied a preprocessing pipeline that included resizing, normalization, grayscale, Gaussian blurring, and Canny edge detection, saving the results side by side for each stage of the pipeline. For Part 2 (Classification), I developed a simple CNN with 2 convolution and max-pooling layers, and 1 fully connected layer to classify the CIFAR-10 dataset. In order to prevent overfitting, the training data was augmented by applying random horizontal flips and random crops to the images. I re-used the workflow from Day 3, except that this time I used the Adam optimizer, dropout, and weight decay, saved the model with the lowest validation loss, and plotted the loss and accuracy curves. I also configured the Python environment for the work, resolving a OneDrive permissions problem by installing packages using python -m pip rather than directly via pip.exe.

## Key Learnings
I familiarized myself with the reason behind CNNs being the preferred architecture for image-related tasks; they are more efficient than fully connected layers for image data because the weights of the convolution layers are invariant across the entire image, detecting local patterns like edges and textures. I understood that pooling (specifically max pooling) makes the feature maps smaller in spatial dimensions by passing on the most active cells, so computation decreases as the network grows deeper. I also understood the distinction between classical feature extraction (e.g., using Canny edge detection in OpenCV) and the automatic feature learning that CNNs achieve in their convolution and pooling layers. I recognized that image augmentation is a form of regularization—similar to dropout, but a way to avoid overfitting by presenting the model with greater visual diversity rather than limiting the network's ability. I gained a bigger understanding of the difference between classification and detection: classification is predicting one label per image, while object detection also involves localizing multiple objects with bounding boxes. Finally, solving a real-life problem in the environment (OneDrive locking pip.exe) served as a reminder that development environment issues are often not due to code, but rather file system or sync conflicts.

## Files in this folder
- `Tasksw3d4.py` — main script: OpenCV preprocessing demo plus a basic CNN image classifier trained on CIFAR-10.
- `opencv_preprocessing_demo.png` — side-by-side visualization of the OpenCV preprocessing steps (resize, grayscale, blur, edges).
- `best_cnn_model.pt` — saved checkpoint of the best-performing CNN model (lowest validation loss) during training.
- `cnn_training_curves.png` — loss and accuracy curves across training epochs.
