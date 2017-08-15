# import packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# init
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# warmup camera
time.sleep(0.1)

fr1_captured = False

# frames capture
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if not fr1_captured:
        base_frame = gray
        fr1_captured = True
    
    image = frame.array
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key == ord("q"):
        break
