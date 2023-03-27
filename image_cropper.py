from PIL import Image, ImageOps
import os, re, glob

def crop_image(img, output_path):

	global crop_size
	crop_width = crop_size[0]
	crop_height = crop_size[1]

	# Determine the smallest dimension of the image
	width, height = img.size
	min_dim = min(width, height)

	# Calculate the scale factor to resize the image
	scale_factor = min(crop_width, crop_height) / min_dim

	# Resize the image using the scale factor
	new_width = int(width * scale_factor)
	new_height = int(height * scale_factor)
	img_resized = img.resize((new_width, new_height))

	# Crop the image to 512x512 pixels from the center
	left = (new_width - crop_width) // 2
	top = (new_height - crop_height) // 2
	right = left + crop_width
	bottom = top + crop_height
	# img_cropped = img_resized.crop((left, top, right, bottom))
	# img.thumbnail(crop_size)

	cropped_image = ImageOps.fit(img, crop_size, method=Image.LANCZOS)

	cropped_image = ImageOps.autocontrast(cropped_image)

	# Save the cropped image
	cropped_image.save(output_path, 'JPEG', quality=95)
	# print(output_path)

	return output_path

# Prompt the user to enter the directory path
dir_path = input("Enter the directory path: ")

# Prompt the user to enter the crop size (default to 512x512)
crop_size_str = input("Enter the crop size (default is 512x512): ")
if crop_size_str == "":
	crop_size_str = "512x512"

# Validate the crop size format
if not re.match(r"^\d{3,4}x\d{3,4}$", crop_size_str):
	print("Error: Please enter the crop size in the format 'widthxheight', e.g. '512x512'")
	exit()

# Parse the crop size
output_width, output_height = map(int, crop_size_str.split("x"))
crop_size = (output_width, output_height)

# Prompt the user to enter the new file name (optional)
new_file_name = input("Enter a new file name (leave blank to keep the original file name): ")

# Output a message to indicate that the processing has started
print(f"Processing image files in {dir_path}...")

# Create the output directory
output_dir_path = os.path.join("output", os.path.basename(dir_path))
os.makedirs(output_dir_path, exist_ok=True)

# Loop through all image files in the directory
count = 0
for infile in glob.glob(f"{dir_path}/*.jpg"):
	file, ext = os.path.splitext(infile)
	
	if new_file_name:
		output_file = os.path.join(output_dir_path, f"{new_file_name}-{count}.jpg")
	else:
		output_file = os.path.join(output_dir_path, os.path.basename(file) + ext )

	with Image.open(infile) as img:
		output = crop_image(img, output_file)
	
	count += 1

	print(f"Saved {output}")
