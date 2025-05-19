import os
import time
import matplotlib.pyplot as plt
from ultralytics import YOLO
import cv2

def flood_seg_yolo(place):
    # Initialize the YOLO model
    model = YOLO("/Users/bbhavna/Desktop/final project code/backend/models/best (4) (1).pt")

    # Determine the image path based on the place
    if place == "nungambakkam":
        image_path = "/Users/bbhavna/Desktop/final project code/backend/flood images/ngm flood.jpg"
    elif place == "mahalingapuram":
        image_path = "//Users/bbhavna/Desktop/final project code/backend/flood images/maha flood.jpg"
    else:
        print(f"Error: No image found for place '{place}'")
        return  # Exit function instead of using exit()

    # Ensure output directory exists
    output_folder = "/Users/bbhavna/Desktop/final project code/backend/outputs"
    os.makedirs(output_folder, exist_ok=True)

    # Run prediction
    st = time.time()
    results = model.predict(source=image_path, save=True, conf=0.6)

    for result in results:
        # Get the image with bounding boxes
        img_with_boxes = result.plot()

        # Define output path (fixed filename)
        output_path = os.path.join(output_folder, "floodoutput.jpg")

        # Save the output image
        cv2.imwrite(output_path, cv2.cvtColor(img_with_boxes, cv2.COLOR_RGB2BGR))

       

    print(f"Processed {place} image in {time.time() - st:.2f} seconds")
    print(f"Saved output image to {output_path}")
    return True

# Example usage
