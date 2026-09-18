import cv2
import numpy as np
import torch

from model import CIFAR10_MEAN, CIFAR10_STD


def preprocess_image(image_bgr: np.ndarray) -> torch.Tensor:
    """
    Takes an image as a BGR numpy array (OpenCV's native format) and returns
    a normalized (1, 3, 32, 32) tensor ready for the model.
    """
    # Resize to the model's expected input size
    resized = cv2.resize(image_bgr, (32, 32), interpolation=cv2.INTER_LINEAR)

    # OpenCV loads BGR; the model was trained on RGB (torchvision convention)
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

    # Scale to [0, 1], then standardize per channel
    normalized = rgb.astype(np.float32) / 255.0
    mean = np.array(CIFAR10_MEAN, dtype=np.float32)
    std = np.array(CIFAR10_STD, dtype=np.float32)
    standardized = (normalized - mean) / std

    # HWC -> CHW, add batch dimension
    chw = np.transpose(standardized, (2, 0, 1))
    tensor = torch.from_numpy(chw).unsqueeze(0)
    return tensor


def bytes_to_bgr(file_bytes: bytes) -> np.ndarray:
    """Decodes raw uploaded file bytes into an OpenCV BGR image array."""
    array = np.frombuffer(file_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(array, cv2.IMREAD_COLOR)
    return image_bgr
