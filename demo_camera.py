# Import modules
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


# Initialize camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Let camera warm up
time.sleep(0.3)
print("Press q to quit")

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    cv2.imshow("Preview", img)

    rawCapture.truncate(0)

    key = cv2.waitKey(1)
    if key == ord("q"):
        print("Quitting")
        break

cv2.destroyAllWindows()
camera.close()
