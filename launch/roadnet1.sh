#!/bin/bash

#Author: Sierra Williams
#Date Created: 07/12/16
#Date Modeified: 07/12/16

clear
# 4 arguments can go here (png of map, nodeFileName, nodePublishRate, launch file)
python road_net.py roadnet1_blk.png roadnet1_blk.json 0.5 road_net2.launch &

python ../src/roadnet_sensor.py &

python ../src/hero_pose_generator.py roadnet1_blk.json &

sleep 10

python ../src/intruder_pose_generator.py roadnet1_blk.json  &

python ../src/intruderCaught.py