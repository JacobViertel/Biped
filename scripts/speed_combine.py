#!/usr/bin/env python

import rospy
import time
from dynamixel_msgs.msg import JointState
from std_msgs.msg import UInt8
from std_msgs.msg import Float64
from std_msgs.msg import String
import os
from math import log
import rosservice

def callback(msg):
	factor_batt = msg.data
	print factor_batt
	init_joint_spped = rospy.get_param("/left_elbow_controller/joint_speed")
	print "init_joint_spped"
	print init_joint_spped
	print "combined speed"
	combined_joint_speed = init_joint_spped*factor_batt
	print combined_joint_speed
	rospy.set_param("/left_elbow_controller/joint_speed", combined_joint_speed)
	print "new_joint_spped"
	print rospy.get_param("/left_elbow_controller/joint_speed")


def speed_manager():
	rospy.init_node('speed_combine', anonymous=True)
	rospy.Subscriber('/factor_vel_bat', Float64, callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		speed_manager()
	except rospy.ROSInterruptException:
		pass