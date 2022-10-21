
import cv2
rgb = cv2.VideoCapture(0)
_, fr = rgb.read()    
gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faces = facec.detectMultiScale(gray, 1.3, 5)
pred, pred_dict = cnn.predict_points(roi[np.newaxis,:,:,np.newaxis]) 
pred, pred_dict = cnn.scale_prediction((x, fc.shape[1]+x), (y,   fc.shape[0]+y))
fr = apply_filter(fr, pred_dict)
fps = int(video_capture.get(cv2.CAP_PROP_FPS))
width  = int(video_capture.get(3)) 
height = int(video_capture.get(4))
fourcc = cv2.VideoWriter_fourcc(*'vp80')
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
     cv2.imshow(frame)