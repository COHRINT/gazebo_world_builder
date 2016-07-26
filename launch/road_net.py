#!/usr/bin/env python

#Author: Sierra Williams
#Date Created: 06/22/16
#Date Modeified: 07/06/16

import sys
import shutil
import os
import json
import rospkg

class numberOfNodes(object):
	def __init__(self, string, number):
		self.string = string
		self.number = number

if len(sys.argv) > 3:
	picName = sys.argv[1]
	nodeFileName = sys.argv[2]
	nodePublishRate = sys.argv[3]
	launch_file = sys.argv[4]

else: 
	picName = "roadnet3_blk.png"
	nodeFileName = "roadnet3_blk.json"
	nodePublishRate = "0.5"
	launch_file = "road_net3.launch"
#Pixel multipled by resolution or need more white around map	
mapy = 1000*0.15
mapx = 1000*0.15
mapModelSize = "-x %s -y %s"%(str(mapy), str(mapx))

# Get file paths
rospack = rospkg.RosPack()
package_path = rospack.get_path('gazebo_world_builder')
model_path = os.path.expanduser('~')

#Need to eventually make this pretty and clean and not calling my home directory
shutil.copy("%s/maps/%s"%(package_path, picName), "%s/.gazebo/models/road_net_visual/"\
	"materials/textures/"%(model_path))

src = "%s/.gazebo/models/road_net_visual/materials/textures/%s"%(model_path, picName)
dest = "%s/.gazebo/models/road_net_visual/materials/textures/roadnet.png"%(model_path)
os.rename(src, dest)

#Get node and robot positions for models
with open('%s/models/node_info/%s'%(package_path, nodeFileName)) as position_file:
	nodeParameters = json.load(position_file)

position = nodeParameters["pixel_positions"]
feature = nodeParameters["feature"]
# Force nodes in order 
new_pos = {}
i = 0
for key, value in position.iteritems():
	new_pos[int(position.keys()[i])] = position.values()[i]
	i += 1

new_features = {}
i = 0
for key, value in feature.iteritems():
	new_features[int(feature.keys()[i])] = feature.values()[i]
	i += 1

# Form Launch String
node = []
node_type = []
i=0
for key, value in new_pos.iteritems():
	node.insert(i,"node_%d:='-x %s -y %s'" % (i+1, value[0]*.15, value[1]*.15))
	i += 1
i=0
for key, value in new_features.iteritems():
	node_type.insert(i,"node_type_%d:='%s'" %(i+1, value))
	i += 1
s = " "
node_string = s.join(node)
node_type_string = s.join(node_type)

# Launch ROS
os.system("roslaunch /home/sierra/p3catkinws/src/gazebo_world_builder/launch/%s %s %s" %(launch_file, node_string, node_type_string))