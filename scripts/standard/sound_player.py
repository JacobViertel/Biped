#!/usr/bin/env python

import rospy
import time
from dynamixel_msgs.msg import JointState
from std_msgs.msg import UInt8
from std_msgs.msg import Float64
from std_msgs.msg import String
import os
from math import log
from playsound import playsound
from subprocess import call
import sys

global in_action
in_action = 0


def callback(data):
    x = data.data
    z = call("python2.7 /home/biped/catkin_ws/src/jacob/scripts/speech/play_sound.py {}".format(x), shell=True)
    
# call back function for the keyboard/key topic subscribe
def keyboard_capture(data):
	global button
	button = data.code

def battery_manager():
	rospy.init_node('sound_player', anonymous=True)
	rospy.Subscriber('/play_quantum_motion', String, callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		battery_manager()
	except rospy.ROSInterruptException:
		pass