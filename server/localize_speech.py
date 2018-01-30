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
import thread
import datetime

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

#Global variable
navigation_service = None
motion_service = None
tts = None
videoDevice = None
ALDialog = None
ALpepper_navigation = False  # Boolean global variable
captureDevice = None
counter = 1


def capture_image(threadName, captureDevice):
    global ALpepper_navigation
    global videoDevice
    global counter

    # create image TODO This need to be in accordance with the capture image size
    width = 320
    height = 240
    nLocation = ""
    print "## Thread has started: " + str(ALpepper_navigation)

    while (ALpepper_navigation == True):
        image = np.zeros((height, width, 3), np.uint8)

        ''' # get image
        nLocation = str(navigation_service.getRobotPositionInMap()[0])
        #nLocation2 = str(navigation_service.getRobotPositionInMap()[1])
        print "I reached at: " + nLocation 
        # print "I uncertainty at: " + nLocation2 
        # filename = '/home/nao/images/camera-%s-%s.png'%datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')%nLocation
        # filename = '/home/nao/images/camera-%s.png'%datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        filename = '/home/nao/images/camera-%s.png'%datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        '''
        # get image
        nLocation = navigation_service.getRobotPositionInMap()[0]
        print "I reached at: " + str(nLocation)
        # print "I uncertainty at: " + nLocation2 
        # filename = '/home/nao/images/camera-%s.png'%datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        #filename = "/home/nao/images/camera_%0.5f_%0.5f_%0.5f.png"%(nLocation[0],nLocation[1],nLocation[2])
        filename = "/home/prashant/work/deep_learning/softbank_robot/sample_code/Pepper_code/server/Images/c%0.5d_%0.5f_%0.5f_%0.5f.png"%(counter, nLocation[0],nLocation[1],nLocation[2])
        counter += 1
        print ">" + filename

        print "Start-%s: %s" % (threadName, datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S'))
        result = videoDevice.getImageRemote(captureDevice);
        print "End-%s: %s" % (threadName, datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S'))

        if result == None:
            print 'cannot capture.'
        elif result[6] == None:
            print 'no image data string.'
        else:
            '''
            # translate value to map
            values = map(ord, list(result[6]))
            i = 0
            for y in range(0, height):
                for x in range(0, width):
                    image.itemset((y, x, 0), values[i + 0])
                    image.itemset((y, x, 1), values[i + 1])
                    image.itemset((y, x, 2), values[i + 2])
                    i += 3
            # show image
            cv2.imshow("pepper-Depth-camera-320x240", image)
            '''
            print "Got an image"
            # Get the image size and pixel array.
            imageWidth = result[0]
            imageHeight = result[1]
            array = result[6]
            image_string = str(bytearray(array))

            # Create a PIL Image from our pixel array.
            im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)
            # Save the image.
            #im.save("camImage.png", "PNG")
            im.save(filename, "PNG")
            #im.show()
            # time.sleep(0.002)

def navigate(captureDevice, x, y, z):
    global navigation_service
    global tts
    global ALpepper_navigation

    # navigation_service.navigateToInMap([float(x), float(y), float(z)])
    # Check where the robot arrived
    # print "I reached: " + str(navigation_service.getRobotPositionInMap()[0])
    max_attempts = 5
    attempt = 1

    # start Image capturing thread
    # Create two threads as follows
    ALpepper_navigation = True
    try:
        thread.start_new_thread(capture_image, ("Thread-CaptureImage", captureDevice ))
    except:
        print "###Error: unable to start thread"

    while (attempt <= max_attempts):
        # if self.stopPatrol:
        #    break
        fut = navigation_service.navigateToInMap([float(x), float(y), float(z)], _async=True)
        print "I reached: " + str(navigation_service.getRobotPositionInMap()[0])
        # while (fut.isRunning()):
        #    self.updateRobotPosition()
        #    time.sleep(0.2)
        returnValue = fut.value()
	print "return value = " + str(returnValue)
        if (returnValue == 4) or (returnValue == 1):
            tts.say("oops, there is an obstacle")
            attempt += 1
        elif (returnValue == 6) or (returnValue == 5):
            tts.say("This target is too far for me, I will skip it")
            break
        else:
            tts.say("Stopping now")
            break

    ALpepper_navigation = False

def gotoAbhishekRoom():
    global captureDevice 
    print"Sure lets Go #####"

def main(session, exploration_file, topic_path):

    try:
	global navigation_service
        global motion_service
        global tts
        global videoDevice
        global ALDialog

        # Get the services ALNavigation and ALMotion.
        navigation_service = session.service("ALNavigation")
        motion_service = session.service("ALMotion")
	tts = session.service("ALTextToSpeech")
        videoDevice = session.service("ALVideoDevice")
        # Getting the service ALDialog
        ALDialog = session.service("ALDialog")

        # Wake up robot
        motion_service.wakeUp()
        # motion_service.setTangentialSecurityDistance(0.01)
        # Load a previously saved exploration

	# Subscribe to 3D or 2D camera (Top = 0, bottom = 1, depth(3D) = 2)
	# subscribe top camera
        captureDevice = videoDevice.subscribeCamera("test", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)
        #captureDevice = videoDevice.subscribeCamera("test", AL_kDepthCamera, AL_kQVGA, 17, 10)

        navigation_service.stopLocalization()
        navigation_service.loadExploration(exploration_file)

        # Relocalize the robot and start the localization process.
        guess = [0., 0.] # assuming the robot is not far from the place where
                         # he started the loaded exploration.
        navigation_service.relocalizeInMap(guess)
        navigation_service.startLocalization()

        ALDialog.setLanguage("English")

        for dT in ALDialog.getLoadedTopics('English'):
            try:
                ALDialog.unloadTopic(dT)
            except Exception as e:
                print "Could not unload", dT
                print e

        # Loading the topic given by the user (absolute path is required)
        topf_path = topic_path.decode('utf-8')
        topic_name = ALDialog.loadTopic(topf_path.encode('utf-8'))

        # Activating the loaded topic
        ALDialog.activateTopic(topic_name)

        # Starting the dialog engine - we need to type an arbitrary string as the identifier
        # We subscribe only ONCE, regardless of the number of topics we have activated
        ALDialog.subscribe('my_dialog_example')


        # Navigate to another place in the map
        # navigation_service.navigateToInMap([2., 0., 0.])
        prompt = "Enter Co-ordinate (format = x/y/z): "
        while True:
            try:
                lists = raw_input(prompt)
            except NameError:
                lists = input(prompt)

            if lists:
                if lists[:1] == 't':
                    print(lists)
                else:
                    x, y, z = lists.split("/")
                    navigate(captureDevice, x, y, z)
                    # capture image and location
                    # capture_image(captureDevice)
                    # global ALpepper_navigation
                    # ALpepper_navigation = True
                    # capture_image("Thread", captureDevice)
                    print "FINALLY I reached at: " + str(navigation_service.getRobotPositionInMap()[0])

        # Check where the robot arrived
        print "I reached: " + str(navigation_service.getRobotPositionInMap()[0])

        # Stop localization
        navigation_service.stopLocalization()
    except KeyboardInterrupt as msg:
        # need to close pepper also
        motion_service.rest()

        # stopping the dialog engine
        ALDialog.unsubscribe('my_dialog_example')
        # Deactivating the topic
        ALDialog.deactivateTopic(topic_name)

        # now that the dialog engine is stopped and there are no more activated topics,
        # we can unload our topic and free the associated memory
        ALDialog.unloadTopic(topic_name)

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

