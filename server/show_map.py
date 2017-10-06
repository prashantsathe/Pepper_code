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



def main(session, exploration_file):
    """
    This example uses localization methods.
    """
    # Get the services ALNavigation and ALMotion.
    navigation_service = session.service("ALNavigation")
    motion_service = session.service("ALMotion")
    mem = session.service("ALMemory")
    tablet_service = session.service("ALMemory")

    # Wake up robot
    # motion_service.wakeUp()
    
    # Load a previously saved exploration
    navigation_service.stopLocalization()
    navigation_service.loadExploration(exploration_file)

    # Retrieve and display the map built by the robot
    result_map = navigation_service.getMetricalMap()
    map_width = result_map[1]
    map_height = result_map[2]
    img = numpy.array(result_map[4]).reshape(map_width, map_height)
    img = (100 - img) * 2.55 # from 0..100 to 255..0
    img = numpy.array(img, numpy.uint8)
    Image.frombuffer('L',  (map_width, map_height), img, 'raw', 'L', 0, 1).show()

    # Stop localization
    # navigation_service.stopLocalization()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--explo", type=str, help="Path to .explo file.")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session, args.explo)

