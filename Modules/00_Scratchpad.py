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
SWScolor = [128/255, 203/255, 88/255] # lightest blue
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

## Create a cube polygon with these dimensions
result = cmds.polyCube (w=0.4, h=0.1, d=0.2, name='myCube#') # d = e seal width
cmds.setAttr(result[0]+'.rotateOrder', 3); # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)

print('result: ' + str(result)) 

# Get transform name for cube polygon and create a group 
transformName = result[0] # get name of transform node for the cube
instanceGroupName = cmds.group(empty=True, name=transformName + '_instance_grp#') 

track_fs = 1 # Track Data sampling frequency (in Hz or "samples per second")
rotationswim_fs = 10 # Swim Rotation Data Sampling frequency (in Hz or "samples per second")

# PART ONE -- PREVIEW YOUR TRACK DATA. This creates a track made out of spheres for the first 100 rows of your track data.

# Open TRACK data file (with 3D position) & refer to it as trackcsv_file

# with open('G:/My Drive/Visualization/Data/04_Sleep-at-Sea_JKB_00_test33_HypoactiveHeidi_09_Hypnotrack_JKB_1Hz_AnimExcerpt.csv') as trackcsv_file:
with open('G:/My Drive/Dissertation Sleep/Sleep_Analysis/Data/test33_HypoactiveHeidi_09_Hypnotrack_1Hz_All_Sleep_Spirals.csv') as trackcsv_file:
   
    trackreader = csv.DictReader(trackcsv_file)
    row_count = 0
    for row in trackreader: #for row in reader:
        if row_count == 0:
            origin_x = float(row['x'])
            origin_z = float(row['y'])

        
        instanceResult = cmds.instance(transformName, name=transformName + '_instance%s' % row)
        cmds.parent(instanceResult, instanceGroupName) # Parent all of your cubes into the instance group
        
        x = float(row['x']) - origin_x # units = scene units (meters if changed, otherwise default is centimeters)
        y = float(row['z'])  # NOTICE THAT y and z axis conventions are switched (Maya uses y up)
        z = float(row['y']) - origin_z
        cmds.move(x,y,z,instanceResult)
        zRot = -float(row['pitch']) * (180/math.pi) # to get from radians to degrees
        yRot = -float(row['heading']) * (180/math.pi) -90 # NOT exactly heading because heading is the direction of your pitched and rolled object (not the z rotation)
        xRot = -float(row['roll']) * (180/math.pi) # to get from radians to degrees
        # IF YOU WANTED TO ROTATE YOUR CUBE, you could use something like this:
        cmds.rotate(xRot, yRot, zRot, instanceResult)
        
        # TO ADD COLORS TO YOUR CUBES ---------------------------------------------
        SleepStage = row['Simple_Sleep_Code']
        if SleepStage == 'SWS':
            cmds.sets(instanceResult, forceElement=SWS)
        elif SleepStage == 'Active Waking':
            cmds.sets(instanceResult, forceElement=AW)
        elif SleepStage == 'Quiet Waking':
            cmds.sets(instanceResult, forceElement=QW)
        else:
            cmds.sets(instanceResult, forceElement=REM)
        # --------------------------------------------------------------------------

        if row_count == 2000: # STOP AT ROW 100
            break
        print('instanceResult: ' + str(instanceResult))
        # The following print syntax works in Python 3 but not 2
        #print(f'setting x = {x} y = {y} z = {z} for row = {row_count},' \
        #f'pitch= {xRot} roll = {zRot} yRotation = {yRot} for instanceResult = {instanceResult} and color = {SleepStage}')
        row_count += 1
cmds.hide(transformName)


        
#############################################
#Defining two variables which will be used as indices where animation starts and ends 
START = 0  #start time in sec
END = 3084   #end time in sec

track_fs = 1 # Track Data sampling frequency (in Hz or "samples per second")
rotationswim_fs = 10 # Swim Rotation Data Sampling frequency (in Hz or "samples per second")

pivot_object = pm.ls('ESEAL_PIVOT')[0]
placer_object = pm.ls('ESEAL_PLACER')[0] 
swim_object = pm.ls('SWIM_CONTROL')[0]

