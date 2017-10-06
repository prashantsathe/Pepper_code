''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''' Prashant:- Robot(pepper) Remote control movement '''
''' Date:- 21/7/2017                                 '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from naoqi import ALProxy
import socket
import select
import fcntl
import struct
import time
import json
import numpy
import Image

host = socket.gethostname()
port = 9999

IP = "10.9.45.11"
PORT = 9559

def read_data_till_newline(connection):
        line = ""
        while True:
                part = connection.recv(1)
		if part:
                	if part != "\n":
                	        line+=part
                	elif part == "\n":
                	        break
		else:
			break
        return line


def main():
	# sample
	# camProxy = ALProxy("ALVideoDevice", '', PORT)
	try:
		tts = ALProxy('ALTextToSpeech', '', PORT)
	except Exception, e:
	        print "Error when creating ALNavigation proxy:"
	        print str(e)
	        exit(1)

	# Create a proxy to ALNavigation
	try:
		navigation = ALProxy("ALNavigation", '', PORT)
	except Exception, e:
	        print "Error when creating ALNavigation proxy:"
	        print str(e)
	        exit(1)

	# Create a proxy to ALMotion
	try:
	        motion = ALProxy("ALMotion", '', PORT)
	except Exception, e:
	        print "Error when creating ALMotion proxy:"
	        print str(e)
	        exit(1)

	# create a proxy for speech
	try:
	        tts =  ALProxy("ALTextToSpeech", '', PORT)
	except Exception, e:
	        print "Error when creating ALSpeech:"
	        print str(e)
	        exit(1)

	motion.wakeUp()
	motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])


	try:
		socket_t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket_t.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		socket_t.bind(('', port))
		socket_t.listen(2)
		inputs = [socket_t]
		output = []

		# conn, addr = s.accept()

		while inputs:
			readable, writable, exceptional = select.select(inputs, output, inputs)

			for soc in readable:
				if soc is socket_t:
					conn, addr = soc.accept()
					print '[*] Connected with ' + addr[0] + ':' + str(addr[1])
					conn.setblocking(0)
					inputs.append(conn)
				else:
					received_data = read_data_till_newline(soc)
					if received_data:
						try:
							j = json.loads(received_data)
						except ValueError, e:
							continue

						print(received_data)

						if j["command"]["api"] == "moveToward":
							print(j["command"]["parameters"]["x"], 
								j["command"]["parameters"]["y"], 
								j["command"]["parameters"]["theta"])
							move1 = motion.moveToward(j["command"]["parameters"]["x"], 
										j["command"]["parameters"]["y"], 
										j["command"]["parameters"]["theta"])
							# tts.say("I can walk!")
							# prashant test code 
							# time.sleep(10);
							# motion.stopMove();
							# motion.waitUntilMoveIsFinished()
							# tts.say("I got to my destination!")
						elif j["command"]["api"] == "navigate":
							motion.stopMove()
							# navigation command
							# Explore the environement, in a radius of 2 m.
							radius = 2.0
							error_code = navigation.explore(radius)
							if error_code != 0:
								print "# Exploration failed."
								continue
							# Saves the exploration on disk
							path = navigation.saveExploration()
							print "Exploration saved at path: \"" + path + "\""
							# Start localization to navigate in map
							navigation.startLocalization()
							# Come back to initial position
							navigation.navigateToInMap([0., 0., 0.])
							# Stop localization
							navigation.stopLocalization()
							# Retrieve and display the map built by the robot
							result_map = navigation.getMetricalMap()
							map_width = result_map[1]
    							map_height = result_map[2]
    							img = numpy.array(result_map[4]).reshape(map_width, map_height)
    							img = (100 - img) * 2.55 # from 0..100 to 255..0
    							img = numpy.array(img, numpy.uint8)
    							Image.frombuffer('L',  (map_width, map_height), img, 'raw', 'L', 0, 1).show()
						elif j["command"]["api"] == "localized":
							print"Yet to Implement the code"

						elif j["command"]["api"] == "stopMove":
							motion.stopMove()
						elif j["command"]["api"] == "say":
							tts.post.say(str(j["command"]["parameters"]["data"]))
							#print(j["command"]["parameters"]["data"])
					else:
						print("closing socket")
						inputs.remove(soc)
						soc.close()

			for soc in exceptional:
				inputs.remove(soc)
				soc.close()	

	except KeyboardInterrupt as msg:
		# need to close pepper also
		motion.rest()
		conn.close()	

if __name__ == "__main__":
	main()
