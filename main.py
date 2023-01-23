# Imports
import os

# Import custom class
from auto_crop import AutoCrop

# Get list of image files
image_files = os.listdir("images/")

# Iterate through all images and apply changes
for image_file in image_files:
    # Create instance of AutoCrop for current image
    AutoCropImage = AutoCrop(file=image_file, image_path="images/"+image_file)

    # Run processing methods on current image
    AutoCropImage.variable_resize()
    # Show original image (after resize for easier viewing)
    AutoCropImage.show_image()
    # Continue processing methods on current image
    AutoCropImage.greyscale()
    AutoCropImage.emphasize_whites()
    AutoCropImage.blur()
    AutoCropImage.detect_edges()
    AutoCropImage.dilate()
    AutoCropImage.contour_crop_and_rotate()

    # Show cropped and rotated image
    AutoCropImage.show_image_cropped()

    # Save cropped and rotated image
    AutoCropImage.save_crop()