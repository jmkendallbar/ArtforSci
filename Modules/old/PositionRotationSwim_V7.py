# To add packages added through Anaconda 
# sys.path.append ("c:/programdata/anaconda3/lib/site-packages")
# Maya 2023 uses Python3

# TROUBLESHOOTING Python coding issues in Maya: syntax errors often are caused by switching Python versions, issues with indenting (tabs are not always = to 4 spaces)

import pymel.core as pm # To load in the Python PyMel core for Maya - allows python code to control Maya
import maya.cmds as cmds # To load in Maya-specific commands (will not work outside of Maya): https://help.autodesk.com/cloudhelp/2018/ENU/Maya-Tech-Docs/Commands/index.html
import csv # To load in CSV data
import sys # To check package versions  
import math 

# Based on this tutorial for scripting in Maya: https://www.youtube.com/watch?v=eXFGeZZbMzQ

# FILEPATH: G:/My Drive/Visualization/Data/
############################################################################################

# FILENAMES: 
#    HIGH-RES HEART & BRAIN DATA: 
# 04_Sleep-at-Sea_JKB_00_test33_HypoactiveHeidi_09_ECGEEGs_JKB_100Hz_AnimExcerpt.csv

#    HYPNOTRACK (Sleep code, 3D position & rotation): 
# 04_Sleep-at-Sea_JKB_00_test33_HypoactiveHeidi_09_Hypnotrack_JKB_1Hz_AnimExcerpt.csv

#    SWIMMING & HR (Detected strokes, Detected heartbeats, 3D rotation): 
# 04_Sleep-at-Sea_JKB_00_test33_HypoactiveHeidi_05_ALL_PROCESSED_Trimmed_10Hz_AnimExcerpt.csv

#    Heartbeat Data (1 row per heart beat):
# 04_Sleep-at-Sea_JKB_00_test33_HypoactiveHeidi_SleepDives_HRbeats.csv
    

# SET UP COLOR SHADERS ------------------------------------------------------------------
def create_shader(name, node_type="lambert"):
    material = cmds.shadingNode(node_type, name=name, asShader=True)
    sg = cmds.sets(name="%sSG" % name, empty=True, renderable=True, noSurfaceShader=True)
    cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
    return material, sg
    
AWcolor  = [63/255, 73/255, 153/255] # dark blue
QWcolor = [77/255, 126/255, 179/255] # lighter blue
SWScolor = [128/255, 183/255, 242/255] # lightest blue
REMcolor = [245/255, 215/255, 66/255] # orange yellow

mtl_SWS, SWS = create_shader("SWS")
cmds.setAttr(mtl_SWS + ".color", SWScolor[0], SWScolor[1], SWScolor[2], type="double3")
mtl_AW, AW = create_shader("AW")
cmds.setAttr(mtl_AW + ".color", AWcolor[0], AWcolor[1], AWcolor[2], type="double3")
mtl_QW, QW = create_shader("QW")
cmds.setAttr(mtl_QW + ".color", QWcolor[0], QWcolor[1], QWcolor[2], type="double3")
mtl_REM, REM = create_shader("REM")
cmds.setAttr(mtl_REM + ".color", REMcolor[0], REMcolor[1], REMcolor[2], type="double3")
# ---------------------------------------------------------------------------------------
    
## Clear all existing cubes in list
cubeList = cmds.ls('myCube*') # get a list of all objects beginning with 'myCube...'
if len(cubeList ) > 0: # if there are objects beginning with 'myCube...'
    cmds.delete(cubeList) # delete those objects to start fresh.

## Create a cube polygon
result = cmds.polyCube (w=0.5, h=3, d=1, name='myCube#') # make a cube with these dimensions
print('result: ' + str(result)) 

# Get transform name for cube polygon and create a group 
transformName = result[0] # get name of transform node for the cube
instanceGroupName = cmds.group(empty=True, name=transformName + '_instance_grp#') 

track_fs = 1 # Track Data sampling frequency (in Hz or "samples per second")
rotationswim_fs = 10 # Swim Rotation Data Sampling frequency (in Hz or "samples per second")

