import qi
import argparse
import sys
import numpy
import Image


def main(session):
	"""	
	This example uses the explore method.
	"""
    	# Get the services ALNavigation and ALMotion.
	navigation_service = session.service("ALNavigation")
	motion_service = session.service("ALMotion")

    	# Wake up robot
	motion_service.wakeUp()
	#motion_service.setTangentialSecurityDistance(0.01)

    	# Explore the environement, in a radius of 2 m.
	radius = 3.0
	error_code = navigation_service.explore(radius)
	if error_code != 0:
		print "Exploration failed."
		return
	# Saves the exploration on disk
	path = navigation_service.saveExploration()
	print "Exploration saved at path: \"" + path + "\""
	
	# Retrieve and display the map built by the robot
	result_map = navigation_service.getMetricalMap()
	map_width = result_map[1]
	map_height = result_map[2]
	img = numpy.array(result_map[4]).reshape(map_width, map_height)
	img = (100 - img) * 2.55 # from 0..100 to 255..0
	img = numpy.array(img, numpy.uint8)
	Image.frombuffer('L',  (map_width, map_height), img, 'raw', 'L', 0, 1).show()

	# Start localization to navigate in map
	navigation_service.startLocalization()
	# Come back to initial position
	navigation_service.navigateToInMap([0., 0., 0.])
	# Retrieve and display the map built by the robot
	result_map = navigation_service.getMetricalMap()

	prompt = "Enter Co-ordinate (format = x/y/z): "
	while True:
		try:
			lists = raw_input(prompt)
		except NameError:
			lists = input(prompt)

		x, y, z = lists.split("/")
		navigation_service.navigateToInMap([float(x), float(y), float(z)], _async=True)


	''' show the map on tablet 
    	map_width = result_map[1]
    	map_height = result_map[2]
    	img = numpy.array(result_map[4]).reshape(map_width, map_height)
    	img = (100 - img) * 2.55 # from 0..100 to 255..0
    	img = numpy.array(img, numpy.uint8)

    	#Image.frombuffer('L',  (map_width, map_height), img, 'raw', 'L', 0, 1).show()
        
	shape = img.shape
        img = img.transpose((1, 0, 2)) # Do not transpose the channels.
        shape = img.shape
        # png
        flag, buff = cv2.imencode(".png", img)
        #print "Flag " + str(flag)

        # base 64
        buff64 = base64.b64encode(buff)
        self.logger.warning("")
        full = "data:image/png;base64," + buff64
        self.logger.warning(full)

        # show app
        self.mem.raiseEvent("Navigation/displayMap", full)
        time.sleep(5)
	'''
    	
	# Stop localization
    	navigation_service.stopLocalization()


if __name__ == "__main__":
    	parser = argparse.ArgumentParser()
    	parser.add_argument("--ip", type=str, default="127.0.0.1",
    	                    help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    	parser.add_argument("--port", type=int, default=9559,
    	                    help="Naoqi port number")

    	args = parser.parse_args()
    	session = qi.Session()
    	try:
    	    session.connect("tcp://" + args.ip + ":" + str(args.port))
    	except RuntimeError:
    	    print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
    	           "Please check your script arguments. Run with -h option for help.")
    	    sys.exit(1)
    	main(session)

