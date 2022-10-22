import cv2
import numpy as np
from tkinter import Tk, filedialog
import os
import dlib
import math
import time
from multiprocessing import Process, Value, Array
from flask import Flask
from flask import render_template
from flask import send_from_directory
import matplotlib.pyplot as plt
import matplotlib
from flask import Flask, request, jsonify
from PIL import Image

plt.ion()
plt.show()

#gets head tilt
def ratio_between_x_points(points):
    top_point = points[0] #retrieving from tuple of points (0 through 2)
    bottom_point = points[2]
    return (top_point[0] - bottom_point[0]) / math.dist(top_point, bottom_point)


#gets head nod ratios
def ratio_between_points(points):
    distances = []
    ratios = []
    for c,point in list(enumerate(points))[:-1]:
        distances.append(math.dist(point, points[c+1]))
    for c,distance in list(enumerate(distances))[:-1]:
        ratios.append(distance / distances[c+1])
    return ratios

def wink_ratio(points):
    return math.dist(points[5], points[6]) / math.dist(points[0], points[2])


def cart_to_polar(x, y): #this literally does not work
    theta = np.arctan2(y,x) #in radians
    r = math.sqrt(x**2 + y**2)
    position = [theta, r]
    return position

def website(x_joy, y_joy, calibrating, wink):
    app = Flask(__name__, template_folder='client', static_folder='client/assets/sprites',static_url_path="/assets/sprites")
    @app.route("/")
    def pacman():
        return render_template("index.html")
    @app.route("/data")
    def getdata():
        return '{{"x_joy": {}, "y_joy": {}, "wink": {}}}'.format(x_joy.value,y_joy.value, wink.value)
    @app.route("/calibrate", methods=['GET'])
    def calibrate():
        calibrating.value = 1
        return True
    app.run(debug=True, use_reloader=False, port=8002)
    
    
def video_stream(x_joy, y_joy, calibrating, wink):
    joystick_x = 0
    joystick_y = 0

    # define a video capture object
    vid = cv2.VideoCapture(0)

    detector = dlib.get_frontal_face_detector()

    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    start_time = time.time() - 5

    calibrated_nod_list = []
    calibrated_nod = 0
    calibrated_tilt_list = []
    calibrated_tilt = 0
    calibrated_turn_list = []
    calibrated_turn = 0

    joystick_x = 0
    joystick_y = 0

    while(True):
        # Capture the video frame
        # by frame

        ret, frame = vid.read()

        if (not isinstance(frame, type(None))):
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

                points = [8, 33, 27, 0, 16, 44, 46] #bottom, middle, top, left, right, eye top, eye bottom
                point_list = []
                for n in points:
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    point_list.append((x,y))

                    # Draw a circle
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0), thickness=-1)


                ratio_y = ratio_between_points(point_list)[0] #nodding (y)
                ratio_x = ratio_between_points([point_list[3],point_list[2],point_list[4]])[0]
                ratio_wink = wink_ratio(point_list)
                difference = ratio_between_x_points(point_list) #tilting (x)

                if (calibrating.value):
                    calibrated_nod_list = []
                    calibrated_tilt_list = []
                    calibrated_turn_list = []
                    start_time = time.time()
                    calibrating.value = 0
                if (time.time() - start_time < 5):
                    calibrated_nod_list.append(ratio_y)
                    calibrated_nod = np.mean(calibrated_nod_list)

                    calibrated_tilt_list.append(difference)
                    calibrated_tilt = np.mean(calibrated_tilt_list)

                    calibrated_turn_list.append(ratio_x)
                    calibrated_turn = np.mean(calibrated_turn_list)

                joystick_y = np.clip((ratio_y - calibrated_nod) * 7, -1, 1)
                joystick_x_turn = np.clip((ratio_x - calibrated_turn) * -3, -1, 1)
                joystick_x_tilt = np.clip((difference - calibrated_tilt) / 0.3, -1, 1)
                joystick_x = 0.25 * joystick_x_turn + joystick_x_tilt
                is_wink = ratio_wink < 0.05
                print(is_wink)
                

                y_joy.value = joystick_y
                x_joy.value = joystick_x
                wink.value = is_wink

                #convert to polar (not implemented)
                theta = cart_to_polar(joystick_x, joystick_y)[0]
                r = cart_to_polar(joystick_x, joystick_y)[1]
                if r > 1: #if r > 1
                    r = 1

            else:
                y_joy.value = 0
                x_joy.value = 0
                # Display the resulting frame
            cv2.imshow('frame', frame)
            plt.cla()
            plt.axis([-1,1,-1,1])
            plt.plot([joystick_x], [joystick_y], 'o')
            plt.pause(0.001)

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(205) & 0xFF == ord('q'):
                break
            
        # After the loop release the cap object
        vid.release()

        # Destroy all the windows
        cv2.destroyAllWindows()


if __name__ == '__main__':
    x_joy = Value('d', 0.0)
    y_joy = Value('d', 0.0)
    wink = Value('i', 0)
    calibrating = Value('i', 1)
    p1 = Process(target=video_stream, args=(x_joy, y_joy, calibrating, wink))
    p2 = Process(target=website, args=(x_joy, y_joy, calibrating, wink))
    p2.start()
    p1.start()
    p2.join()
    p1.join()