import cv2
import os

# Prompt the user to enter the directory path
dir_path = input("Enter the directory path: ")

# Prompt the user to enter the crop size
crop_size = input("Enter the crop size (e.g. 512x512): ")
crop_width, crop_height = map(int, crop_size.split("x"))

# Output a message to indicate that the processing has started
print(f"Processing JPEG files in {dir_path}...")

# Initialize a cascade classifier for face detection (optional)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Loop through all JPEG files in the directory
for file in os.listdir(dir_path):
    if file.endswith(".jpg"):
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
        cv2.imwrite(img_path, crop_img)

# Output a message to indicate that the processing has finished
print("Processing complete.")