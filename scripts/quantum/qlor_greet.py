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

lor_motion_pub = rospy.Publisher('/play_quantum_motion', String, queue_size = 10)

def callback(data):
    x = data.data
    z = call("python3.7 /home/biped/catkin_ws/src/jacob/scripts/qiskit/l_r_greet.py {}".format(x), shell=True)
    with open("/home/biped/catkin_ws/src/jacob/scripts/results/l_r_greet_result.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            motion = row[0]
	name = ""
	print(motion)
	print(type(motion))
	if motion == "00":
		name = "left"
	elif motion == "01":
		name = "up"
	elif motion == "10":
		name = "down"
	elif motion == "11":
		name = "right"
	lor_motion_pub.publish(name)

def internal_state():
	rospy.init_node('lor_node', anonymous=True)
	rospy.Subscriber('/lor_handed', String, callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		internal_state()
	except rospy.ROSInterruptException:
		pass