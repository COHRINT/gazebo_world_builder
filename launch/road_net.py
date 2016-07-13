#!/usr/bin/env python

#Author: Sierra Williams
#Date Created: 06/22/16
#Date Modeified: 07/06/16

import sys
import shutil
import os
import json

# Things to change make node update rate, node number (Could be gross), mapModelSize a parameter in this script

# Instead if making nodes bigger make nodes white?

if len(sys.argv) > 3:
	picName = sys.argv[1]
	nodeFileName = sys.argv[2]
	nodePublishRate = sys.argv[3]

else: 
	picName = "roadnet1_blk.png"
	nodeFileName = "roadnet1_blk.json"
	nodePublishRate = "0.5"
#Pixel multipled by resolution or need more white around map	
mapy = 1000*0.15
mapx = 1000*0.15
mapModelSize = "-x %s -y %s"%(str(mapy), str(mapx))

#Need to eventually make this pretty and clean and not calling my home directory
shutil.copy("/home/sierra/p3catkinws/src/gazebo_world_builder/maps/%s"%(picName), "/home/sierra/.gazebo/models/road_net_visual/"\
	"materials/textures/")

src = "/home/sierra/.gazebo/models/road_net_visual/materials/textures/%s"%(picName)
dest = "/home/sierra/.gazebo/models/road_net_visual/materials/textures/roadnet1.png"
os.rename(src, dest)

#Get node and robot positions for models
with open('/home/sierra/p3catkinws/src/self_confidence/Road_Network_POMDPX/%s'%(nodeFileName)) as position_file:
	nodeParameters = json.load(position_file)

position = nodeParameters["pixel_positions"]
feature = nodeParameters["feature"]
# Force nodes in order 
numbermap = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12, '13': 13}
keys = sorted(position.keys(), key=numbermap.__getitem__)
key_feature = sorted(feature.keys(), key=numbermap.__getitem__)
features = {}
pos = {}
i=0
for key in keys:
	pos[i] = position[key]
	i += 1
i=0
for key in key_feature:
	features[i] = feature[key]
	i += 1

# Extract values in nodes
node = []
node_type = []
i=0
for key, value in pos.iteritems():
	node.insert(i,'-x %s -y %s' % (value[0]*.15, value[1]*.15))
	i += 1
i=0
for key, value in features.iteritems():	
	node_type.insert(i,value)
	i += 1

# Launch ROS
os.system("roslaunch /home/sierra/p3catkinws/src/gazebo_world_builder/launch/road_net2.launch node_1:='%s' node_2:='%s' node_3:='%s'"\
	" node_4:='%s' node_5:='%s' node_6:='%s' node_7:='%s' node_8:='%s' node_9:='%s' node_10:='%s' node_11:='%s' node_12:='%s' node_13:='%s'" \
	" node_type_1:='%s' node_type_2:='%s' node_type_3:='%s' node_type_4:='%s' node_type_5:='%s' node_type_6:='%s' node_type_7:='%s' node_type_8:='%s'"\
	" node_type_9:='%s' node_type_10:='%s' node_type_11:='%s' node_type_12:='%s' node_type_13:='%s'" % (node[0], node[1], node[2], node[3], node[4], \
	node[5], node[6], node[7], node[8], node[9], node[10], node[11], node[12], node_type[0], node_type[1], node_type[2], node_type[3], node_type[4], \
	node_type[5], node_type[6], node_type[7], node_type[8], node_type[9], node_type[10], node_type[11], node_type[12]))

