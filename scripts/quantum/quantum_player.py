#!/usr/bin/env python

import rospy
import time
from dynamixel_msgs.msg import JointState
from std_msgs.msg import Float64
from std_msgs.msg import String
import os


global is_moving
is_moving = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
global in_action
in_action = 0

qbbvpub = rospy.Publisher('/qbbv_player', String, queue_size = 10)
pub2 = rospy.Publisher('/left_shoulder_controller/command', Float64, queue_size = 10)
pub3 = rospy.Publisher('/right_elbow_controller/command', Float64, queue_size = 10)
pub4 = rospy.Publisher('/left_elbow_controller/command', Float64, queue_size = 10)
pub5 = rospy.Publisher('/right_hand_controller/command', Float64, queue_size = 10)
pub6 = rospy.Publisher('/left_hand_controller/command', Float64, queue_size = 10)
pub7 = rospy.Publisher('/right_rot_hip_controller/command', Float64, queue_size = 10)
pub8 = rospy.Publisher('/left_rot_hip_controller/command', Float64, queue_size = 10)
pub9 = rospy.Publisher('/right_tilt_hip_controller/command', Float64, queue_size = 10)
pub10 = rospy.Publisher('/left_tilt_hip_controller/command', Float64, queue_size = 10)
pub11 = rospy.Publisher('/right_lift_leg_controller/command', Float64, queue_size = 10)
pub12 = rospy.Publisher('/left_lift_leg_controller/command', Float64, queue_size = 10)
pub13 = rospy.Publisher('/right_knee_controller/command', Float64, queue_size = 10)
pub14 = rospy.Publisher('/left_knee_controller/command', Float64, queue_size = 10)
pub15 = rospy.Publisher('/right_lift_ankle_controller/command', Float64, queue_size = 10)
pub16 = rospy.Publisher('/left_lift_ankle_controller/command', Float64, queue_size = 10)
pub17 = rospy.Publisher('/right_rot_ankle_controller/command', Float64, queue_size = 10)
pub18 = rospy.Publisher('/left_rot_ankle_controller/command', Float64, queue_size = 10)
pub19 = rospy.Publisher('/neck_controller/command', Float64, queue_size = 10)

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
					# delay = joint_positions[6]
					# del joint_positions[6]
					pub2.publish(float(joint_positions[0]))
					pub3.publish(float(joint_positions[1]))
					pub4.publish(float(joint_positions[2]))
					pub5.publish(float(joint_positions[3]))
					pub6.publish(float(joint_positions[4]))
					pub7.publish(float(joint_positions[5]))
					pub8.publish(float(joint_positions[6]))
					pub9.publish(float(joint_positions[7]))
					pub10.publish(float(joint_positions[8]))
					pub11.publish(float(joint_positions[9]))
					pub12.publish(float(joint_positions[10]))
					pub13.publish(float(joint_positions[11]))
					pub14.publish(float(joint_positions[12]))
					pub15.publish(float(joint_positions[13]))
					pub16.publish(float(joint_positions[14]))
					pub17.publish(float(joint_positions[15]))
					pub18.publish(float(joint_positions[16]))
					pub19.publish(float(joint_positions[17]))
					delay = joint_positions[18]
					rospy.sleep(float(delay))
					global is_moving
					is_moving = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
					def left_shoulder_callback(data):
						global is_moving 
						is_moving[0]  = data.is_moving															
					def right_elbow_callback(data):
						global is_moving
						is_moving[1] = data.is_moving			
					def left_elbow_callback(data):
						global is_moving
						is_moving[2] = data.is_moving
					def right_hand_callback(data):
						global is_moving
						is_moving[3] = data.is_moving					
					def left_hand_callback(data):
						global is_moving
						is_moving[4] = data.is_moving
					def right_hip_turn_callback(data):
						global is_moving
						is_moving[5] = data.is_moving
					def left_hip_turn_callback(data):
						global is_moving
						is_moving[6] = data.is_moving
					def right_tilt_hip_callback(data):
						global is_moving
						is_moving[7] = data.is_moving
					def left_tilt_hip_callback(data):
						global is_moving
						is_moving[8] = data.is_moving
					def right_lift_leg_callback(data):
						global is_moving
						is_moving[9] = data.is_moving
					def left_lift_leg_callback(data):
						global is_moving
						is_moving[10] = data.is_moving
					def right_knee_callback(data):
						global is_moving
						is_moving[11] = data.is_moving
					def left_knee_callback(data):
						global is_moving
						is_moving[12] = data.is_moving
					def right_lift_ankle_callback(data):
						global is_moving
						is_moving[13] = data.is_moving
					def left_lift_ankle_callback(data):
						global is_moving
						is_moving[14] = data.is_moving
					def right_rot_ankle_callback(data):
						global is_moving
						is_moving[15] = data.is_moving
					def left_rot_ankle_callback(data):
						global is_moving
						is_moving[16] = data.is_moving																									
					def neck_callback(data):
						global is_moving
						is_moving[17] = data.is_moving
								
					rospy.Subscriber('/left_shoulder_controller/state', JointState, left_shoulder_callback)	
					rospy.Subscriber('/right_elbow_controller/state', JointState, right_elbow_callback)
					rospy.Subscriber('/left_elbow_controller/state', JointState, left_elbow_callback)
					rospy.Subscriber('/right_hand_controller/state', JointState, right_hand_callback)
					rospy.Subscriber('/left_hand_controller/state', JointState, left_hand_callback)
					rospy.Subscriber('/right_rot_hip_controller/state', JointState, right_hip_turn_callback)
					rospy.Subscriber('/left_rot_hip_controller/state', JointState, left_hip_turn_callback)
					rospy.Subscriber('/right_tilt_hip_controller/state', JointState, right_tilt_hip_callback)
					rospy.Subscriber('/left_tilt_hip_controller/state', JointState, left_tilt_hip_callback)
					rospy.Subscriber('/right_lift_leg_controller/state', JointState, right_lift_leg_callback)
					rospy.Subscriber('/left_lift_leg_controller/state', JointState, left_lift_leg_callback)
					rospy.Subscriber('/right_knee_controller/state', JointState, right_knee_callback)
					rospy.Subscriber('/left_knee_controller/state', JointState, left_knee_callback)
					rospy.Subscriber('/right_lift_ankle_controller/state', JointState, right_lift_ankle_callback)
					rospy.Subscriber('/left_lift_ankle_controller/state', JointState, left_lift_ankle_callback)
					rospy.Subscriber('/right_rot_ankle_controller/state', JointState, right_rot_ankle_callback)
					rospy.Subscriber('/left_rot_ankle_controller/state', JointState, left_rot_ankle_callback)
					rospy.Subscriber('/neck_controller/state', JointState, neck_callback)
					print("is_moving")
					with open ("/home/biped/catkin_ws/src/jacob/scripts/results/status.txt", "w") as fp:
						fp.write("is moving")
					# delay between motions
					while any(is_moving):
						rospy.sleep(0.05)
				in_action = 0
				print "motion is done"
				with open ("/home/biped/catkin_ws/src/jacob/scripts/results/status.txt", "w") as fp:
					fp.write("done")
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
	rospy.init_node('quantum_motion_player', anonymous=True)
	rospy.Subscriber('/play_quantum_motion', String, motion_play)
	rate = rospy.Rate(20)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		motion_control()
	except rospy.ROSInterruptException:
		pass