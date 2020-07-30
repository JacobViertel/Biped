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
	y = call("python /home/biped/catkin_ws/src/jacob/scripts/prepross/ros_scan.py {}", shell=True)
	z = call("python3.7 /home/biped/catkin_ws/src/jacob/scripts/qiskit/Grover_oracle.py {}".format(x), shell=True)
	
	with open("/home/biped/catkin_ws/src/jacob/scripts/prepross/prediction_ip.csv", "r") as csv_file:
		csv_reader = csv.reader(csv_file)
		result =[]
		for line in csv_reader:
			result.append(line[2])

	print(type(result[0]))		
	if result[0] == "6":
		# print("I see Jacob, I am happy")
		quantum_motion_pub.publish("seesix")

	elif result[0] == "9":
		# print("I see Marek, I am afraid")
		quantum_motion_pub.publish("seenine")
	

# def callback(data):
    	# x= call("python /home/biped/catkin_ws/src/jacob/scripts/prepross/ros_scan.py {}", shell=True)
    	# with open('/home/biped/catkin_ws/src/jacob/scripts/prepross/test.csv') as f:
        	# csv_reader = csv.reader(f, delimiter=',')
			# 
		# print("hurensohn")
		# 
# with open('/home/biped/catkin_ws/src/jacob/scripts/prepross/test.csv') as csv_file:
    # csv_reader = csv.reader(csv_file, delimiter=',')
    # for row in csv_reader:
        # theta_test.append(row[1])
			
def internal_state():
	rospy.init_node('prepross', anonymous=True)
	rospy.Subscriber('/prepross', String, callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		internal_state()
	except rospy.ROSInterruptException:
		pass