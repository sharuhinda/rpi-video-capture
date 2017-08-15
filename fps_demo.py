from __future__ import print_function
from lib_camperformance import WebcamVideoStream
from lib_camperformance import FPS
import imutils
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100, help="# of frames to loop for FPS test")
ap.add_argument("-d", "--display", type=int, default=1, help="Display frames or not")
args = vars(ap.parse_args())

print("[INFO] Sampling frames from webcam...")
stream = cv2.VideoCapture(0)
fps = FPS().start()

while fps._numFrames < args["num_frames"]:
    (grabbed, frame) = stream.read()
    frame = imutils.resize(frame, width=400)

    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

    fps.update()

fps.stop()
print("[INFO] Elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] Approx. FPS: {:.2f}".format(fps.fps()))

stream.release()
cv2.destroyAllWindows()

print("[INFO] Sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

while fps._numFrames < args["num_frames"]:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

    fps.update()

fps.stop()
print("[INFO] Elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] Approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
