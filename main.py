import math

import cv2
import time

import mediapipe
from mediapipe.tasks.python.core import base_options
from pyzbar.pyzbar import decode # for qr codes
from pupil_apriltags import Detector # for april tags
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import pyautogui

def draw_rect(rect):
    cv2.line(frame, rect[0], rect[1], color=(100, 10, 10), thickness=thick)
    cv2.line(frame, rect[1], rect[2], color=(100, 10, 10), thickness=thick)
    cv2.line(frame, rect[2], rect[3], color=(100, 10, 10), thickness=thick)
    cv2.line(frame, rect[3], rect[0], color=(100, 10, 10), thickness=thick)




camera_params = (650.0, 650.0, 640.0, 360.0)
cam = cv2.VideoCapture(0)
code = 0   #what detection to use



MODEL_PATH = "hand_landmarker.task"

# Configure the hand detector
options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)
# Connections between the 21 landmarks
connections = vision.HandLandmarksConnections.HAND_CONNECTIONS
hand_detector = vision.HandLandmarker.create_from_options(options)

at_detector = Detector(
    families= "tag36h11",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0
)
april_tag_size = 0.06144

prev_input_time = time.time()
prev_output_time = time.time()
output_fps_calc = 0
frame_rate = 0

fps_pos_in = (20,40)
fps_pos_out = (20,60)
color = (0,255,0)
thick = 2

### TO DO:   *while learning open cv and image recognition*
#$ detect qr codes and see them on screen
#  even use apriltags
#  add mediapipe for hand gesture detection
#  add facial recognition

#  detect speed of objects from my hand, using bosch course
#  predict the trajectory of the object, using bosch and sys id
#  try to attack the object using a simulated gun, using bosch and control engineering

#  draw from hand gestures complex shapes
#  create 3d model from drawing
#  create stl, export to prusa
#  export gcode to UM




while True:
    current_time = time.time()
    ret,frame = cam.read()

    input_duration = current_time - prev_input_time
    input_fps = 1.0 / input_duration if input_duration > 0 else 0.0
    prev_input_time = current_time

    if code == 1:
        objects = decode(frame)
        for obj in objects:
            if obj.type == 'QRCODE':
                poly = obj.polygon
                draw_rect(poly)
    elif code == 2:
        gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

        detections = at_detector.detect(
            gray,
            estimate_tag_pose=True,
            camera_params=camera_params,
            tag_size=april_tag_size,
        )

        for obj in detections:
            poly = obj.corners.astype(int)
            draw_rect(poly)
            center = obj.center.astype(int)

            x_trans = obj.pose_t[0][0]
            y_trans = obj.pose_t[1][0]
            z_depth = obj.pose_t[2][0]

            distance = math.sqrt(x_trans*x_trans+y_trans*y_trans+z_depth*z_depth)

            print(f"Distance is : {distance}")

            value = obj.tag_id
            cv2.putText(frame,f"{value}",center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            # print(obj)


    elif code == 3:








    cv2.putText(frame,f"FPS_IN: {round(input_fps)}",fps_pos_in,cv2.FONT_HERSHEY_SIMPLEX, 0.7,color,thickness=thick)
    cv2.putText(frame,f"FPS_OUT: {round(output_fps_calc)}",fps_pos_out,cv2.FONT_HERSHEY_SIMPLEX, 0.7,color,thickness=thick)
    cv2.imshow('Cam 0',frame)

    end_output_time = time.time()
    output_duration = end_output_time - prev_output_time
    output_fps_calc = 1.0 / output_duration if output_duration > 0 else 0.0
    prev_output_time = end_output_time

    key = cv2.waitKey(1)

    match key:
        case 48:  # ASCII for '0'
            code = 0
        case 49:  # ASCII for '1'
            code = 1
        case 50:  # ASCII for '2'
            code = 2
        case 51:  # ASCII for '3'
            code = 3
        case 113:  # ASCII for 'q'
            break



cam.release()
cv2.destroyAllWindows()


