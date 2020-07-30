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

quantum_motion_pub = rospy.Publisher('/play_quantum_motion', String, queue_size = 10)


def callback(data):
    	while(1):
    			with open ("/home/biped/catkin_ws/src/jacob/scripts/results/status.txt", "w") as fp:
					fp.write("is moving")
			z = call("python /home/biped/catkin_ws/src/jacob/scripts/face_recog/recognize_faces_image.py {}", shell=True)
			x = call("python3.7 /home/biped/catkin_ws/src/jacob/scripts/qiskit/qbbv_qiskit.py {}", shell=True)
			quantum_motion_pub.publish("combined")
			f = open("/home/biped/catkin_ws/src/jacob/scripts/results/status.txt", "r")
			if f.read() == "finish":
    				break
			while(1):
    				f = open("/home/biped/catkin_ws/src/jacob/scripts/results/status.txt", "r")
				if f.read() == "done":
    					break
				else:
    					pass
			print("done waiting, ready for next move!")

def internal_state():
	rospy.init_node('qbbv', anonymous=True)
	rospy.Subscriber('/qbbv', String, callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		internal_state()
	except rospy.ROSInterruptException:
		pass