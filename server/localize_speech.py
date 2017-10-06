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
import numpy
import cv2
import base64



def main(session, exploration_file, topic_path):

    try:
        # Get the services ALNavigation and ALMotion.
        navigation_service = session.service("ALNavigation")
        motion_service = session.service("ALMotion")
        mem = session.service("ALMemory")
        tablet_service = session.service("ALMemory")

        # Getting the service ALDialog
        ALDialog = session.service("ALDialog")

        # Wake up robot
        motion_service.wakeUp()
        # motion_service.setTangentialSecurityDistance(0.01)
        # Load a previously saved exploration
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
                    navigation_service.navigateToInMap([float(x), float(y), float(z)])
                    # Check where the robot arrived
                    print "I reached: " + str(navigation_service.getRobotPositionInMap()[0])

        # Check where the robot arrived
        print "I reached: " + str(navigation_service.getRobotPositionInMap()[0])

        # Stop localization
        navigation_service.stopLocalization()
    except KeyboardInterrupt as msg:
        # need to close pepper also
        # motion_service.rest()

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

