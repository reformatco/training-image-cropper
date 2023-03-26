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
    print("Error: Please enter the crop size in the format 'widthxheight', e.g. '512x512'")
    exit()

# Parse the crop size
crop_width, crop_height = map(int, crop_size.split("x"))

# Prompt the user to enter the new file name (optional)
new_file_name = input("Enter a new file name (leave blank to keep the original file name): ")

# Output a message to indicate that the processing has started
print(f"Processing image files in {dir_path}...")

# Initialize a cascade classifier for face detection (optional)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Create the output directory
output_dir_path = os.path.join(os.path.dirname(dir_path), "output", os.path.basename(dir_path))
os.makedirs(output_dir_path, exist_ok=True)

# Loop through all image files in the directory
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

        # Calculate the cropping region
        center_x, center_y = x + w/2, y + h/2
        crop_x1, crop_y1 = int(center_x - crop_width/2), int(center_y - crop_height/2)
        crop_x2, crop_y2 = crop_x1 + crop_width, crop_y1 + crop_height

        # Crop the image around the detected region
        crop_img = img[crop_y1:crop_y2, crop_x1:crop_x2]

        # Resize the cropped image to 512x512
        if crop_img.size != 0:
            resized_img = cv2.resize(crop_img, (512, 512), interpolation=cv2.INTER_AREA)
        else:
            print(f"Error: {file} has zero size and could not be cropped")
            continue


        # Save the cropped and resized image
        if new_file_name:
            new_filename = f"{new_file_name}-{i}.jpg"
        else:
            new_filename = os.path.splitext(file)[0] + ".jpg"
        output_file_path = os.path.join(output_dir_path, new_filename)
        cv2.imwrite(output_file_path, resized_img)
        print(f"Saved {output_file_path}")

        # Increment the counter
        i += 1

        # Output a message to indicate that the processing of the current file is complete
        print(f"Processing complete for {file}")

        # Output a message to indicate that the processing of all files is complete
        print("All image files processed.")