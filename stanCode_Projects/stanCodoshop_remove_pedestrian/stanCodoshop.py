"""
File: stanCodoshop.py
----------------------------------------------
SC101_Assignment3
Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.

-----------------------------------------------

TODO:
"""

import os
import sys
from simpleimage import SimpleImage
import math


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns the color distance between pixel and mean RGB value

    Input:
        pixel (Pixel): pixel with RGB values to be compared
        red (int): average red value across all images
        green (int): average green value across all images
        blue (int): average blue value across all images

    Returns:
        dist (int): color distance between red, green, and blue pixel values

    """
    dist = math.sqrt((red - pixel.red) ** 2 + (green - pixel.green) ** 2 + (blue - pixel.blue) ** 2)
    return dist


def get_average(pixels):
    """
    Given a list of pixels, finds the average red, blue, and green values

    Input:
        pixels (List[Pixel]): list of pixels to be averaged
    Returns:
        rgb (List[int]): list of average red, green, blue values across pixels respectively

    Assumes you are returning in the order: [red, green, blue]

    """
    rgb = []
    red_sum = 0
    blue_sum = 0
    green_sum = 0
    for i in range(len(pixels)):
        red_sum += pixels[i].red
        blue_sum += pixels[i].blue
        green_sum += pixels[i].green
    rgb.append(red_sum // len(pixels))
    rgb.append(green_sum // len(pixels))
    rgb.append(blue_sum // len(pixels))
    return rgb


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest
    distance from the average red, green, and blue values across all pixels.

    Input:
        pixels (List[Pixel]): list of pixels to be averaged and compared
    Returns:
        best (Pixel): pixel closest to RGB averages

    """

    min_dist = float('inf')
    # create a variable to record the minimum distance
    average_rgb_lst = get_average(pixels)
    for pixel in pixels:
        if get_pixel_dist(pixel, average_rgb_lst[0], average_rgb_lst[1], average_rgb_lst[2]) < min_dist:
            min_dist = get_pixel_dist(pixel, average_rgb_lst[0], average_rgb_lst[1], average_rgb_lst[2])
            best = pixel
    return best


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    # create a blank image to be filled in
    for y in range(result.height):
        for x in range(result.width):
            pixels = []
            for image in images:
                pixels.append(image.get_pixel(x, y))
            new_pixel = result.get_pixel(x, y)
            new_pixel.red = get_best_pixel(pixels).red
            new_pixel.green = get_best_pixel(pixels).green
            new_pixel.blue = get_best_pixel(pixels).blue
            # color up the blank image
    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    # images = load_images(args[0])
    images = load_images(args[0])

    solve(images)


if __name__ == '__main__':
    main()
