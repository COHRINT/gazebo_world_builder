#!/bin/bash

#Author: Sierra Williams
#Date Created: 07/12/16
#Date Modeified: 07/12/16

clear
# 3 arguments can go here (png of map, nodeFileName, nodePublishRate)
python road_net.py &

python ../src/roadnet_sensor.py &

python ../src/hero_pose_generator.py &

sleep 15

python ../src/intruder_pose_generator.py 