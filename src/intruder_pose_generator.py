#!/usr/bin/env python

#Author: Sierra Williams
#Date Created: 07/12/16
#Date Modeified: 07/12/16

### What script does ###
# Send Goal poses to Intruder#
# listen to topic to see if at goal pose #
# get coordinated of node from json script #
# Publish goal poses #

import sys
import rospy
import logging
import json
import os
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
import random
import rospkg
import numpy

def callback(data):
	x = float(data.pose.pose.position.x)
	y = float(data.pose.pose.position.y)
	Goal_intruder(x, y)

def Goal_intruder(pose_x, pose_y):
	if len(sys.argv) > 1:
		nodeFileName = sys.argv[1]

	else: 
		nodeFileName = "roadnet1_blk.json"
	# Get file paths
	rospack = rospkg.RosPack()
	package_path = rospack.get_path('gazebo_world_builder')
	
	with open('%s/models/node_info/%s'%(package_path, nodeFileName)) as position_file:
		nodeParameters = json.load(position_file)
	position = nodeParameters["pixel_positions"]
	new_pos = {}
	i = 0
	for key, value in position.iteritems():
		new_pos[int(position.keys()[i])] = position.values()[i]
		i += 1
	goal_pose = []
	x = []
	y = []
	i=0
	for key, value in new_pos.iteritems():
		goal_pose.insert(i, (value[0]*.15, value[1]*.15))
		x.insert(i, (value[0]*.15))
		y.insert(i, (value[1]*.15))
		i += 1

	for i in range(0, len(goal_pose)):
		dist_x = pose_x-x[i]
		dist_y = pose_y-y[i]
		dist = numpy.sqrt(pow(dist_x, 2)+pow(dist_y, 2))
		if (dist <= 1.2):
			Goal = str(goal_pose[random.randint(0, len(goal_pose)-1)])
			talker_intruder(Goal)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('/intruder/odom', Odometry, callback)
	rospy.spin()

def talker_intruder(msgIntuder):
	x_goal_intruder = msgIntuder.split(',')[0].split('(')[1]
	y_goal_intruder = msgIntuder.split(',')[1].split(')')[0]
	pubIntruder = rospy.Publisher('/intruder/move_base_simple/goal', PoseStamped, queue_size=10)
	rospy.Rate = 2.0
	move_base_goal_intruder = PoseStamped()
	# rospy.loginfo("Goal Pose for Intruder: (%s, %s)"%(x_goal_intruder, y_goal_intruder))
	move_base_goal_intruder.pose.position.x = float(x_goal_intruder)
	move_base_goal_intruder.pose.position.y = float(y_goal_intruder)
	move_base_goal_intruder.pose.orientation.x = 0.0
	move_base_goal_intruder.pose.orientation.y = 0.0
	move_base_goal_intruder.pose.orientation.z = 0.0
	move_base_goal_intruder.pose.orientation.w = 1.0
	move_base_goal_intruder.header.frame_id = '/map'
	move_base_goal_intruder.header.stamp = rospy.Time.now()
	pubIntruder.publish(move_base_goal_intruder)

if __name__ == '__main__' :
	listener()	

