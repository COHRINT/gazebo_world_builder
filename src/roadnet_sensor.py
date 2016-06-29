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


import rospy
from std_msgs.msg import String

def callback_sensor(data):
	rospy.loginfo(rospy.get_caller_id() + "The intruder is at sensor node %s in position %s", data.node, data.position)
def callback_exit(data):
	rospy.loginfo(rospy.get_caller_id() + "The intruder has reached the exit node.  The simulation is over.")

def listener():
	rospy.iniy_node('listener', anonymous=True)
	# Before calling callbacks make sure to check that you are not reposrting on the hero
	rospy.Subscriber('SENSOR', String, callback_sensor)
	rospy.Subscriber('EXIT', String, callback_exit)
	rospy.spin()

def talker():
	pub = rospy.Publisher('tripped_pressure_sensor', String, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10) #rate at 10Hz PROBABLY NOT SOMETHING WE SHOULD HAVE

if __name__ == '__main__' :
	listener()
	try:
		talker()
	except rospy.ROSInterruptionException:
		pass