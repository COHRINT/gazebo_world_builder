1#!/usr/bin/python2
import os, string, csv, random

#Make a world based on a few inputs
class MazeInfo(object):
    def __init__(self, m_mazeName, m_locFile):
        self.mazeName = m_mazeName #Will have sdf appended
        self.mazeLocs = self.readLocs(m_locFile)
        self.lastLoc = 0
        
    def readLocs(self, fileName):
        #Returns a list of (x,y) tuples
        file1 = open(fileName, 'rb')
        reader = csv.reader(file1)
        next(reader, None) #skip the header
        out = []
        index = 0
        for row in reader:
            #print "Object: %s " % (row[0])
            out.append((row[0], row[1]))
        file1.close()   # <---IMPORTANT
        return out
    
    def getLoc(self):
        loc = self.mazeLocs[self.lastLoc]
        self.lastLoc = self.lastLoc + 1

        floc = (float(loc[0]), float(loc[1]))
        return floc

    def resetLoc(self):
        self.lastLoc = 0
        
def readModels(fileName):
    #Returns a list of objects
    file1 = open(fileName, 'rb')
    reader = csv.reader(file1)
    next(reader, None) #skip the header
    out = []
    index = 0
    for row in reader:
        #print "Object: %s " % (row[0])
        out.append(row[0])
    file1.close()   # <---IMPORTANT
    return out

def getHeader():
    out = """
<launch>

  <!-- We resume the logic in empty_world.launch, changing only the name of the world to be launched -->
  <include file="$(find gazebo_ros)/launch/empty_world.launch">
  
    <!-- <arg name="world_name" value="$(find ramrod)/worlds/testImage.world"/>  -->
    <!-- Note: the world_name is with respect to GAZEBO_RESOURCE_PATH environmental variable -->
    <arg name="paused" value="false"/>
    <arg name="use_sim_time" value="true"/>
    <arg name="gui" value="true"/>
    <arg name="headless" value="false"/>
    <arg name="debug" value="false"/>
  </include>
"""
    return out

def getObject(modelName, x, y):
    out = """ <include file="model_spawn.gazebo.launch">
     <arg name="model_dbname" value="%s" />
     <arg name="model_position" value="-x %s -y %s -z 0.01 -R 0 -P 0 -Y -1.57" />
  </include >\n""" % (modelName, x, y)
    return out

def getRobot(robotNum, x, y):
    out = """<include file="$(find gazebo_plugins)/test/multi_robot_scenario/launch/pioneer3dx.gazebo.launch">
     <arg name="robot_name" value="r%d" />
     <arg name="robot_position" value="-x %s -y %s -z 0.01 -R 0 -P 0 -Y +1.57" />
   </include>\n""" % (robotNum, x, y)
    return out

def getMaze(mazeName, x, y):
    out = """ <include file="maze_spawn.gazebo.launch">
     <arg name="maze_name" value="%s"/>
     <arg name="maze_position" value="-x %f -y %f -z 0.01 -R 0 -P 0 -Y 1.57" />
  </include >\n""" % (mazeName, x, y)
    return out

def getMotionControl():
    out = """<include file="$(find basic_move_base)/launch/basic_move.launch"/>\n"""
    return out

def getMapserver(mazeName):
    out = """<node name="map_server" pkg="hri_map_server" type="map_server" args="$(find ramrod)/launch/%s.yaml" />\n""" % mazeName
    return out

def writeMapYaml(mazeName):
    f = open("%s.yaml" % mazeName, 'w')
    f.write("""image: ../maps/%s.pbm
resolution: 1.0
origin: [0.0, 0.0, 0.0]
occupied_thresh: 0.5
free_thresh: 0.5
negate: 0
mode: raw\n""" % (mazeName))
    f.close()
    

def main():
    robotNames = ['r0', 'r1','r2','r3']
    numRobots = [1,2,4]
    mazeWidth = 31
    numModels = 9
    
    mazes = [MazeInfo('maze_high', '../maps/locs_high.csv'),
             MazeInfo('maze_low','../maps/locs_low.csv')]
    
    models = readModels('../models/gazebo_models.csv')
    
    print 'Found %d models to use' % len(models)

    #Generate the maze.launch files to procedurally spawn everything
    
    for theMI in mazes:
        #Spawn the mapserver's description file for this maze
        writeMapYaml(theMI.mazeName)


        
        for robotCount in numRobots:
            launchName = "%s_%d.launch" % (theMI.mazeName, robotCount)
            theFile = open(launchName, 'w')
            #Reset the location list
            theMI.resetLoc()
            
            #Write header info
            theFile.write(getHeader())

            #Spawn the maze
            theFile.write(getMaze(theMI.mazeName, mazeWidth, 0))
            
            #Spawn the mapserver
            theFile.write(getMapserver(theMI.mazeName))

            #Spawn the motion controllers
            theFile.write(getMotionControl())
            
            #Spawn the robots
            for thisRobot in range(0,robotCount):
                robotLoc = theMI.getLoc()
                theFile.write(getRobot(thisRobot, robotLoc[0], robotLoc[1])) 


            #Get a subset of models to spawn

            objs = random.sample(xrange(len(models)), numModels)

            objFile = open('%s_%d_objs.csv' % (theMI.mazeName, robotCount), 'w')
            objFile.write('modelName, x, y\n')
            for theObj in objs:
                objLoc = theMI.getLoc()
                theFile.write(getObject(models[theObj], objLoc[0], objLoc[1]))
                objFile.write(models[theObj] + ',' + str(objLoc[0]) + ',' + str(objLoc[1]) + '\n') 
                #Write a simpler file with the objects and their locations
            objFile.close()
            #Write footer info
            theFile.write("</launch>\n")
    
    
if __name__ == "__main__":
    main()
