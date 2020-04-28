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

factor_vel_mood_pub = rospy.Publisher('/factor_vel_mood', String, queue_size = 10)

def callback(data):
    x = data.data
    z = call("python3.7 /home/biped/catkin_ws/src/jacob/scripts/qiskit/qpe_mood.py {}".format(x), shell=True)
    
    with open("/home/biped/catkin_ws/src/jacob/scripts/results/qpe_mood.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            init_mood = row[0]
    # good mood 
    def split(word):
        return [char for char in word]
    # print(split(init_mood)) 
    mood = init_mood[0]
    intensity = init_mood[1]+init_mood[2]
    # print(mood)
    # print(intensity)

    if intensity == "00":
        if mood == "1":
            max_value = 1
            min_value = 1
        else:
            max_value = 0.9
            min_value = 1.1
        fac_mood = 0.75
        # print fac_mood

    elif mood == "1":
        max_value = 1
        min_value = 1
        if intensity == "01":
            fac_mood = 0.80
            # print fac_mood
        else:
            fac_mood = 0.90
            # print fac_mood
    else:
        max_value = 0.9
        min_value = 1.1
        if intensity == "01":
            fac_mood = 0.70
            # print fac_mood
        else:
            fac_mood = 0.60
            # print fac_mood

    # get init params 
    lshou_speed = rospy.get_param("/left_shoulder_controller/joint_speed")
    maxlshou = rospy.get_param("/left_shoulder_controller/motor/max")
    minlshou = rospy.get_param("/left_shoulder_controller/motor/min")
    lelbow_speed = rospy.get_param("/left_elbow_controller/joint_speed")
    maxlelbow = rospy.get_param("/left_elbow_controller/motor/max")
    minlelbow = rospy.get_param("/left_elbow_controller/motor/min")
    lhand_speed = rospy.get_param("/left_hand_controller/joint_speed")
    maxlhand = rospy.get_param("/left_hand_controller/motor/max")
    minlhand = rospy.get_param("/left_hand_controller/motor/min")
    relbow_speed = rospy.get_param("/right_elbow_controller/joint_speed")
    maxrelbow = rospy.get_param("/right_elbow_controller/motor/max")
    minrelbow = rospy.get_param("/right_elbow_controller/motor/min")
    rhand_speed = rospy.get_param("/right_hand_controller/joint_speed")
    maxrhand = rospy.get_param("/right_hand_controller/motor/max")
    minrhand = rospy.get_param("/right_hand_controller/motor/min")
    neck_speed = rospy.get_param("/neck_controller/joint_speed")
    maxneck = rospy.get_param("/neck_controller/motor/max")
    minneck = rospy.get_param("/neck_controller/motor/min")

    # claculate new param according to mood 
    lshou_speed = lshou_speed*fac_mood
    maxlshou = maxlshou*max_value
    minlshou = minlshou*min_value
    lelbow_speed = lelbow_speed*fac_mood
    maxlelbow = maxlelbow*max_value
    minlelbow = minlelbow*min_value
    lhand_speed = lhand_speed*fac_mood
    maxlhand = maxlhand*max_value
    minlhand = minlhand*min_value
    relbow_speed = relbow_speed*fac_mood
    maxrelbow = maxrelbow*max_value
    minrelbow = minrelbow*min_value
    rhand_speed = rhand_speed*fac_mood
    maxrhand = maxrhand*max_value
    minrhand = minrhand*min_value
    neck_speed = neck_speed*fac_mood
    maxneck = maxneck*max_value
    minneck = minneck*min_value
    rospy.set_param("/left_shoulder_controller/joint_speed", lshou_speed)
    rospy.set_param("/left_shoulder_controller/motor/max",maxlshou)
    rospy.set_param("/left_shoulder_controller/motor/min",minlshou)
    rospy.set_param("/left_elbow_controller/joint_speed",lelbow_speed)
    rospy.set_param("/left_elbow_controller/motor/max",maxlelbow)
    rospy.set_param("/left_elbow_controller/motor/min",minlelbow)
    rospy.set_param("/left_hand_controller/joint_speed",lhand_speed)
    rospy.set_param("/left_hand_controller/motor/max",maxlhand)
    rospy.set_param("/left_hand_controller/motor/min",minlhand)
    rospy.set_param("/right_elbow_controller/joint_speed",relbow_speed)
    rospy.set_param("/right_elbow_controller/motor/max",maxrelbow)
    rospy.set_param("/right_elbow_controller/motor/min",minrelbow)
    rospy.set_param("/right_hand_controller/joint_speed",rhand_speed)
    rospy.set_param("/right_hand_controller/motor/max",maxrhand)
    rospy.set_param("/right_hand_controller/motor/min",minrhand)
    rospy.set_param("/neck_controller/joint_speed",neck_speed)
    rospy.set_param("/neck_controller/motor/max",maxneck)
    rospy.set_param("/neck_controller/motor/min",  minneck)
    print "Done!"
    

def internal_state():
	rospy.init_node('quantum_mood', anonymous=True)
	rospy.Subscriber('/q_mood', String, callback)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		internal_state()
	except rospy.ROSInterruptException:
		pass