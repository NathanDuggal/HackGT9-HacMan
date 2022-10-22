import cv2
import numpy as np
from tkinter import Tk, filedialog
import os

img = cv2.imread('client/assets/sprites/Maze.png', cv2.IMREAD_GRAYSCALE)
with open("array_image.txt", 'w') as file:
    file.write(str([list(e) for e in list(np.where(img > 0.5, 1, 0))]))