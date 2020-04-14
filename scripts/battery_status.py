#!/usr/bin/env python

import rospy
import time
from dynamixel_msgs.msg import JointState
from std_msgs.msg import UInt8
from std_msgs.msg import Float64
from std_msgs.msg import String
import os
from math import log

global in_action
in_action = 0


factor_vel_bat_pub = rospy.Publisher('/factor_vel_bat', Float64, queue_size = 10)

def callback(data):
	max = 6.644
	min = 4.322
	range = max - min
	th_batt = 0.5
	batt_status = 0.0
	# print ("we got something as String: ") + data.data
	name = data.data
	# print ("we got something as name saved ") + name
	# print type(name)
	batt_int = int(name)
	# print ("we got something as Int: ")
	# print type(batt_int)
	# print batt_int 
	# print ("we got something as Int: ")
	# print log(batt_int,2)
	# print ("Factor for vel: ")
	batt_status = (log(batt_int,2)-min)/(range)
	if batt_status < th_batt:
		print th_batt
	else:
		print batt_status
	factor_vel_bat_pub.publish(batt_status)


# call back function for the keyboard/key topic subscribe
def keyboard_capture(data):
	global button
	button = data.code

def battery_manager():
	rospy.init_node('battery_status', anonymous=True)
	rospy.Subscriber('/battery_stat', String, callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		battery_manager()
	except rospy.ROSInterruptException:
		pass