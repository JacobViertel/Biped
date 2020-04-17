#!/usr/bin/env python

import rospy
import time
from dynamixel_msgs.msg import JointState
from std_msgs.msg import Float64
from std_msgs.msg import String
import os

global in_action
in_action = 0

pub2 = rospy.Publisher('/left_shoulder_controller/command', Float64, queue_size=1)
pub3 = rospy.Publisher('/right_elbow_controller/command', Float64, queue_size=1)
pub4 = rospy.Publisher('/left_elbow_controller/command', Float64, queue_size=1)
pub5 = rospy.Publisher('/right_hand_controller/command', Float64, queue_size=1)
pub6 = rospy.Publisher('/left_hand_controller/command', Float64, queue_size=1)
pub19 = rospy.Publisher('/neck_controller/command', Float64, queue_size=1)
# pub1 = rospy.Publisher('/right_shoulder_controller/command', Float64, queue_size=1)
# pub7 = rospy.Publisher('/right_hip_turn_controller/command', Float64, queue_size=1)
# pub8 = rospy.Publisher('/left_hip_turn_controller/command', Float64, queue_size=1)
# pub9 = rospy.Publisher('/right_hip_shake_controller/command', Float64, queue_size=1)
# pub10 = rospy.Publisher('/left_hip_shake_controller/command', Float64, queue_size=1)
# pub11 = rospy.Publisher('/right_hip_bend_controller/command', Float64, queue_size=1)
# pub12 = rospy.Publisher('/left_hip_bend_controller/command', Float64, queue_size=1)
# pub13 = rospy.Publisher('/right_knee_controller/command', Float64, queue_size=1)
# pub14 = rospy.Publisher('/left_knee_controller/command', Float64, queue_size=1)
# pub15 = rospy.Publisher('/right_ankle_controller/command', Float64, queue_size=1)
# pub16 = rospy.Publisher('/left_ankle_controller/command', Float64, queue_size=1)
# pub17 = rospy.Publisher('/right_foot_controller/command', Float64, queue_size=1)
# pub18 = rospy.Publisher('/left_foot_controller/command', Float64, queue_size=1)
# pub20 = rospy.Publisher('/head_controller/command', Float64, queue_size=1)

def motion_play(data):
	global in_action
	if in_action == 0:
		in_action = 1
		
		homedir = os.environ['HOME']
		filepath = homedir + "/catkin_ws/src/jacob/motions/" + data.data + ".txt"  
		try:
			with open(filepath) as f:
				content = f.readlines()
				# you may also want to remove whitespace characters like `\n` at the end of each line
				content = [x.strip('\n') for x in content]

				print "playing " + data.data + " motion"
				print(len(content))
				for i in range (0, len(content)):
					joint_positions = content[i].split(",")
					delay = joint_positions[6]
					del joint_positions[6]

					pub2.publish(float(joint_positions[0]))
					pub3.publish(float(joint_positions[1]))
					pub4.publish(float(joint_positions[2]))
					pub5.publish(float(joint_positions[3]))
					pub6.publish(float(joint_positions[4]))
					pub19.publish(float(joint_positions[5]))
											
					rospy.sleep(float(delay))
				in_action = 0
				print "motion is done"
		except:
			in_action = 0
			print "motion file doens't exist"
	else:
		print "The robot can't play this motion because it is playing another motion. Wait until the motion is done."
			
# call back function for the keyboard/key topic subscribe
def keyboard_capture(data):
	global button
	button = data.code

def motion_control():
	rospy.init_node('motion_player', anonymous=True)
	rospy.Subscriber('/play_motion', String, motion_play)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		motion_control()
	except rospy.ROSInterruptException:
		pass