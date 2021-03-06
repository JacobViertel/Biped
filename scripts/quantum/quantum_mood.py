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
        fac_mood = 0.80
        # print fac_mood

    elif mood == "1":
        max_value = 1
        min_value = 1
        if intensity == "01":
            fac_mood = 0.90
            # print fac_mood
        else:
            fac_mood = 1.1
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

    rrh_speed = rospy.get_param("/right_rot_hip_controller/joint_speed")
    maxrrh = rospy.get_param("/right_rot_hip_controller/motor/max")
    minrrh = rospy.get_param("/right_rot_hip_controller/motor/min")
    lrh_speed = rospy.get_param("/left_rot_hip_controller/joint_speed")
    maxlrh = rospy.get_param("/left_rot_hip_controller/motor/max")
    minlrh = rospy.get_param("/left_rot_hip_controller/motor/min")
    rth_speed= rospy.get_param("/right_tilt_hip_controller/joint_speed")
    maxrth= rospy.get_param("/right_tilt_hip_controller/motor/max")
    minrth= rospy.get_param("/right_tilt_hip_controller/motor/min")
    lth_speed= rospy.get_param("/left_tilt_hip_controller/joint_speed")
    maxlth= rospy.get_param("/left_tilt_hip_controller/motor/max")
    minlth= rospy.get_param("/left_tilt_hip_controller/motor/min")
    rll_speed = rospy.get_param("/right_lift_leg_controller/joint_speed")
    maxrll = rospy.get_param("/right_lift_leg_controller/motor/max")
    minrll = rospy.get_param("/right_lift_leg_controller/motor/min")
    lll_speed = rospy.get_param("/left_lift_leg_controller/joint_speed")
    maxlll = rospy.get_param("/left_lift_leg_controller/motor/max")
    minlll = rospy.get_param("/left_lift_leg_controller/motor/min")
    rk_speed = rospy.get_param("/right_knee_controller/joint_speed")
    maxrk = rospy.get_param("/right_knee_controller/motor/max")
    minrk = rospy.get_param("/right_knee_controller/motor/min")
    lk_speed = rospy.get_param("/left_knee_controller/joint_speed")
    maxlk = rospy.get_param("/left_knee_controller/motor/max")
    minlk = rospy.get_param("/left_knee_controller/motor/min")
    rla_speed = rospy.get_param("/right_lift_ankle_controller/joint_speed")
    maxrla = rospy.get_param("/right_lift_ankle_controller/motor/max")
    minrla = rospy.get_param("/right_lift_ankle_controller/motor/min")
    lla_speed = rospy.get_param("/left_lift_ankle_controller/joint_speed")
    maxlla = rospy.get_param("/left_lift_ankle_controller/motor/max")
    minlla = rospy.get_param("/left_lift_ankle_controller/motor/min")
    rra_speed = rospy.get_param("/right_rot_ankle_controller/joint_speed")
    maxrra = rospy.get_param("/right_rot_ankle_controller/motor/max")
    minrra = rospy.get_param("/right_rot_ankle_controller/motor/min")
    lra_speed = rospy.get_param("/left_rot_ankle_controller/joint_speed")
    maxlra = rospy.get_param("/left_rot_ankle_controller/motor/max")
    minlra = rospy.get_param("/left_rot_ankle_controller/motor/min")


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

    rrh_speed = rrh_speed*fac_mood
    maxrrh = maxrrh*max_value
    minrrh = minrrh*min_value
    lrh_speed = lrh_speed*fac_mood
    maxlrh = maxlrh*max_value
    minlrh = minlrh*min_value
    rth_speed = rth_speed*fac_mood
    maxrth = maxrth*max_value
    minrth = minrth*min_value
    lth_speed = lth_speed*fac_mood
    maxlth = maxlth*max_value
    minlth = minlth*min_value
    rll_speed = rll_speed*fac_mood
    maxrll = maxrll*max_value
    minrll = minrll*min_value
    lll_speed = lll_speed*fac_mood
    maxlll = maxlll*max_value
    minlll = minlll*min_value
    rk_speed = rk_speed*fac_mood
    maxrk = maxrk*max_value
    minrk = minrk*min_value
    lk_speed = lk_speed*fac_mood
    maxlk = maxlk*max_value
    minlk = minlk*min_value
    rla_speed = rla_speed*fac_mood
    maxrla = maxrla*max_value
    minrla = minrla*min_value
    lla_speed = lla_speed*fac_mood
    maxlla = maxlla*max_value
    minlla = minlla*min_value
    rra_speed = rra_speed*fac_mood
    maxrra = maxrra*max_value
    minrra = minrra*min_value
    lra_speed = lra_speed*fac_mood
    maxlra = maxlra*max_value
    minlra = minlra*min_value






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

    rospy.set_param("/right_rot_hip_controller/joint_speed", rrh_speed)
    rospy.set_param("/right_rot_hip_controller/motor/max", maxrrh)
    rospy.set_param("/right_rot_hip_controller/motor/min", minrrh)
    rospy.set_param("/left_rot_hip_controller/joint_speed", lrh_speed)
    rospy.set_param("/left_rot_hip_controller/motor/max", maxlrh)
    rospy.set_param("/left_rot_hip_controller/motor/min", minlrh)
    rospy.set_param("/right_tilt_hip_controller/joint_speed", rth_speed)
    rospy.set_param("/right_tilt_hip_controller/motor/max", maxrth)
    rospy.set_param("/right_tilt_hip_controller/motor/min", minrth)
    rospy.set_param("/left_tilt_hip_controller/joint_speed", lth_speed)
    rospy.set_param("/left_tilt_hip_controller/motor/max", maxlth)
    rospy.set_param("/left_tilt_hip_controller/motor/min", minlth)
    rospy.set_param("/right_lift_leg_controller/joint_speed", rll_speed)
    rospy.set_param("/right_lift_leg_controller/motor/max", maxrll)
    rospy.set_param("/right_lift_leg_controller/motor/min", minrll)
    rospy.set_param("/left_lift_leg_controller/joint_speed", lll_speed)
    rospy.set_param("/left_lift_leg_controller/motor/max", maxlll)
    rospy.set_param("/left_lift_leg_controller/motor/min", minlll)
    rospy.set_param("/right_knee_controller/joint_speed", rk_speed)
    rospy.set_param("/right_knee_controller/motor/max", maxrk)
    rospy.set_param("/right_knee_controller/motor/min", minrk)
    rospy.set_param("/left_knee_controller/joint_speed", lk_speed)
    rospy.set_param("/left_knee_controller/motor/max", maxlk)
    rospy.set_param("/left_knee_controller/motor/min", minlk)
    rospy.set_param("/right_lift_ankle_controller/joint_speed", rla_speed)
    rospy.set_param("/right_lift_ankle_controller/motor/max", maxrla)
    rospy.set_param("/right_lift_ankle_controller/motor/min", minrla)
    rospy.set_param("/left_lift_ankle_controller/joint_speed", lla_speed)
    rospy.set_param("/left_lift_ankle_controller/motor/max", maxlla)
    rospy.set_param("/left_lift_ankle_controller/motor/min", minlla)
    rospy.set_param("/right_rot_ankle_controller/joint_speed", rra_speed)
    rospy.set_param("/right_rot_ankle_controller/motor/max", maxrra)
    rospy.set_param("/right_rot_ankle_controller/motor/min", minrra)
    rospy.set_param("/left_rot_ankle_controller/joint_speed", lra_speed)
    rospy.set_param("/left_rot_ankle_controller/motor/max", maxlra)
    rospy.set_param("/left_rot_ankle_controller/motor/min", minlra)



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