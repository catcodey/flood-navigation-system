import cv2
import numpy as np
import matplotlib.pyplot as plt

def generate_blue_brown_overlay(dem_path, roads_path, output_path="/Users/bbhavna/Desktop/final project code/backend/outputs/blue-brown roads.png"):
    """Overlay road segmentation on DEM and save blue-brown roads."""
    
    # Load the DEM image and convert to RGB
    dem = cv2.imread(dem_path)
    dem = cv2.cvtColor(dem, cv2.COLOR_BGR2RGB)

    # Load road extraction binary image
    roads = cv2.imread(roads_path, cv2.IMREAD_GRAYSCALE)
    if roads is None:
        print("❌ Error: Road image not found!")
        return None

    # Resize roads to match DEM dimensions
    roads = cv2.resize(roads, (dem.shape[1], dem.shape[0]))

    # Convert DEM to HSV for color segmentation
    hsv = cv2.cvtColor(dem, cv2.COLOR_RGB2HSV)

    # Define color ranges
    lower_brown, upper_brown = np.array([10, 50, 50]), np.array([30, 255, 255])
    lower_blue, upper_blue = np.array([90, 50, 50]), np.array([140, 255, 255])

    # Create masks for brown and blue regions
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply road mask
    _, road_mask = cv2.threshold(roads, 200, 255, cv2.THRESH_BINARY)
    roads_rgb = cv2.cvtColor(road_mask, cv2.COLOR_GRAY2RGB)

    # Identify roads overlapping with brown and blue
    roads_on_brown = cv2.bitwise_and(road_mask, brown_mask)
    roads_on_blue = cv2.bitwise_and(road_mask, blue_mask)

    # Get coordinates of road pixels
    brown_road_coords = np.column_stack(np.where(roads_on_brown > 0))
    blue_road_coords = np.column_stack(np.where(roads_on_blue > 0))

    # Define road colors
    brown_color, blue_color = [109, 169, 19], [189, 109, 190]

    # Color detected roads
    for y, x in brown_road_coords:
        roads_rgb[y, x] = brown_color
    for y, x in blue_road_coords:
        roads_rgb[y, x] = blue_color

    # Save the final output
    final_output = cv2.cvtColor(roads_rgb, cv2.COLOR_BGR2RGB)
    cv2.imwrite(output_path, final_output)
    print(f"✅ Blue-Brown Roads saved as '{output_path}'")

    return True
