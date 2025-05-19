import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
from collections import deque


# === Function to find the shortest path using BFS ===
def bfs_find_path(road_img, start, end):
    rows, cols, _ = road_img.shape
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    queue = deque([start])
    visited = set()
    parent_map = {}

    while queue:
        curr = queue.popleft()
        if curr == end:
            path = []
            while curr in parent_map:
                path.append(curr)
                curr = parent_map[curr]
            path.append(start)
            return path[::-1]

        if curr in visited:
            continue
        visited.add(curr)

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = curr[0] + dx, curr[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and np.any(road_img[nx, ny] > 0) and (nx, ny) not in visited:
                queue.append((nx, ny))
                parent_map[(nx, ny)] = curr

    return None  # No path found

# === Function to find the nearest brown point ===
def find_nearest_brown(start_point, brown_coords):
    min_dist = float("inf")
    nearest_point = None

    for pt in brown_coords:
        dist = np.sqrt((pt[0] - start_point[0]) ** 2 + (pt[1] - start_point[1]) ** 2)
        if dist < min_dist:
            min_dist = dist
            nearest_point = tuple(pt)

    return nearest_point,dist

# === Function to check if a point is far enough from previously selected points ===
def is_far_enough(point, selected_points, min_dist_threshold=100):
    for prev_point in selected_points:
        dist = np.sqrt((prev_point[0] - point[0]) ** 2 + (prev_point[1] - point[1]) ** 2)
        if dist < min_dist_threshold:
            return False
    return True

def generate_shortest_path(input_path,output_path):
    
    sta=time.time()
    FILE_PATH="/Users/bbhavna/Desktop/final project code/backend/path_lengths.txt"

    # === Define colors in RGB ===
    brown_rgb = np.uint8([[[109, 169, 19]]])  # Brown
    blue_rgb = np.uint8([[[189, 109, 190]]])  # Blue

    # === Convert to HSV ===
    brown_hsv = cv2.cvtColor(brown_rgb, cv2.COLOR_RGB2HSV)[0][0]
    blue_hsv = cv2.cvtColor(blue_rgb, cv2.COLOR_RGB2HSV)[0][0]

    print(f"Brown HSV: {brown_hsv}")
    print(f"Blue HSV: {blue_hsv}")

    # Define HSV color ranges
    lower_brown = np.array([brown_hsv[0] - 10, 50, 50])
    upper_brown = np.array([brown_hsv[0] + 10, 255, 255])

    lower_blue = np.array([blue_hsv[0] - 20, 50, 50])  # Widen the range
    upper_blue = np.array([blue_hsv[0] + 20, 255, 255])

    # === Load the binary road extraction image ===
    road_img = cv2.imread(input_path)  # Replace with actual file path
    road_img = cv2.cvtColor(road_img, cv2.COLOR_BGR2RGB)

    # Convert image to HSV for color segmentation
    hsv = cv2.cvtColor(road_img, cv2.COLOR_RGB2HSV)

    # Create masks for brown and blue roads
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Get coordinates of brown and blue roads
    brown_coords = np.column_stack(np.where(brown_mask > 0))
    blue_coords = np.column_stack(np.where(blue_mask > 0))

    # Debug: Print detected coordinates count
    print(f"Brown roads detected: {len(brown_coords)}")
    print(f"Blue roads detected: {len(blue_coords)}")

    # Ensure there are both blue and brown roads before selecting points
    if len(brown_coords) == 0 or len(blue_coords) == 0:
        print("Error: No blue or brown roads detected. Check the input image or HSV color thresholds.")
        exit()

    # === Process for 3 pairs of points ===
    num_pairs = 5
    attempts = 0
    paths_found = 0
    path_number=0
    selected_blue_points = []  # Store selected blue points

    while paths_found < num_pairs and attempts < 50:
        attempts += 1

        # Pick a random blue point, ensure it's far enough from previously selected points
        valid_point_found = False
        max_retries = 20
        retry_count = 0

        while not valid_point_found and retry_count < max_retries:
            start_point = tuple(blue_coords[np.random.randint(len(blue_coords))])

            # Check distance from previously selected points
            if is_far_enough(start_point, selected_blue_points, min_dist_threshold=200):  # 200 pixels apart
                valid_point_found = True
            else:
                retry_count += 1

        if not valid_point_found:
            print(f"Could not find a valid new point after {max_retries} retries. Skipping.")
            continue

        # Add selected point to list
        selected_blue_points.append(start_point)

        # Find nearest brown point
        end_point,distanceval = find_nearest_brown(start_point, brown_coords)

        # Debug: Print selected points
        print(f"\nAttempt {attempts}:")
        print(f"Selected Blue Point: {start_point}")
        print(f"Nearest Brown Point: {end_point}")

        # === Find and highlight the shortest path ===
    # === Find and highlight the shortest path ===
        path = bfs_find_path(road_img, start_point, end_point)
        if path:
            paths_found += 1
            path_number+=1
            print(f"Path found for pair {paths_found} after {attempts} attempt(s).")
            print("path length: ",round(distanceval,2))
            time_evac=round(distanceval,2)//10
            with open(FILE_PATH, "a") as file:  # "a" mode appends new data
                file.write(f"{path_number}, {round(distanceval,2)}, {time_evac}\n")

            # Draw path on the original image
            for y, x in path:
                cv2.circle(road_img, (x, y), radius=8, color=(255, 0, 0), thickness=-1)  # Thick red path

            # Draw start and end points on the same image using OpenCV
            cv2.circle(road_img, (start_point[1], start_point[0]), radius=20, color=(0, 0, 255), thickness=-1)  # Blue
            cv2.circle(road_img, (end_point[1], end_point[0]), radius=20, color=(139, 69, 19), thickness=-1)  # Brown

            # Add labels for each start (S1, S2, ...) and end (E1, E2, ...)
            label_start = f"S{paths_found}"
            label_end = f"E{paths_found}"
            cv2.putText(road_img, label_start, (start_point[1] + 15, start_point[0] - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3, cv2.LINE_AA)  # Bigger yellow text
            cv2.putText(road_img, label_end, (end_point[1] + 15, end_point[0] - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3, cv2.LINE_AA)  # Bigger yellow text
        else:
            print("No path found. Picking a new blue point immediately...")


    cv2.imwrite(output_path,cv2.cvtColor(road_img,cv2.COLOR_RGB2BGR))
    
    return True