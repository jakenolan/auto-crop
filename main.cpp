#include <iostream>
#include <vector>
#include <io.h>
#include <direct.h>
#include "auto_crop.h"

int main() {
    // Get list of image files
    std::vector<std::string> image_files;
    _finddata_t file;
    intptr_t hFile;
    if ((hFile = _findfirst("images\\*.*", &file)) != -1) {
        do {
            if (strcmp(file.name, ".") != 0 && strcmp(file.name, "..") != 0) {
                image_files.push_back(file.name);
            }
        } while (_findnext(hFile, &file) == 0);
        _findclose(hFile);
    } else {
        std::cout << "Error opening images directory" << std::endl;
        return -1;
    }
    // Iterate through all images and apply changes
    for (auto const& image_file : image_files) {
        // Create instance of AutoCrop for current image
        AutoCrop AutoCropImage(image_file, "images\\" + image_file);

        // Run processing methods on current image
        AutoCropImage.variable_resize();
        // Show original image (after resize for easier viewing)
        AutoCropImage.show_image();
        // Continue processing methods on current image
        AutoCropImage.greyscale();
        AutoCropImage.emphasize_whites();
        AutoCropImage.blur();
        AutoCropImage.detect_edges();
        AutoCropImage.dilate();
        AutoCropImage.contour_crop_and_rotate();

        // Show cropped and rotated image
        AutoCropImage.show_image_cropped();

        // Save cropped and rotated image
        AutoCropImage.save_crop();
    }
    return 0;
}