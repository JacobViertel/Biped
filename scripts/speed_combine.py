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

def bat_callback(msg):
	factor_batt = msg.data
	init_joint_spped = rospy.get_param("/left_elbow_controller/joint_speed")
	print "get_init_joint_spped"
	print init_joint_spped
	combined_joint_speed = init_joint_spped*factor_batt
	print "set combined speed"
	print combined_joint_speed
	rospy.set_param("/left_elbow_controller/joint_speed", combined_joint_speed)
	print "get_set_joint_spped"
	print rospy.get_param("/left_elbow_controller/joint_speed")

def mood_callback(msg):
	factor_batt = msg.data
	init_joint_spped = rospy.get_param("/left_elbow_controller/joint_speed")
	print "get_init_joint_spped"
	print init_joint_spped
	combined_joint_speed = init_joint_spped*factor_batt
	print "set combined speed"
	print combined_joint_speed
	rospy.set_param("/left_elbow_controller/joint_speed", combined_joint_speed)
	print "get_set_joint_spped"
	print rospy.get_param("/left_elbow_controller/joint_speed")


def speed_manager():
	rospy.init_node('speed_combine', anonymous=True)
	rospy.Subscriber('/factor_vel_bat', Float64, bat_callback)
	rospy.Subscriber('/factor_vel_mood', Float64, mood_callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		speed_manager()
	except rospy.ROSInterruptException:
		pass