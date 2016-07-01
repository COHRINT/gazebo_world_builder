#!/usr/bin/env python

#Author: Sierra Williams
#Date Created: 06/22/16
#Date Modeified: 06/30/16

import sys
import shutil
import os
import json


if len(sys.argv) > 1:
	fileName = sys.argv[1]
else: 
	fileName = "roadnet1_blk.png"

shutil.copy("/home/sierra/p3catkinws/src/gazebo_world_builder/maps/%s"%(fileName), "/home/sierra/.gazebo/models/road_net_visual/"\
	"materials/textures/")

#for fileName in os.listdir("/home/sierra/.gazebo/models/road_net_visual/materials/textures/"):
src = "/home/sierra/.gazebo/models/road_net_visual/materials/textures/%s"%(fileName)
dest = "/home/sierra/.gazebo/models/road_net_visual/materials/textures/roadnet1.png"
os.rename(src, dest)

#Get node and robot positions for models
with open('/home/sierra/p3catkinws/src/self_confidence/Road_Network_POMDPX/node_position.json') as position_file:
	position = json.load(position_file)
# Force nodes in order 
numbermap = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13}
keys = sorted(position.keys(), key=numbermap.__getitem__)
pos = {}
i=0
for key in keys:
	pos[i] = position[key]
	i += 1


# Extract values in nodes
node = []
i=0
for key, value in pos.iteritems():
	node.insert(i,'-x %s -y %s' % (value[0], value[1]))
	i += 1

# Launch ROS
os.system("roslaunch /home/sierra/p3catkinws/src/gazebo_world_builder/launch/road_net2.launch node_1:='%s' node_2:='%s' node_3:='%s'"\
	" node_4:='%s' node_5:='%s' node_6:='%s' node_7:='%s' node_8:='%s' node_9:='%s' node_10:='%s' node_11:='%s' node_12:='%s' node_13:='%s'" \
	% (node[0], node[1], node[2], node[3], node[4], node[5], node[6], node[7], node[8], node[9], node[10], node[11], node[12]))

