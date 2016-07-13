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
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
import random

def callback(data):
	x = int(data.pose.pose.position.x)
	y = int(data.pose.pose.position.y)
	pose = '(%s, %s)'%(str(x), str(y))
	Goal_intruder(pose)

def Goal_intruder(pose):
	nodeFileName = "roadnet1_blk.json"
	with open('/home/sierra/p3catkinws/src/self_confidence/Road_Network_POMDPX/%s'%(nodeFileName)) as position_file:
		nodeParameters = json.load(position_file)
	position = nodeParameters["pixel_positions"]
	numbermap = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13}
	keys = sorted(position.keys(), key=numbermap.__getitem__)
	pos = {}
	i=0
	for key in keys:
		pos[i] = position[key]
		i += 1
	node_pose = []
	goal_pose = []
	i=0
	for key, value in pos.iteritems():
		node_pose.insert(i, (int(value[0]*.15), int(value[1]*.15)))
		goal_pose.insert(i, (value[0]*.15, value[1]*.15))
		i += 1

	for i in range(0, len(node_pose)):
		# Need to make less exact 
		if (pose == str(node_pose[i])):
			Goal = str(goal_pose[random.randint(0, 12)])
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
	rospy.loginfo("Goal Pose for Intruder: (%s, %s)"%(x_goal_intruder, y_goal_intruder))
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

