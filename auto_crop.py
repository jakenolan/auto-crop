# Imports
import cv2
import numpy as np

class AutoCrop:

    # Init
    def __init__(self, file, image_path):
        # Save image_path and file
        self.file = file
        self.image_path = image_path
        # Read in the image
        self.image = cv2.imread(image_path)
        # Create dimensions variables for later
        self.img_height = 0
        self.img_width = 0
    
    # Show image (close out with any key)
    def show_image(self):
        # Show image and wait
        cv2.imshow("", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Auto adjust image size to be under a prespecified height and width
    def variable_resize(self):
        # Set the width and height limit
        width_limit = 1000
        height_limit = 1000
        # Get the current size of the image
        height, width, _ = self.image.shape
        # Calculate the new size
        if width > width_limit or height > height_limit:
            if width > height:
                ratio = width_limit / width
                new_size = (width_limit, int(height * ratio))
            else:
                ratio = height_limit / height
                new_size = (int(width * ratio), height_limit)
            # Resize the image
            self.image = cv2.resize(self.image, new_size, interpolation = cv2.INTER_LINEAR)
            # Update dimensions for calculations
            self.img_height, self.img_width = self.image.shape[:2]
    
    # Convert the image to greyscale
    def greyscale(self):
        self.image_greyscale = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    # Emphasize whites and dull other colors
    def emphasize_whites(self):
        # Threshold the image to isolate the white pixels
        # Lowering the first integer argument will lower the value a pixel needs to be to be turned white
        _, image_thresh = cv2.threshold(self.image_greyscale, 200, 255, cv2.THRESH_BINARY)

        # Use the thresholded image to mask the original image
        self.image_adjusted_whites = self.image.copy()
        self.image_adjusted_whites[image_thresh == 0] = [0, 0, 0]

    # Blur image
    def blur(self):
        # Apply blur function to counter noise
        # Higher kernal size (x, x) reduces noise by blurring more
        self.image_blurred = cv2.GaussianBlur(self.image_adjusted_whites, (3, 3), 0)
    
    # Edge detection
    def detect_edges(self):
        # Apply Canny edge detection
        # Lower thresholds results in more edges being detected (resulting in more noise too)
        self.image_canny = cv2.Canny(self.image_blurred, threshold1=100, threshold2=300)
    
    # Dilate image
    def dilate(self):
        # Define the dilation kernel
        # Raising kernel size will make the effect of the dilation stronger
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))

        # Apply dilation to close gaps in the edges
        self.image_dilated = cv2.dilate(self.image_canny, kernel)
    
    # Find contours, find bounding box, and crop/rotate accordingly
    def contour_crop_and_rotate(self):
        # Find contours in the image
        contours, _ = cv2.findContours(self.image_dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate through the contours
        for contour in contours:
            # Get the bounding box of the contour
            [x, y, w, h] = cv2.boundingRect(contour)
            # Filter contours by area (Area > 10% of images size)
            if cv2.contourArea(contour) > int(self.img_width * self.img_height / 10):
                # Check if bounding box is within image boundaries
                if x > 0 and y > 0 and x+w < self.img_width and y+h < self.img_height:
                    # Get the rotated bounding box of the contour
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    # Draw the bounding box on the original image (not necessary unless showing)
                    self.image_bb_drawn = self.image.copy()
                    cv2.drawContours(self.image_bb_drawn, [box], -1, (0, 255, 0), 2)
                    # Get the rotation angle
                    angle = rect[2]
                    # Get the center of the bounding box
                    cx = int(rect[0][0])
                    cy = int(rect[0][1])
                    # Get the size of the bounding box
                    w = int(rect[1][0])
                    h = int(rect[1][1])
                    # Get the rotation matrix
                    rotation_matrix = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
                    # Rotate the image
                    image_rotated = cv2.warpAffine(self.image, rotation_matrix, (self.image.shape[1], self.image.shape[0]))
                    # Crop the image
                    self.image_cropped = cv2.getRectSubPix(image_rotated, (w, h), (cx, cy))

    # Show cropped image
    def show_image_cropped(self):
        # Show image and wait
        cv2.imshow("", self.image_cropped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    # Save cropped image
    def save_crop(self):
        # Save cropped image using region of interest
        cv2.imwrite("cropped_images/" + "cropped_" + self.file, self.image_cropped)