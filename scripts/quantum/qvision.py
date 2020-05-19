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
	x = data.data
	y = call("python /home/biped/catkin_ws/src/jacob/scripts/face_recog/recognize_faces_image.py {}".format(x), shell=True)
	z = call("python3.7 /home/biped/catkin_ws/src/jacob/scripts/qiskit/Grover_oracle.py {}".format(x), shell=True)
	
	with open("/home/biped/catkin_ws/src/jacob/scripts/results/qvision_output.csv", "r") as csv_file:
		csv_reader = csv.reader(csv_file)
		for line in csv_reader:
			result =  line[0]+line[1]

	print(result)		
	if result == "01":
		print("I see Jacob, I am happy")
		quantum_motion_pub.publish("happy")

	elif result == "10":
		print("I see Marek, I am afraid")
		quantum_motion_pub.publish("sad")

	else :
		print("I dont know you!")
		quantum_motion_pub.publish("sad")
			
def internal_state():
	rospy.init_node('qvision', anonymous=True)
	rospy.Subscriber('/qvision', String, callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		internal_state()
	except rospy.ROSInterruptException:
		pass