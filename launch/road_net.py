import sys
import shutil
import os

if len(sys.argv) > 1:
	fileName = sys.argv[1]
else: 
	fileName = "roadnet.png"

shutil.copy("/home/sierra/p3catkinws/src/gazebo_world_builder/maps/%s"%(fileName), "/home/sierra/.gazebo/models/road_net_visual/materials/textures/")

#for fileName in os.listdir("/home/sierra/.gazebo/models/road_net_visual/materials/textures/"):
src = "/home/sierra/.gazebo/models/road_net_visual/materials/textures/%s"%(fileName)
dest = "/home/sierra/.gazebo/models/road_net_visual/materials/textures/roadnet1.png"
os.rename(src, dest)

os.system("roslaunch /home/sierra/p3catkinws/src/gazebo_world_builder/launch/road_net2.launch")
