
__author__ = 'Leo Fabiano'
__author__ = 'Leo Fabiano'
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from naoqi import ALProxy
import cv2
import argparse
camera='camera'
photo='photo'
error='error'
from naoRobot import naoRobot
# Command ??
COMMAND_WAKEUP = 'WAKEUP'
COMMAND_REST = 'REST'
COMMAND_SIT='SIT'

COMMAND_FORWARD = 'FORWARD'
COMMAND_BACK = 'BACK'
COMMAND_LEFT = 'LEFT'
COMMAND_RIGHT = 'RIGHT'
COMMAND_STOP = 'STOP'

COMMAND_TURNLEFT = 'TURNLEFT'
COMMAND_TURNRIGHT = 'TURNRIGHT'

COMMAND_DISCONNECT = 'DISCONNECT'
COMMAND_SENSOR = 'SENSOR'
COMMAND_SAY = 'SAY'
COMMAND_HEADYAW = 'HEADYAW' 	# ???
COMMAND_HEADPITCH = 'HEADPITCH' # ???


from time import sleep
import base64

class SimpleEcho(WebSocket):
    global video
    def init(self,robot_IP='127.0.0.1',robot_PORT=9559):
        try:
            self.naoRobot=naoRobot(port=robot_PORT)
            print('New robot loaded')
        except:
            print('Filed to ini robot..')
            pass
    def handleMessage(self):
        # echo message back to client
        data=self.data.encode("utf-8")

        message= self.execCommand(data)

        '''
        ret, frame = self.video.read()

        ret, jpeg = cv2.imencode('.jpg', frame)
        encoded_string = base64.b64encode(jpeg.tobytes())
        print(encoded_string)
        cv2.imwrite('leo.jpg',frame)
        '''
        self.sendMessage(message)

    def handleConnected(self):
        print self.address, 'connected'
        self.init()

    def handleClose(self):
        self.naoRobot.stop()
        print self.address, 'closed'

    def getCommand(self,data):

        arg='none'
        command=data.split()
        cmd= command[0]
        print cmd
        if command.__len__()>1:  arg=command[1:]

        return cmd,arg

    def execCommand(self,cmd='none'):
        arg='none'

        cmd, arg =self.getCommand(cmd)
        print cmd,arg
        msg=''
        ok=self.naoRobot.Operation(cmd,arg)
        msg='cmd: '+ cmd + '-->' + ok

        return msg








'''
# Create a proxy to ALPhotoCapture
try:
  photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
except Exception, e:
  print "Error when creating ALPhotoCapture proxy:"
  print str(e)
  exit(1)
'''
def main(IP='127.0.0.1', PORT=8000):
    server = SimpleWebSocketServer('', PORT, SimpleEcho)
    server.serveforever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="Robot ip address")
    parser.add_argument("--port", type=int, default=8000, help="Robot port number")
    args = parser.parse_args()
    main(args.ip, args.port)