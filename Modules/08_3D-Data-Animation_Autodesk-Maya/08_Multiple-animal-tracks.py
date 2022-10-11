import pymel.core as pm # To load in the Python PyMel core for Maya - allows python code to control Maya
import maya.cmds as cmds # To load in Maya-specific commands (will not work outside of Maya): https://help.autodesk.com/cloudhelp/2018/ENU/Maya-Tech-Docs/Commands/index.html
import csv # To load in CSV data
import sys # To check package versions  
import math 

#############################################
#Defining two variables which will be used as indices where animation starts and ends 
START = 0  #start time in sec
END = 50000   #end time in sec

track_fs = 1 # Track Data sampling frequency (in Hz or "samples per second")
rotationswim_fs = 10 # Swim Rotation Data Sampling frequency (in Hz or "samples per second")


# FOR WHALE 55 - BODHICHITA (green)
pivot_object1 = pm.ls('humpback_NBS_0003:PIVOT')[0]
placer_object1 = pm.ls('humpback_NBS_0003:PLACER')[0] 
swim_object1 = pm.ls('humpback_NBS_0003:SWIM_CONTROL')[0]

# FOR WHALE 58 - APOLLO11 (dark blue)
pivot_object2 = pm.ls('humpback_NBS_0004:PIVOT')[0]
placer_object2 = pm.ls('humpback_NBS_0004:PLACER')[0] 
swim_object2 = pm.ls('humpback_NBS_0004:SWIM_CONTROL')[0]

# FOR WHALE 99 - YIN YANG (yellow)
pivot_object3 = pm.ls('humpback_NBS_0005:PIVOT')[0]
placer_object3 = pm.ls('humpback_NBS_0005:PLACER')[0] 
swim_object3 = pm.ls('humpback_NBS_0005:SWIM_CONTROL')[0]

# FOR WHALE 95 - FIRST BUBBLE BLOWER - BERCHERVILLE (light blue)
pivot_object4 = pm.ls('humpback_NBS_0001:PIVOT')[0]
placer_object4 = pm.ls('humpback_NBS_0001:PLACER')[0] 
swim_object4 = pm.ls('humpback_NBS_0001:SWIM_CONTROL')[0]
bubbles_object4 = pm.ls('humpback_NBS_0001:bubbles.rat')[0]

# FOR WHALE 97 - SECOND BUBBLE BLOWER - EPIMELETIC (pink)
pivot_object5 = pm.ls('humpback_NBS_0002:PIVOT')[0]
placer_object5 = pm.ls('humpback_NBS_0002:PLACER')[0] 
swim_object5 = pm.ls('humpback_NBS_0002:SWIM_CONTROL')[0]
bubbles_object5 = pm.ls('humpback_NBS_0002:bubbles.rat')[0]

# DELETE EXISTING KEYFRAMES
pm.cutKey(pivot_object1, time = (0,END * track_fs))
pm.cutKey(swim_object1, time = (0,END * track_fs))
pm.cutKey(placer_object1, time = (0,END * track_fs))

pm.cutKey(pivot_object2, time = (0,END * track_fs))
pm.cutKey(swim_object2, time = (0,END * track_fs))
pm.cutKey(placer_object2, time = (0,END * track_fs))

pm.cutKey(pivot_object3, time = (0,END * track_fs))
pm.cutKey(swim_object3, time = (0,END * track_fs))
pm.cutKey(placer_object3, time = (0,END * track_fs))

pm.cutKey(pivot_object4, time = (0,END * track_fs))
pm.cutKey(swim_object4, time = (0,END * track_fs))
pm.cutKey(placer_object4, time = (0,END * track_fs))
pm.cutKey(bubbles_object4, time = (0,END * track_fs))

pm.cutKey(pivot_object5, time = (0,END * track_fs))
pm.cutKey(swim_object5, time = (0,END * track_fs))
pm.cutKey(placer_object5, time = (0,END * track_fs))
pm.cutKey(bubbles_object5, time = (0,END * track_fs))

#Change rotation order to match scientific conventions: 
# FIRST: heading (y-axis in Maya)
# SECOND: pitch (z- or x-axis in Maya depending on model)
# THIRD: roll (x- or z-axis in Maya depending on model)
# Maya applies these right to left so select mode 3 for XZY
cmds.setAttr(placer_object1+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)
cmds.setAttr(pivot_object1+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)
cmds.setAttr(placer_object2+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)
cmds.setAttr(pivot_object2+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)
cmds.setAttr(placer_object3+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)
cmds.setAttr(pivot_object3+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)
cmds.setAttr(placer_object4+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)
cmds.setAttr(pivot_object4+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)
cmds.setAttr(placer_object5+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)
cmds.setAttr(pivot_object5+".rotateOrder", 3) # (0=XYZ, 1=YZX, 2=ZXY, 3=XZY, 4=YXZ, 5=ZYX)



t1 = -2 * 180/math.pi
print(f'time elapsed = {t1}')

