#!/usr/bin/env python

#Author: Sierra Williams
#Date Created: 07/26/16
#Date Modeified: 07/28/16

### What script needs to do ###
#Stop robots#

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
import rospkg

def callback_hero(data_hero):
	x_hero = float(data_hero.pose.pose.position.x)
	y_hero = float(data_hero.pose.pose.position.y)
	orientation_hero  = float(data_hero.pose.pose.orientation.w)
	talker_hero(x_hero, y_hero, orientation_hero)

def callback_intruder(data_intruder):
	x_intruder = float(data_intruder.pose.pose.position.x)
	y_intruder = float(data_intruder.pose.pose.position.y)
	orientation_intruder  = float(data_intruder.pose.pose.orientation.w)
	talker_intruder(x_intruder, y_intruder, orientation_intruder)

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('/hero/odom', Odometry, callback_hero)
	rospy.Subscriber('/intruder/odom', Odometry, callback_intruder)
	rospy.spin()

     
def talker_hero(x_goal, y_goal, orientation_goal):
	move_base_goal = PoseStamped()
	pubHero = rospy.Publisher('/hero/move_base_simple/goal', PoseStamped, queue_size=10)
	rospy.Rate = 25.0
	move_base_goal.pose.position.x = x_goal
	move_base_goal.pose.position.y = y_goal
	move_base_goal.pose.orientation.x = 0.0
	move_base_goal.pose.orientation.y = 0.0
	move_base_goal.pose.orientation.z = 0.0
	move_base_goal.pose.orientation.w = orientation_goal
	move_base_goal.header.frame_id = '/map'
	move_base_goal.header.stamp = rospy.Time.now()
	pubHero.publish(move_base_goal)

def talker_intruder(x_goal, y_goal, orientation_goal):
	move_base_goal = PoseStamped()
	pubIntruder = rospy.Publisher('/intruder/move_base_simple/goal', PoseStamped, queue_size=10)
	rospy.Rate = 25.0
	move_base_goal.pose.position.x = x_goal
	move_base_goal.pose.position.y = y_goal
	move_base_goal.pose.orientation.x = 0.0
	move_base_goal.pose.orientation.y = 0.0
	move_base_goal.pose.orientation.z = 0.0
	move_base_goal.pose.orientation.w = orientation_goal
	move_base_goal.header.frame_id = '/map'
	move_base_goal.header.stamp = rospy.Time.now()
	pubIntruder.publish(move_base_goal)


if __name__ == '__main__' :
	listener()