# PART ONE -- PREVIEW YOUR TRACK DATA. This creates a track made out of spheres for the first 100 rows of your track data.

# Open TRACK data file (with 3D position) & refer to it as trackcsv_file
with open('G:/My Drive/Visualization/Data/04_Sleep-at-Sea_JKB_00_test33_HypoactiveHeidi_09_Hypnotrack_JKB_1Hz_AnimExcerpt.csv') as trackcsv_file:
    
    trackreader = csv.DictReader(trackcsv_file)
    row_count = 0
    for row in trackreader: #for row in reader:
        if row_count == 0:
            origin_x = float(row['x'])
            origin_z = float(row['y'])

        row_count += 1
        instanceResult = cmds.instance(transformName, name=transformName + '_instance#')
        cmds.parent(instanceResult, instanceGroupName) # Parent all of your cubes into the instance group
        x = float(row['x']) - origin_x # units = scene units (meters if changed, otherwise default is centimeters)
        y = float(row['z'])  # NOTICE THAT y and z axis conventions are switched (Maya uses y up)
        z = float(row['y']) - origin_z
        cmds.move(x,y,z,instanceResult)
        xRot = float(row['pitch']) * (180/math.pi) # to get from radians to degrees
        yRot = 0 # NOT exactly heading because heading is the direction of your pitched and rolled object (not the z rotation)
        zRot = float(row['roll']) * (180/math.pi) # to get from radians to degrees
        # IF YOU WANTED TO ROTATE YOUR CUBE, you could use something like this:
        cmds.rotate(xRot, yRot, zRot, instanceResult)
        
        # TO ADD COLORS TO YOUR CUBES ---------------------------------------------
        SleepStage = row['Simple_Sleep_Code']
        if SleepStage == 'Slow Wave Sleep':
            cmds.sets(instanceResult, forceElement=SWS)
        elif SleepStage == 'Active Waking':
            cmds.sets(instanceResult, forceElement=AW)
        elif SleepStage == 'Quiet Waking':
            cmds.sets(instanceResult, forceElement=QW)
        else:
            cmds.sets(instanceResult, forceElement=REM)
        # --------------------------------------------------------------------------

        if row_count == 100: # STOP AT ROW 100
            break
        print('instanceResult: ' + str(instanceResult))
        # The following print syntax works in Python 3 but not 2
        print(f'setting x = {x} y = {y} z = {z} for row = {row_count},' \
        f'pitch= {xRot} roll = {zRot} yRotation = {yRot} for instanceResult = {instanceResult} and color = {SleepStage}')
        
cmds.hide(transformName)

## Clear cubes to start fresh with whole track
cubeList = cmds.ls('myCube*') # get a list of all objects beginning with 'myCube...'
if len(cubeList ) > 0: # if there are objects beginning with 'myCube...'
    cmds.delete(cubeList) # delete those objects to start fresh.

# Open TRACK data file (with 3D position) & refer to it as trackcsv_file
with open('G:/My Drive/Visualization/Data/04_Sleep-at-Sea_JKB_00_test33_HypoactiveHeidi_09_Hypnotrack_JKB_1Hz_AnimExcerpt.csv') as trackcsv_file:
    
    trackreader = csv.DictReader(trackcsv_file)
    row_count = 0
    for row in trackreader: #for row in reader:
        if row_count == 0:
            origin_x = float(row['x'])
            origin_z = float(row['y'])
        row_count += 1
        instanceResult = cmds.instance(transformName, name=transformName + '_instance#')
        cmds.parent(instanceResult, instanceGroupName) # Parent all of your cubes into the instance group
        x = float(row['x']) - origin_x # units = scene units (meters if changed, otherwise default is centimeters)
        y = float(row['z'])  # NOTICE THAT y and z axis conventions are switched (Maya uses y up)
        z = float(row['y']) - origin_z
        cmds.move(x,y,z,instanceResult)
        xRot = float(row['pitch']) * (180/math.pi) # to get from radians to degrees
        yRot = 0 # NOT exactly heading because heading is the direction of your pitched and rolled object (not the z rotation)
        zRot = float(row['roll']) * (180/math.pi) # to get from radians to degrees
        # IF YOU WANTED TO ROTATE YOUR CUBE, you could use something like this:
        cmds.rotate(xRot, yRot, zRot, instanceResult)
        if row_count == 100: # STOP AT ROW 100
            break
        print('instanceResult: ' + str(instanceResult))
        # The following print syntax works in Python 3 but not 2
        print(f'setting x = {x} y = {y} z = {z} for row = {row_count},' \
        f'pitch= {xRot} roll = {zRot} yRotation = {yRot}')

