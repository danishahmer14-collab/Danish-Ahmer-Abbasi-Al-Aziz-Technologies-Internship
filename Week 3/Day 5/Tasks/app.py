import json
import os

import numpy as np
import streamlit as st
import torch
import torch.nn.functional as F

from model import BasicCNN, CLASS_NAMES
from utils import bytes_to_bgr, preprocess_image

CHECKPOINT_PATH = "checkpoints/best_model.pt"

st.set_page_config(page_title="CIFAR-10 Image Classifier", page_icon="🖼️", layout="centered")
st.title("🖼️ CIFAR-10 Image Classifier")
st.write(
    "Upload an image and this CNN will predict which of 10 categories it "
    "belongs to: " + ", ".join(CLASS_NAMES) + "."
)


@st.cache_resource
def load_model():
    if not os.path.exists(CHECKPOINT_PATH):
        return None, None
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(CHECKPOINT_PATH, map_location=device)
    model = BasicCNN(dropout_rate=checkpoint["config"]["dropout_rate"])
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()
    return model, device


model, device = load_model()

if model is None:
    st.error(
        f"No trained model found at `{CHECKPOINT_PATH}`. "
        "Run `python train.py` first to train and save the model."
    )
    st.stop()

# Show training results in the sidebar if available
if os.path.exists("results/metrics.json"):
    with open("results/metrics.json") as f:
        metrics = json.load(f)
    st.sidebar.header("Model Performance")
    st.sidebar.metric("Test Accuracy", f"{metrics['final_test_accuracy']*100:.1f}%")
    st.sidebar.metric("Test Loss", f"{metrics['final_test_loss']:.4f}")
    if os.path.exists("results/training_curves.png"):
        st.sidebar.image("results/training_curves.png", caption="Training curves")

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    image_bgr = bytes_to_bgr(file_bytes)

    if image_bgr is None:
        st.error("Could not read that image — try a different file.")
    else:
        st.image(file_bytes, caption="Uploaded image", use_column_width=True)

        tensor = preprocess_image(image_bgr).to(device)
        with torch.no_grad():
            logits = model(tensor)
            probabilities = F.softmax(logits, dim=1)[0].cpu().numpy()

        top_idx = int(np.argmax(probabilities))
        st.subheader(f"Prediction: **{CLASS_NAMES[top_idx]}**")
        st.write(f"Confidence: {probabilities[top_idx]*100:.1f}%")

        st.write("All class probabilities:")
        prob_dict = {CLASS_NAMES[i]: float(probabilities[i]) for i in range(len(CLASS_NAMES))}
        st.bar_chart(prob_dict)
