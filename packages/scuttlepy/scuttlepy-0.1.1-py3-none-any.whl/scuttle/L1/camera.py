# This file retrieves an image from the usb camera.

# Import external libraries
import numpy as np
import cv2

# Initialize important vars
width  = 240 # desired width in pixels
height = 160 # desired height in pixels
camera = cv2.VideoCapture(0) # This will take images only from the camera assigned as "0"

# A function to capture an image & return all pixel data
def newImage(size=(width, height)):
    ret, image = camera.read() # return the image as well as ret
    if not ret: # (ret is a boolean for returned successfully?)
        return None # (return an empty var if the image could not be captured)
    image = cv2.resize(image,size) # reduce size of image
    return image

if __name__ == '__main__':
    while 1:
        image = newImage()
        print(image.shape) #print info about the image (height, width, colorspace)
