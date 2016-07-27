#!/usr/bin/env python

#Author: Sierra Williams
#Date Created: 07/12/16
#Date Modeified: 07/13/16

### What script does ###
# Ends Simulation if hero caught intruder #

import sys
import os
import rospkg
import rospy
import logging
import numpy
from nav_msgs.msg import Odometry

class Robot(object):
	def __init__(self, x_pose, y_pose, type_flag):
		self.x_pose = x_pose
		self.y_pose = y_pose
		self.type_flag = type_flag

	def compare(self, other):
		if (self.type_flag != other.type_flag):
			dist_x = self.x_pose-other.x_pose
			dist_y = self.y_pose-other.y_pose
			dist = numpy.sqrt(pow(dist_x, 2)+pow(dist_y, 2))
			if (dist <= 2.5):
				rospy.loginfo("The simulation is over the hero has caught the intruder")
				rospack = rospkg.RosPack()
				package_path = rospack.get_path('gazebo_world_builder')
				os.system("python %s/src/stop_sim.py" %(package_path))

def callback_hero(data_hero, objects):
	hero = objects[0]
	intruder = objects[1]
	x_hero = float(data_hero.pose.pose.position.x)
	y_hero = float(data_hero.pose.pose.position.y)
	hero.x_pose = x_hero
	hero.y_pose = y_hero
	hero.compare(intruder)



def callback_intruder(data_intruder, objects):
	intruder = objects[0]
	hero = objects[1]
	x_intruder = float(data_intruder.pose.pose.position.x)
	y_intruder = float(data_intruder.pose.pose.position.y)
	intruder.x_pose = x_intruder
	intruder.y_pose = y_intruder
	intruder.compare(hero)

def listener():
	rospy.init_node('listener', anonymous=True)
	hero = Robot(0, 0, 'hero')
	intruder = Robot(0, 0, 'intruder')
	rospy.Subscriber('/hero/odom', Odometry, callback_hero, (hero,intruder))
	rospy.Subscriber('/intruder/odom', Odometry, callback_intruder, (intruder, hero))

	rospy.spin()

if __name__ == '__main__' :
	listener()