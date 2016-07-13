#!/usr/bin/env python

#Author: Sierra Williams
#Date Created: 07/12/16
#Date Modeified: 07/12/16

### What script does ###
# Ends Simulation if hero caught intruder #

import sys
import rospy
import logging
import numpy
import message_filters
from nav_msgs.msg import Odometry

def callback(data_hero, data_intruder):
	print(data_hero)
	x_hero = int(data_hero.pose.pose.position.x)
	y_hero = int(data_hero.pose.pose.position.y)
	x_intruder = int(data_intruder.pose.pose.position.x)
	y_intruder = int(data_intruder.pose.pose.position.y)

	caught(x_hero, y_hero, x_intruder, y_intruder)

def caught(x_hero, y_hero, x_intruder, y_intruder):
	print("here")
	dist_x = x_hero-x_intruder
	dist_y = y_hero-y_intruder
	dist = sqrt(pow(dist_x, 2)+pow(dist_y, 2))
	if (dist <= 1.5):
		rospy.loginfo("The simulation is over the Hero has caught the intruder")
		sys.exit()

def listener():
	rospy.init_node('listener', anonymous=True)
	# rospy.Subscriber('/intruder/odom', Odometry, callback_intruder)
	# rospy.Subscriber('/hero/odom', Odometry, callback_hero)
	data_hero = message_filters.Subscriber('/hero/odom', Odometry)
	data_intruder = message_filters.Subscriber('/intruder/odom', Odometry)
	msg = message_filters.TimeSynchronizer([data_hero, data_intruder], 1)
	msg.registerCallback(callback)
	rospy.spin()

if __name__ == '__main__' :
	listener()