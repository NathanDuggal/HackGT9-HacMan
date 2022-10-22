import cv2
import numpy as np
from tkinter import Tk, filedialog
import os
import dlib
import math
  
# define a video capture object
vid = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

print(1)

def ratio_between_points(points):
    distances = []
    ratios = []
    for c,point in enumerate(points)[:-1]:
        distances.append(math.dist(point, points[c+1]))
    for c,distance in enumerate(distances)[:-1]:
        ratios.append(distance / distances[c+1])
    return ratios



while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    scale_percent = 25 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

    gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if (len(faces) != 0):
        face = faces[0]
        x1 = face.left() # left point
        y1 = face.top() # top point
        x2 = face.right() # right point
        y2 = face.bottom() # bottom point

        # Look for the landmarks
        landmarks = predictor(image=gray, box=face)
        x = landmarks.part(27).x
        y = landmarks.part(27).y

        # Draw a circle
        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0), thickness=-1)

        # Display the resulting frame
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()

# Destroy all the windows
cv2.destroyAllWindows()