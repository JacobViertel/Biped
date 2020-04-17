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

factor_vel_mood_pub = rospy.Publisher('/factor_vel_mood', Float64, queue_size = 10)

def callback(data):
    x = data.data
    print type(x)
    z = call("python3.7 /home/biped/catkin_ws/src/jacob/scripts/qiskit/qpe_mood.py {}".format(x), shell=True)
    with open("/home/biped/catkin_ws/src/jacob/scripts/results/qpe_mood_result.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            init_mood = row[0]
    # good mood 
    print init_mood
    print type(init_mood)
    init_joint_spped = rospy.get_param("/left_elbow_controller/joint_speed")
    print init_joint_spped
	# print "get_init_joint_spped"
    if init_mood == "01":
        fac_mood = 0.85
        print fac_mood
    elif init_mood == "10":
        fac_mood = 0.85
        print fac_mood
    # exhausted mood 
    elif init_mood == "00":
        fac_mood = 0.75
        print fac_mood
    # happy mood    
    elif init_mood == "11":
        fac_mood = 1.00
        print fac_mood
    else:
        print "unkown state, please try again"  
    maxlshoulder = rospy.get_param("/left_shoulder_controller/motor/max")
    print maxlshoulder
	# print "max left shoulder init"
	# print max_l_shoulder
	# mooddep_l_shoulder = max_l_shoulder*fac_mood
	# print "set combined speed"
	# print mooddep_l_shoulder
	# rospy.set_param("/left_elbow_controller/motor/max", mooddep_l_shoulder)
	# print "new max l_shoulder"
	# print rospy.get_param("/left_elbow_controller/motor/max")

    print "Done!"
    factor_vel_mood_pub.publish(fac_mood)
    

def internal_state():
	rospy.init_node('quantum_mood', anonymous=True)
	rospy.Subscriber('/q_mood', Float64, callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		internal_state()
	except rospy.ROSInterruptException:
		pass