#Change rotation order to match scientific conventions: 
# FIRST: heading (y-axis in Maya)
# SECOND: pitch (z- or x-axis in Maya depending on model)
# THIRD: roll (x- or z-axis in Maya depending on model)
# Maya applies these right to left so select mode 3 for XZY
cmds.setAttr(placer_object+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)
cmds.setAttr(pivot_object+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)

cmds.cutKey( 'ESEAL_PLACER', time = (0,END * track_fs))
cmds.cutKey( 'ESEAL_PIVOT', time = (0,END * track_fs))
cmds.cutKey( 'SWIM_CONTROL', time = (0,END * track_fs))

with open('G:/My Drive/Visualization/Data/04_Sleep-at-Sea_JKB_00_test33_HypoactiveHeidi_09_Hypnotrack_JKB_1Hz_AnimExcerpt.csv') as trackcsv_file:
    with open('G:/My Drive/Visualization/Data/04_Sleep-at-Sea_JKB_00_test33_HypoactiveHeidi_05_ALL_PROCESSED_Trimmed_10Hz_AnimExcerpt.csv') as rotationswimcsv_file:
        
        trackreader = csv.DictReader(trackcsv_file)
        row_count = 0
        #If the row number is between the start and end indices of where we want to animate, run this code. 
        
        for row in trackreader: #for row in reader:
            #We will use the function float() to return floating point numbers (with decimals) for data values
            rows_elapsed = float(row_count) - START #Translate .csv data time into animation time
            time = rows_elapsed * (24/track_fs) #Get from frames to seconds
            if row_count == 0:
                origin_x = float(row['x'])
                origin_z = float(row['y'])

            if row_count >= START*track_fs and row_count < END*track_fs: 
                x = float(row['x']) - origin_x # units = scene units (meters if changed, otherwise default is centimeters)
                y = float(row['z'])  # NOTICE THAT y and z axis conventions are switched (Maya uses y up)
                z = float(row['y']) - origin_z
                
                placer_object.translateX.setKey(value=x, time=time) # Moving forward at 1m/s
                placer_object.translateY.setKey(value=y, time=time) # given Y is vertical axis, this is depth
                placer_object.translateZ.setKey(value=z, time=time) # Y and Z defined above  

            if row_count == 2000 * track_fs: # STOP AT ROW 100
                break
            row_count += 1
            
            print(f'setting x = {x}, y = {y}, z = {z} for time = {time}')
                
                
        rotationswimreader = csv.DictReader(rotationswimcsv_file)
        row_count = 0
        
        for row in rotationswimreader: #for row in reader:
            if row_count >= START*rotationswim_fs and row_count < END*rotationswim_fs: 
                #We will use the function float() to return floating point numbers (with decimals) for data values
                rows_elapsed = float(row_count) - START #Translate .csv data time into animation time
                time = rows_elapsed * (24/rotationswim_fs) #Get from frames to seconds
        
                yRot = -float(row['heading'])
                zRot = -float(row['pitch']) # to get from radians to degrees
                xRot = float(row['roll']) # to get from radians to degrees
                
                glide = float(row['Glide_Controller'])
                swim_stroke = int(row['Stroke_Detected'])

                placer_object.rotateY.setKey(value=yRot, time=time)
                pivot_object.rotateZ.setKey(value=zRot, time=time)
                pivot_object.rotateX.setKey(value=xRot, time=time)

                swim_object.glide.setKey(value=glide, time=time)
                
                if swim_stroke:
                    swim_object.swim.setKey(value=0, time=time)
                    swim_object.swim.setKey(value=1, time=time - .001)
                    pm.keyTangent(swim_object.swim, inTangentType='linear', outTangentType='linear', time=(time - .001, time))
                
                if row_count == 2000 *rotationswim_fs: # STOP AT ROW 100
                    break

                print(f'setting swim = {swim_stroke}, glide = {glide}, heading = {yRot}, pitch = {xRot}, roll = {zRot} for time = {time}')
                row_count += 1
    