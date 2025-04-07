import os
import App
from tkinter import filedialog
import customtkinter
import numpy as np
from PIL import Image
from scipy import ndimage

def convolve_image(matrix, pil_image):
    # Convert PIL to NumPy array (auto-handles RGB/grayscale)
    img_array = np.array(pil_image, dtype=np.float32)  # Avoid integer overflow
    
    # Normalize kernel to sum=1 (prevent brightness change)
    kernel = np.array(matrix, dtype=np.float32)
    kernel /= kernel.sum() if kernel.sum() != 0 else 1
    
    if img_array.ndim == 2:  # Grayscale
        convolved = ndimage.convolve(img_array, kernel)
        
    elif img_array.ndim == 3:  # RGB
        convolved = np.zeros_like(img_array)
        for c in range(img_array.shape[2]):
            convolved[..., c] = ndimage.convolve(
                img_array[..., c], kernel
            )
    else:
        raise ValueError("Unsupported image format")
    
    # Clip and convert back to PIL
    convolved = np.clip(convolved, 0, 255).astype(np.uint8)
    return Image.fromarray(convolved)