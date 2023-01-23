#include <opencv2/opencv.hpp>
#include <iostream>

class AutoCrop{
    private:
        cv::Mat image;
        int img_height, img_width;
    public:
        AutoCrop(std::string image_path){
            // Read in the image
            image = cv::imread(image_path);
            // Create dimensions variables for later
            img_height = 0;
            img_width = 0;
        }
    // Show image (close out with any key)
    void show_image(){
        // Show image and wait
        cv::imshow("", image);
        cv::waitKey(0);
        cv::destroyAllWindows();
    }

    // Auto adjust image size to be under a prespecified height and width
    void variable_resize(){
        // Set the width and height limit
        int width_limit = 1000;
        int height_limit = 1000;
        // Get the current size of the image
        img_height = image.rows;
        img_width = image.cols;
        // Calculate the new size
        if (img_width > width_limit || img_height > height_limit) {
            if (img_width > img_height) {
                double ratio = (double)width_limit / img_width;
                cv::resize(image, image, cv::Size(), ratio, ratio, cv::INTER_LINEAR);
            }
            else {
                double ratio = (double)height_limit / img_height;
                cv::resize(image, image, cv::Size(), ratio, ratio, cv::INTER_LINEAR);
            }
        }
    }

    // Convert the image to greyscale
    void greyscale(){
        cv::cvtColor(image, image, cv::COLOR_BGR2GRAY);
    }

    // Emphasize whites and dull other colors
    void emphasize_whites(){
        // Threshold the image to isolate the white pixels
        // Lowering the first integer argument will lower the value a pixel needs to be to be turned white
        cv::Mat image_thresh;
        cv::threshold(image, image_thresh, 200, 255, cv::THRESH_BINARY);

        // Use the thresholded image to mask the original image
        cv::Mat image_adjusted_whites = image.clone();
        for (int i = 0; i < image_adjusted_whites.rows; i++) {
            for (int j = 0; j < image_adjusted_whites.cols; j++) {
                if (image_thresh.at<uchar>(i, j) == 0) {
                    image_adjusted_whites.at<cv::Vec3b>(i, j) = cv::Vec3b(0, 0, 0);
                }
            }
        }
        image = image_adjusted_whites;
    }

    // Blur image
    void blur(){
        // Apply blur function to counter noise
        // Higher kernal size (x, x) reduces noise by blurring more
        cv::GaussianBlur(image, image, cv::Size(3, 3), 0);
    }
    
    // Edge detection
    void detect_edges(){
        // Apply Canny edge detection
        // Lower thresholds results in more edges being detected (resulting in more noise too)
        cv::Canny(image, image, 100, 300);
    }

    // Dilate image
    void dilate(){
        // Define the dilation kernel
        // Raising kernel size will make the effect of the dilation stronger
        cv::Mat kernel = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(9, 9));

        // Apply dilation to close gaps in the edges
        cv::dilate(image, image, kernel);
    }

    void contour_crop_and_rotate(){
        // Find contours in the image
        std::vector<std::vector<cv::Point> > contours;
        cv::findContours(image_dilated, contours, cv::RETR_LIST, cv::CHAIN_APPROX_SIMPLE);

        // Iterate through the contours
        for (int i = 0; i < contours.size(); i++) {
            // Get the bounding box of the contour
            cv::Rect rect = cv::boundingRect(contours[i]);
            // Filter contours by area (Area > 10% of images size)
            if (cv::contourArea(contours[i]) > (img_width * img_height / 10)) {
                // Check if bounding box is within image boundaries
                if (rect.x > 0 && rect.y > 0 && rect.x + rect.width < img_width && rect.y + rect.height < img_height) {
                    // Get the rotated bounding box of the contour
                    cv::RotatedRect minRect = cv::minAreaRect(contours[i]);
                    cv::Point2f rect_points[4]; 
                    minRect.points(rect_points);
                    // Draw the bounding box on the original image (not necessary unless showing)
                    image_bb_drawn = image.clone();
                    for(int j = 0; j < 4; j++)
                    {
                    cv::line(image_bb_drawn, rect_points[j], rect_points[(j+1)%4], cv::Scalar(0,255,0), 2, cv::LINE_AA);
                    }
                    // Get the rotation angle
                    float angle = minRect.angle;
                    // Get the center of the bounding box
                    cv::Point2f center = minRect.center;
                    int cx = center.x;
                    int cy = center.y;
                    // Get the size of the bounding box
                    int w = minRect.size.width;
                    int h = minRect.size.height;
                    // Get the rotation matrix
                    cv::Mat rot_mat = cv::getRotationMatrix2D(center, angle, 1.0);
                    // Rotate the image
                    cv::Mat image_rotated;
                    cv::warpAffine(image, image_rotated, rot_mat, image.size());
                    // Crop the image
                    cv::getRectSubPix(image_rotated, cv::Size(w,h), center, image_cropped);
                }
            }
        }
    }