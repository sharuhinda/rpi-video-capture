from __future__ import print_function
from lib_camperformance import PiVideoStream
from lib_camperformance import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100, help="# of frames for test")
ap.add_argument("-d", "--display", type=int, default=-1, help="Display frames or not")
args = vars(ap.parse_args())

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
stream = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)

print("[INFO] Sampling frames from `picamera` module...")
time.sleep(2.0)
fps = FPS().start()

for (i, f) in enumerate(stream):
	frame = f.array
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

	rawCapture.truncate(0)
	fps.update()

	if i == args["num_frames"]:
		break

fps.stop()
print("[INFO] Elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] Approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
stream.close()
rawCapture.close()
camera.close()

print("[INFO] Sampling frames from THREADED `picamera` module...")
vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()

while fps._numFrames < args["num_frames"]:
	frame = vs.read()
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

	fps.update()

fps.stop()
print("[INFO] Elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] Approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()