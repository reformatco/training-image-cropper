import cv2
import os
import re

# Prompt the user to enter the directory path
dir_path = input("Enter the directory path: ")

# Prompt the user to enter the crop size (default to 512x512)
crop_size = input("Enter the crop size (default is 512x512): ")
if crop_size == "":
    crop_size = "512x512"

# Validate the crop size format
if not re.match(r"^\d{3,4}x\d{3,4}$", crop_size):
    print("Error: Please enter the crop size in the format 512x512")
    exit(1)

# Parse the crop size
crop_width, crop_height = map(int, crop_size.split("x"))

# Prompt the user to enter the new file name
new_file_name = input("Enter the new file name (leave blank to use the original file name): ")

# Output a message to indicate that the processing has started
if new_file_name:
    print(f"Processing JPEG files in {dir_path} and renaming to {new_file_name}...")
else:
    print(f"Processing JPEG files in {dir_path}...")

# Initialize a cascade classifier for face detection (optional)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Loop through all files in the directory
i = 1
for file in os.listdir(dir_path):
    if file.lower().endswith((".jpg", ".jpeg", ".webp", ".png")):
        # Load the image
        img_path = os.path.join(dir_path, file)
        img = cv2.imread(img_path)

        # Detect faces (optional)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # If no faces are detected, detect edges instead
        if len(faces) == 0:
            edges = cv2.Canny(gray, 100, 200)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            areas = [cv2.contourArea(c) for c in contours]
            max_idx = areas.index(max(areas))
            x, y, w, h = cv2.boundingRect(contours[max_idx])
        else:
            # If faces are detected, crop around the first face
            x, y, w, h = faces[0]

        # Crop the image around the detected region
        crop_x = max(x + w/2 - crop_width/2, 0)
        crop_y = max(y + h/2 - crop_height/2, 0)
        crop_img = img[int(crop_y):int(crop_y+crop_height), int(crop_x):int(crop_x+crop_width)]

        # Save the cropped image
        if new_file_name:
            new_filename = f"{new_file_name}-{i}.jpg"
            cv2.imwrite(os.path.join(dir_path, new_filename), crop_img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        else:
            new_filename = os.path.splitext(file)[0] + ".jpg"
            cv2.imwrite(os.path.join(dir_path, new_filename), crop_img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

        # Output a message to indicate that the image has been processed
        if new_file_name:
            print(f"Cropped and renamed image {new_filename}")
        else:
            print(f"Cropped image {file}")
        i += 1

# Output a message to indicate that the processing has finished
print("Processing complete.")
