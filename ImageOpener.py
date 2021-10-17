# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 22:05:40 2021

@author: leand
"""

from PIL import Image
import os


class ImageUnpacker:
    
    def __init__(self, image_name):
        self.image_name = image_name

    def set_image_name(self, image_name):
        self.image_name = image_name
        
    def get_image_name(self):
        return self.image_name
    
    # Needs to be called to load the image into variable space
    def updateImage(self):
        current_dir = os.getcwd()
        self.im = Image.open(current_dir + "/" + self.image_name)
    
    # To check whether it works
    def showImage(self):
        self.im.show()
        
    # Returns [(x_size,y_size),[...]] where the ... represents the image data
    def getData(self):
        self.data = self.im.getdata()
        return [self.im.size, list(self.data)]
    
      
    
if __name__ == '__main__':
    
    iU = ImageUnpacker("testImage.png")
    iU.updateImage()
    iU.showImage()
    
    DASADD = iU.getData()

    
