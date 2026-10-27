import cv2
import time
from pyzbar.pyzbar import decode
import pyautogui

cam = cv2.VideoCapture(0)

prev_input_time = time.time()
prev_output_time = time.time()
output_fps_calc = 0
frame_rate = 0

fps_pos_in = (20,40)
fps_pos_out = (20,60)
color = (0,255,0)
thick = 2

### TO DO:   *while learning open cv and image recognition*
# detect qr codes and see them on screen %% even use apriltags
# add mediapipe for hand gesture detection
# add facial recognition

# detect speed of objects from my hand, using bosch course
# predict the trajectory of the object, using bosch and sys id
# try to attack the object using a simulated gun, using bosch and control engineering

# draw from hand gestures complex shapes
# create 3d model from drawing
# create stl, export to prusa
# export gcode to UM



while True:
    current_time = time.time()
    ret,frame = cam.read()

    input_duration = current_time - prev_input_time
    input_fps = 1.0 / input_duration if input_duration > 0 else 0.0
    prev_input_time = current_time

    objects = decode(frame)
    time.sleep(0.1)
    for obj in objects:
        if obj.type == 'QRCODE':
            poly = obj.polygon
            cv2.line(frame,poly[0],poly[1],color=(100,10,10),thickness=thick)
            cv2.line(frame,poly[1],poly[2],color=(100,10,10),thickness=thick)
            cv2.line(frame,poly[2],poly[3],color=(100,10,10),thickness=thick)
            cv2.line(frame,poly[3],poly[0],color=(100,10,10),thickness=thick)


    cv2.putText(frame,f"FPS_IN: {round(input_fps)}",fps_pos_in,cv2.FONT_HERSHEY_SIMPLEX, 0.7,color,thickness=thick)
    cv2.putText(frame,f"FPS_OUT: {round(output_fps_calc)}",fps_pos_out,cv2.FONT_HERSHEY_SIMPLEX, 0.7,color,thickness=thick)
    cv2.imshow('Cam 0',frame)

    end_output_time = time.time()
    output_duration = end_output_time - prev_output_time
    output_fps_calc = 1.0 / output_duration if output_duration > 0 else 0.0
    prev_output_time = end_output_time

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

