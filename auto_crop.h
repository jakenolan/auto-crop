#ifndef AUTOCROP_H
#define AUTOCROP_H

#include <opencv2/opencv.hpp>
#include <iostream>

class AutoCrop{
    private:
        cv::Mat image;
        int img_height, img_width;
    public:
        AutoCrop(std::string image_path);
        void show_image();
        void variable_resize();
        void greyscale();
        void emphasize_whites();
        void blur();
        void detect_edges();
        void dilate();
        void contour_crop_and_rotate();
};

#endif