with open('G:/My Drive/Visualization/Data/08_Bubble-Nets_LBAS_01_ALLWHALES_1Hz.csv') as trackcsv_file:
    with open('G:/My Drive/Visualization/Data/08_Bubble-Nets_LBAS_01_ALLWHALES_10Hz.csv') as rotationswimcsv_file:
        
        trackreader = csv.DictReader(trackcsv_file)
        row_count = 0

        for row in trackreader: #for row in reader:
            
            if row_count == 0:
                origin_time = float(row['DN']) * 86400
            
            #We will use the function float() to return floating point numbers (with decimals) for data values
            secs_elapsed = float(row['DN'])*86400 - origin_time # Seconds elapsed
            time = secs_elapsed * (24) #Get time into frames for setting keyframes
            
            # DECIDE WHAT WHALE TO CONTROL ---------------------------------------------
            whaleName = row['whaleName']
            if whaleName == 'mn210614-55': # BODHICHITA - green
                pivot_object = pivot_object1
                placer_object = placer_object1
                swim_object = swim_object1
            elif whaleName == 'mn210614-58': # APOLLO11 - dark blue
                pivot_object = pivot_object2
                placer_object = placer_object2
                swim_object = swim_object2
            elif whaleName == 'mn210614-99': # YIN YANG - yellow
                pivot_object = pivot_object3
                placer_object = placer_object3
                swim_object = swim_object3
            elif whaleName == 'mn210614-95': # BERCHERVILLE - light blue
                pivot_object = pivot_object4
                placer_object = placer_object4
                swim_object = swim_object4
                bubbles_object = bubbles_object4
            elif whaleName == 'mn210614-97': # EPIMELETIC - pink
                pivot_object = pivot_object5
                placer_object = placer_object5
                swim_object = swim_object5
                bubbles_object = bubbles_object5
            else:
                print(f'whale not found')
            # --------------------------------------------------------------------------
            
            if row_count == 0:
                origin_x = float(row['x_fix'])
                origin_z = float(row['y_fix'])

            if row_count >= START*track_fs and row_count < END*track_fs: 
                x = float(row['x_finefix']) - origin_x # units = scene units (meters if changed, otherwise default is centimeters)
                y = -float(row['z'])  # NOTICE THAT y and z axis conventions are switched (Maya uses y up)
                z = float(row['y_finefix']) - origin_z
                
                placer_object.translateX.setKey(value=x, time=time) # Moving forward at 1m/s
                placer_object.translateY.setKey(value=y, time=time) # given Y is vertical axis, this is depth
                placer_object.translateZ.setKey(value=z, time=time) # Y and Z defined above  

            if row_count == 2000000 * track_fs: # STOP AT ROW 100
                break
            row_count += 1
            
            print(f'setting x = {x}, y = {y}, z = {z} for time = {time}')
                     
        rotationswimreader = csv.DictReader(rotationswimcsv_file)
        row_count = 0
        
        for row in rotationswimreader: #for row in reader:
            if row_count == 0:
                origin_time = float(row['DN']) * 86400
            
            whaleName = row['whaleName']
            if whaleName == 'mn210614-55': # BODHICHITA - green
                pivot_object = pivot_object1
                placer_object = placer_object1
                swim_object = swim_object1
            elif whaleName == 'mn210614-58': # APOLLO11 - dark blue
                pivot_object = pivot_object2
                placer_object = placer_object2
                swim_object = swim_object2
            elif whaleName == 'mn210614-99': # YIN YANG - yellow
                pivot_object = pivot_object3
                placer_object = placer_object3
                swim_object = swim_object3
            elif whaleName == 'mn210614-95': # BERCHERVILLE - light blue
                pivot_object = pivot_object4
                placer_object = placer_object4
                swim_object = swim_object4
                bubbles_object = bubbles_object4
            elif whaleName == 'mn210614-97': # EPIMELETIC - pink
                pivot_object = pivot_object5
                placer_object = placer_object5
                swim_object = swim_object5
                bubbles_object = bubbles_object5
            else:
                print(f'whale not found')
            # --------------------------------------------------------------------------
            
            #We will use the function float() to return floating point numbers (with decimals) for data values
            secs_elapsed = float(row['DN'])*86400 - origin_time # Seconds elapsed
            time = secs_elapsed * (24) #Get time into frames for setting keyframes                                                    
    
            yRot = float(row['head']) * 180/math.pi
            xRot = -float(row['pitch']) * 180/math.pi # to get from radians to degrees
            zRot = float(row['roll']) * 180/math.pi # to get from radians to degrees
            
            glide = float(row['Glide_Controller'])
            swim_stroke = int(row['Stroke_Detected'])

            placer_object.rotateY.setKey(value=yRot, time=time, inTangentType = 'stepnext', outTangentType = 'step')
            pivot_object.rotateZ.setKey(value=zRot, time=time, inTangentType = 'stepnext', outTangentType = 'step')
            pivot_object.rotateX.setKey(value=xRot, time=time, inTangentType = 'stepnext', outTangentType = 'step')

            swim_object.glide.setKey(value=glide, time=time)
            
            
            if swim_stroke:
                swim_object.swim.setKey(value=0, time=time)
                swim_object.swim.setKey(value=1, time=time - .001)
                pm.keyTangent(swim_object.swim, inTangentType='linear', outTangentType='linear', time=(time - .001, time))
            
            bubblefactor=1000
            if whaleName == 'mn210614-95' or whaleName == 'mn210614-97' :
                bubbles_object.setKey(value=bubblefactor*float(row['Bubble_Controller']), time=time, inTangentType = 'stepnext', outTangentType = 'step')
                
            
            if row_count == 2000000 * rotationswim_fs : # STOP AT ROW 100
                break

            print(f'setting whaleName = {whaleName} swim = {swim_stroke}, glide = {glide}, heading = {yRot}, pitch = {xRot}, roll = {zRot} for time = {time}')
            row_count += 1
    