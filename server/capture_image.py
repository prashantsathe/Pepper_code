"""Example: Use localization methods"""
from naoqi import ALProxy
import socket
import select
import fcntl
import struct
import time
import json
from PIL import Image
import qi
import argparse
import sys
import numpy as np
import cv2
import base64

# AL_resolution
AL_kQQQQVGA = 8 	#Image of 40*30px
AL_kQQQVGA  = 7 	#Image of 80*60px
AL_kQQVGA   = 0 	#Image of 160*120px
AL_kQVGA    = 1 	#Image of 320*240px
AL_kVGA     = 2 	#Image of 640*480px
AL_k4VGA    = 3 	#Image of 1280*960px
AL_k16VGA   = 4 	#Image of 2560*1920px

# Camera IDs
AL_kTopCamera = 0
AL_kBottomCamera = 1
AL_kDepthCamera = 2

# Need to add All color space variables
AL_kBGRColorSpace = 13

# Supported fps details
# Resolution 	Supported Framerate
# AL::kQQQQVGA 	from 1 to 30 fps
# AL::kQQQVGA 	from 1 to 30 fps
# AL::kQQVGA 	from 1 to 30 fps
# AL::kQVGA 	from 1 to 30 fps
# AL::kVGA 	from 1 to 30 fps
# AL::k4VGA 	1 fps
# AL::k16VGA 	1 fps

def main(session, exploration_file, topic_path):

    try:
        # motion_service = session.service("ALMotion")
        videoDevice = session.service("ALVideoDevice")

        # Wake up robot
        # motion_service.wakeUp()
        # motion_service.setTangentialSecurityDistance(0.01)
        # Load a previously saved exploration
        
	#
        # captureDevice = videoDevice.subscribeCamera("test", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)
        captureDevice = videoDevice.subscribeCamera("test", 1, AL_kQVGA, AL_kBGRColorSpace, 10)
        # captureDevice = videoDevice.subscribe("test", AL_kQVGA, AL_kBGRColorSpace, 10)
        print "ID = " + captureDevice
        # create image
        width = 320
        height = 240
        image = np.zeros((height, width, 3), np.uint8)
        result = videoDevice.getImageRemote(captureDevice);
        if result == None:
            print '# cannot capture.'
        elif result[6] == None:
            print 'no image data string.'
        else:
            print "Got an image"
            # Get the image size and pixel array.
            imageWidth = result[0]
            imageHeight = result[1]
            array = result[6]
            image_string = str(bytearray(array))

            # Create a PIL Image from our pixel array.
            im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)
            # Save the image.
            # im.save("camImage.png", "PNG")
            # im.save(filename, "PNG")
            im.show()

        # cameraID = 0
        # resolution = 2
        # fileName = str("2DFile")
        # photoCapture.setResolution(resolution)
        # photoCapture.setCameraID(cameraID)
        # photoCapture.setPictureFormat("jpg")
        # photoCapture.takePicture( "/home/nao/", fileName )

    except KeyboardInterrupt as msg:
        # need to close pepper also
        motion_service.rest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--explo", type=str, help="Path to .explo file.")
    parser.add_argument("--topic-path", type=str, required=True,
                        help="absolute path of the dialog topic file (on the robot)")
    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session, args.explo, args.topic_path)

