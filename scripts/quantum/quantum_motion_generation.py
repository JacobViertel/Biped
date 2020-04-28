#!/usr/bin/env python
from subprocess import call
import sys
import csv

import rospy
import time
from dynamixel_msgs.msg import JointState
from std_msgs.msg import Float64
from std_msgs.msg import String
import os

# factor_vel_mood_pub = rospy.Publisher('/factor_vel_mood', Float64, queue_size = 10)

def callback(data):
    x = data.data
    z = call("python3.7 /home/biped/catkin_ws/src/jacob/scripts/qiskit/qmg.py {}".format(x), shell=True)

def internal_state():
	rospy.init_node('quantum_motion_generation', anonymous=True)
	rospy.Subscriber('/motion_name', String, callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		internal_state()
	except rospy.ROSInterruptException:
		pass