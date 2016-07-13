#!/usr/bin/env python

#Author: Sierra Williams
#Date Created: 07/06/16
#Date Modeified: 07/11/16

### What script does ###
# Send Goal poses to Hero and Intruder #
# listen to intruder sensor topic #
# get coordinated of node from json script #
# Publish goal poses #

import sys
import rospy
import logging
import json
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import random


def callback(data):
	data = str(data)
	nodeNumber = data.split('_')[1]
	# Grab JSON node positions
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
	i=0
	for key, value in pos.iteritems():
		node_pose.insert(i, ((value[0]*.15), (value[1]*.15)))
		i += 1

	Goal_hero = str(node_pose[int(nodeNumber)-1])

	talker_hero(Goal_hero)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('/tripped_pressure_sensor', String, callback)
	rospy.spin()

     
def talker_hero(msgHero):
	x_goal = msgHero.split(',')[0].split('(')[1]
	y_goal = msgHero.split(',')[1].split(')')[0]
	move_base_goal = PoseStamped()
	pubHero = rospy.Publisher('/hero/move_base_simple/goal', PoseStamped, queue_size=10)
	rospy.loginfo("Goal Pose: (%s, %s)"%(x_goal, y_goal))
	move_base_goal.pose.position.x = float(x_goal)
	move_base_goal.pose.position.y = float(y_goal)
	move_base_goal.pose.orientation.x = 0.0
	move_base_goal.pose.orientation.y = 0.0
	move_base_goal.pose.orientation.z = 0.0
	move_base_goal.pose.orientation.w = 1.0
	move_base_goal.header.frame_id = '/map'
	move_base_goal.header.stamp = rospy.Time.now()
	pubHero.publish(move_base_goal)


if __name__ == '__main__' :
	listener()
