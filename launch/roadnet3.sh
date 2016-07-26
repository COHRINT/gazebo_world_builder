#!/bin/bash

#Author: Sierra Williams
#Date Created: 07/12/16
#Date Modeified: 07/12/16

clear
# 4 arguments can go here (png of map, nodeFileName, nodePublishRate and launch file)
python road_net.py roadnet3_blk.png roadnet3_blk.json 0.5 road_net3.launch &

python ../src/roadnet_sensor.py &

# 1 Argument can go here (nodeFileName)
python ../src/hero_pose_generator.py roadnet3_blk.json &

sleep 15

# 1 Argument can go here (nodeFileName)
python ../src/intruder_pose_generator.py roadnet3_blk.json