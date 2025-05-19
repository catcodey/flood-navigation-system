import os
import random
import numpy as np
import matplotlib.pyplot as plt
import cv2
from glob import glob
from PIL import Image

import tensorflow as tf
from sklearn.model_selection import train_test_split

from keras.optimizers import Adam
from keras.metrics import Recall, Precision
from keras import backend as K
from keras.layers import (Input, Conv2D, BatchNormalization,
                          Activation, MaxPool2D, Conv2DTranspose,
                          Concatenate)
from keras.models import Model
from keras.layers import LeakyReLU

smooth = 1e-15

def iou(y_true, y_pred):
    """Intersection over Union."""
    y_pred = tf.cast(y_pred > 0.5, tf.float32)
    intersection = tf.reduce_sum(y_true * y_pred)
    union = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) - intersection
    iou_value = (intersection + smooth) / (union + smooth)
    return tf.ensure_shape(iou_value, shape=())

def soft_dice_coef(y_true, y_pred, smooth=1e-6):
    intersection = tf.reduce_sum(y_true * y_pred)
    denominator = tf.reduce_sum(y_true) + tf.reduce_sum(y_pred)
    return (2. * intersection + smooth) / (denominator + smooth)

def soft_dice_loss(y_true, y_pred):
    return 1.0 - soft_dice_coef(y_true, y_pred)

W, H = 256, 256

def read_image(path):  # image in rgb format but normalised
    """Reads and resizes the input image."""
    try:
        img = Image.open(path)
        img = img.resize((W, H))
        x = np.array(img, dtype=np.float32) / 255.0
        return x
    except Exception as e:
        print(f'Error while reading image: {e}')
        return None

def road_display(road_path,place):
    from tensorflow.keras.models import load_model

    # Import your custom objects
    custom_objects = {
        'soft_dice_loss': soft_dice_loss,
        'soft_dice_coef': soft_dice_coef,
        'iou': iou

    }

    # Load the model
    loaded_model = load_model('//Users/bbhavna/Desktop/final project code/backend/models/v5_road_extraction_beefy_unet (2).h5', custom_objects=custom_objects)


    # Pick a random image from test set or any single image
    if place=="nungambakkam":
        sample_image_path = "/Users/bbhavna/Desktop/final project code/backend/gearthimgs/ngmbkm gearth.jpg"
    elif place=="mahalingapuram":
        sample_image_path = "/Users/bbhavna/Desktop/final project code/backend/gearthimgs/maha.jpg"

    sample_img = read_image(sample_image_path)
    if sample_img is not None:
        sample_img_expanded = np.expand_dims(sample_img, axis=0)
        prediction = loaded_model.predict(sample_img_expanded)[0]
        


        prediction_cv = (prediction.squeeze() * 255).astype(np.uint8)
        cv2.imwrite(road_path, prediction_cv)
        cv2.imwrite("/Users/bbhavna/Desktop/final project code/backend/outputs/predicted_mask_cv.png", prediction_cv)
        
        
        
        print(f"✅ Mask saved as '{road_path}'")
        return True  # ✅ Success
    else:
        print("❌ Error: Could not read sample image.")
        return False  # ❌ Error


"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load images
dem_path = "dem_map.png"  # Replace with actual DEM image path
roads_path = "predicted_mask_cv.png"  # Replace with actual road image path

dem = cv2.imread(dem_path)
roads = cv2.imread(roads_path, cv2.IMREAD_GRAYSCALE)  # Load roads as grayscale

# Resize roads image to match DEM dimensions
roads_resized = cv2.resize(roads, (dem.shape[1], dem.shape[0]))

# Convert roads to a 3-channel image
roads_colored = cv2.cvtColor(roads_resized, cv2.COLOR_GRAY2BGR)

# Define overlay color (e.g., red roads)
roads_colored[roads_resized > 0] = [255, 0, 0]  # Color roads red

# Blend images
alpha = 0.6  # Transparency factor (adjust as needed)
overlay = cv2.addWeighted(dem, 1 - alpha, roads_colored, alpha, 0)

# Display result
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
plt.title("Binary Road Extraction Overlaid on DEM")
plt.axis("off")
plt.show()
"""