# Defining two variables which will be used as indices where animation starts and ends 
START = 0    # start time in sec
END = 3084   # end time in sec

with open('G:/My Drive/Visualization/Data/04_Sleep-at_Sea_JKB_00_test33_HypoactiveHeidi_05_ALL_PROCESSED_Trimmed.csv') as csv_file:
    
    data = csv.reader(csv_file, delimiter=',')
    
    
    
#Defining two variables which will be used as indices where animation starts and ends 
START = 0  #start time in sec
END = 3084   #end time in sec

fs = 10 #Sample frequency (in Hz or "samples per second") #16 fs for Gitte's data

SECONDS = 0
ECG = 1
PITCH_DEG = 2
ROLL_DEG = 3
HEAD_DEG = 4
GYRO_Z = 5
GLIDE = 6
DEPTH = 7
HEART_RATE = 8
STROKE_RATE = 9
COMMENT = 10
HEARTBEATDETECTED = 11
STROKE = 12


#For loop runs through all rows in data .csv file
for i, row in enumerate(data):
if i % 1 == 0:
    
    #print('Processing row %s' % (i)) #Print progress in with data row counter in console to keep track of if/where code gets stuck
    
    #If the row number is between the start and end indices of where we want to animate, run this code.        
    if i >= START*fs and i < END*fs: 
        instanceResult = cmds.instance(transformName, name=transformName + '_instance#')
        
        x = float(row[PITCH_DEG]) 
        cmds.move(x,y,z,instanceResult)
        cmds.rotate(xRot, yRot, zRot, instanceResult)
    
    #We will use the function float() to return floating point numbers (with decimals) for data values
        time = float(i) / fs - START #Translate .csv data time into animation time
        time = time * fs #Get from frames to seconds
     
        depth_value      = -float(row[DEPTH])
        head_value = float(row[HEAD_DEG]) 
     
        #Define which object will be transformed according to data (use name as described in "Outliner")
        object = pm.ls('ESEAL_PLACER')[0] 
         
        #..setKey function sets a keyframe of the given value at the given time.
        # IF HAVE NO translate data
        # object.translateX.setKey(value=2*(-time/fs), time=time) # Moving forward at 1m/s
        # object.translateY.setKey(value=2*depth_value, time=time)
        object.rotateY.setKey(value=head_value, time=time)
     
        pitch_value = -float(row[PITCH_DEG]) 
        roll_value  = -float(row[ROLL_DEG])
        
        object = pm.ls('ESEAL_PIVOT')[0]
        
        object.rotateZ.setKey(value=pitch_value, time=time)
        object.rotateX.setKey(value=roll_value, time=time)
        
        object = pm.ls('SWIM_CONTROL')[0]
        
        glide = float(row[GLIDE])
        object.glide.setKey(value=glide, time=time)
        
        swim_stroke = int(row[STROKE])
        if swim_stroke:
            object.swim.setKey(value=0, time=time)
            object.swim.setKey(value=1, time=time - .001)
            pm.keyTangent(object.swim, inTangentType='linear', outTangentType='linear', time=(time - .001, time))
        
        print('setting swim = %s, glide = %s, y= %s units, pitch= %s, roll = %s for time= %s frames' % (swim_stroke, glide, depth_value , pitch_value , roll_value , time))
        