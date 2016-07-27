#!/usr/bin/env python

#Author: Sierra Williams
#Date Created: 06/27/16
#Date Modeified: 06/28/16

### What script needs to do ###
# Listen to pressure sensors #
# Check and see if hero is in the node range #
# if so publish nothing #
# Publish node number and position #
# When intruder gets to exit sensor end game #
## A possible issue is if both intruder and hero are on the smae node ##

import sys
import os
import rospy
import rospkg
import logging
from std_msgs.msg import String
from gazebo_msgs.msg import ContactsState

def callback_sensor(data):
	if len(data.states) > 0:
		msg = data.states[1]
		subject = msg.collision1_name.split(':')[0]
		nodeNumber = msg.collision2_name.split(':')[0]
		if subject == "husky_intruder":
			pub_msg = nodeNumber
			# rospy.loginfo(rospy.get_caller_id() + " The intruder is at %s"%(nodeNumber))
			talker(pub_msg)

def callback_exit(data):
	if len(data.states) > 0:
		msg = data.states[1]
		subject = msg.collision1_name.split(':')[0]
		if subject == "husky_intruder":
			print('exit')
			rospy.loginfo(rospy.get_caller_id() + "The intruder has reached the exit node.  The simulation is over.")
			#Stop simulation
			rospack = rospkg.RosPack()
			package_path = rospack.get_path('gazebo_world_builder')
			os.system("python %s/src/stop_sim.py" %(package_path))
			os.system("python stop_sim.py")

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('/pressure_plate_sensor', ContactsState, callback_sensor)
	rospy.Subscriber('/pressure_plate_exit', ContactsState, callback_exit)
	rospy.spin()

     
def talker(msg):
	pub = rospy.Publisher('/tripped_pressure_sensor', String, queue_size=10)
	# rospy.loginfo(msg)
	pub.publish(msg)

if __name__ == '__main__' :
	listener()
