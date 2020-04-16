#!/usr/bin/env python
from subprocess import call
import sys

import rospy
import time
from dynamixel_msgs.msg import JointState
from std_msgs.msg import Float64
from std_msgs.msg import String
import os

factor_vel_mood_pub = rospy.Publisher('/factor_vel_mood', Float64, queue_size = 10)

def callback(data):
    x = data.data
    z = call("python3.7 /home/biped/catkin_ws/src/jacob/scripts/qpe_mood.py {}".format(x), shell=True)
    
    # f = open("qpe_mood_result.csv", "r")
    # content = f.read()
    # print(content)
    # fac_mood = data.data
    # if fac_mood == 0:
    #     fac_mood = 0.75
    #     print "sending small fac"
    # else:
    #     # send factor 1 to combined 
    #     print "sending norm fac"
    #     factor = 1  
    # factor_vel_mood_pub.publish(fac_mood)

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