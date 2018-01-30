import cv2
from naoqi import ALProxy
import vision_definitions

from PIL import Image
import StringIO
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        #self.video = cv2.VideoCapture(0)

        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        IP = "127.0.0.1"  # Replace here with your NAOqi's IP address.
        PORT = 9559
        self.camProxy = ALProxy("ALVideoDevice", IP, PORT)
        ####
        # Register a Generic Video Module

        resolution = vision_definitions.kQVGA  # 320 * 240
        colorSpace = vision_definitions.kRGBColorSpace
        fps = 30

        self.nameId = self.camProxy.subscribe("python_GVM", resolution, colorSpace, fps)



    def __del__(self):
        #self.video.release()
        self.camProxy.unsubscribe(self.nameId)

    def get_frame(self):
        #success, image = self.video.read()
        naoImage=self.camProxy.getImageRemote(self.nameId)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        #ret, jpeg = cv2.imencode('.jpg', image)

         # Get the image size and pixel array.
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        array = naoImage[6]

  # Create a PIL Image from our pixel array.
        try:
            im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
        except:
            im = Image.frombytes("RGB", (imageWidth, imageHeight), array)
        buf= StringIO.StringIO()
        im.save(buf, format= 'PNG')
        jpeg= buf.getvalue()
        return jpeg

        #return jpeg.tobytes()