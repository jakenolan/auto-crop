# Imports
import cv2
import numpy as np

# Auto adjust image size to be under a prespecified height and width
def variable_resize(image):
    # Set the width and height limit
    width_limit = 1000
    height_limit = 1000

    # Get the current size of the image
    height, width, _ = image.shape

    # Calculate the new size
    if width > width_limit or height > height_limit:
        if width > height:
            ratio = width_limit / width
            new_size = (width_limit, int(height * ratio))
        else:
            ratio = height_limit / height
            new_size = (int(width * ratio), height_limit)
        # Resize the image and return
        image = cv2.resize(image, new_size, interpolation = cv2.INTER_LINEAR)
        return image

# Read in the image
image = cv2.imread("img_3.png")

# Run variable resize to makie inputs relatively uniform
image = variable_resize(image)

# Save dimensions for calculations
img_height, img_width = image.shape[:2]

# Show image (close out with any key)
cv2.imshow("", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Convert the image to greyscale
image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image to isolate the white pixels
# Lowering the first integer argument will lower the value a pixel needs to be to be turned white
_, image_thresh = cv2.threshold(image_greyscale, 200, 255, cv2.THRESH_BINARY)

# Use the thresholded image to mask the original image
image_adjusted_whites = image.copy()
image_adjusted_whites[image_thresh == 0] = [0, 0, 0]

cv2.imshow("", image_adjusted_whites)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply blur function to counter noise
# Higher kernal size (x, x) reduces noise by blurring more
image_blurred = cv2.GaussianBlur(image_adjusted_whites, (3, 3), 0)

# Apply Canny edge detection
# Lower thresholds results in more edges being detected (resulting in more noise too)
image_canny = cv2.Canny(image_blurred, threshold1=100, threshold2=300)

cv2.imshow("", image_canny)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Define the dilation kernel
# Raising kernel size will make the effect of the dilation stronger
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))

# Apply dilation to close gaps in the edges
image_dilated = cv2.dilate(image_canny, kernel)

cv2.imshow("", image_dilated)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Find contours in the image
contours, _ = cv2.findContours(image_dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through the contours
for contour in contours:
    # Get the bounding box of the contour
    [x, y, w, h] = cv2.boundingRect(contour)
    # Filter contours by area (Area > 10% of images size)
    if cv2.contourArea(contour) > int(img_width * img_height / 10):
        # Check if bounding box is within image boundaries
        if x > 0 and y > 0 and x+w < img_width and y+h < img_height:
            # Get the rotated bounding box of the contour
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            # Draw the bounding box on the original image
            image_bb_drawn = image.copy()
            cv2.drawContours(image_bb_drawn, [box], -1, (0, 255, 0), 2)
            # Get the rotation angle
            angle = rect[2]

            # Get the center of the bounding box
            cx = int(rect[0][0])
            cy = int(rect[0][1])

            # Get the size of the bounding box
            w = int(rect[1][0])
            h = int(rect[1][1])

            # Get the rotation matrix
            M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)

            # Rotate the image
            image_rotated = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

            # Crop the image
            image_cropped = cv2.getRectSubPix(image_rotated, (w, h), (cx, cy))
            #image_cropped = image_rotated[cy-h//2:cy+h//2, cx-w//2:cx+w//2]
            print( image_cropped )

cv2.imshow("", image_bb_drawn)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("", image_cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save cropped image using region of interest
#cv2.imwrite('cropped_image.jpg', image_cropped)