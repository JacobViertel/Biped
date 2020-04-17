#!/usr/bin/env python

import rospy
import time
from dynamixel_msgs.msg import JointState
from std_msgs.msg import Float64
from std_msgs.msg import String
import os

factor_vel_mood_pub = rospy.Publisher('/factor_vel_mood', Float64, queue_size = 10)

def callback(data):
    fac_mood = data.data
    if fac_mood == 0:
        fac_mood = 0.75
        print "sending small fac"
    else:
        # send factor 1 to combined 
        print "sending norm fac"
        factor = 1.00  
    factor_vel_mood_pub.publish(fac_mood)

def internal_state():
	rospy.init_node('classical_mood', anonymous=True)
	rospy.Subscriber('/cl_mood', Float64, callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		internal_state()
	except rospy.ROSInterruptException:
		pass