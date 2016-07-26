#!/usr/bin/env python

#Author: Sierra Williams
#Date Created: 07/12/16
#Date Modeified: 07/13/16

### What script does ###
# Ends Simulation if hero caught intruder #

import sys
import rospy
import logging
import numpy
import message_filters
from nav_msgs.msg import Odometry

class Robot(object):
	def __init__(self, x_pose, y_pose):
		self.x_pose = x_pose
		self.y_pose = y_pose

	def compare(self, other):
		print("here")
		dist_x = self.x_pose-other.x_pose
		dist_y = self.y_pose-other.y_pose
		dist = sqrt(pow(dist_x, 2)+pow(dist_y, 2))
		if (dist <= 2.5):
			rospy.loginfo("The simulation is over the hero has caught the intruder")
			sys.exit()

def callback_hero(data_hero):
	x_hero = float(data_hero.pose.pose.position.x)
	y_hero = float(data_hero.pose.pose.position.y)
	hero = Robot(x_hero, y_hero)
	hero.compare()


def callback_intruder(data_intruder):
	x_intruder = float(data_intruder.pose.pose.position.x)
	y_intruder = float(data_intruder.pose.pose.position.y)
	intruder = Robot(x_intruder, y_intruder)
	intruder.compare()

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('/intruder/odom', Odometry, callback_intruder)
	rospy.Subscriber('/hero/odom', Odometry, callback_hero)
	rospy.spin()

if __name__ == '__main__' :
	listener()