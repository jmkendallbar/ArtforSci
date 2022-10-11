# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 18:26:07 2022

@author: jmkb9
"""

"""
LINKING HEART RATE DATA TO SOUND
Created on Tue May 18 10:35:14 2021

@author: Jessica Kendall-Bar
"""
#%%
# import libraries
import os
import pandas as pd
from psychopy import prefs, core, sound

# UPDATE ME
data_path = "G:/My Drive/Visualization/Data"

os.chdir(data_path)
os.getcwd()

# From this website https://mbraintrain.com/how-to-set-up-precise-sound-stimulation-with-psychopy-and-pylsl/
# Change the pref libraty to PTB (psychtoolbox) 
prefs.hardware['audioLib'] = 'PTB'
# Set the latency mode to high precision (3)
prefs.hardware['audioLatencyMode'] = 3

# Load in heartbeat sound
#badum_fast = sound.Sound('04_heart_badum-450ms.wav') #sound of heart beating
badum_slow = sound.Sound('04_heart_badum-730ms.wav') #sound of heart beating

# swish = sound.Sound('01 Tail Noise.wav') #sound of tail swishing back and forth
sound_dur_fast = 0.45 # second duration of sound file
sound_dur_slow = 0.73 # second duration of sound file

# Load in heartrate data (with array of interbeat intervals in seconds)
HR_data = pd.read_csv('08_Blue-Whale-HR_PP_01_HRdata.csv', sep=",", header=0, squeeze=True)

# After heartbeat plays, wait interval - duration of heartbeat until next.
HR_data['Wait'] = HR_data['Interval'] - sound_dur_slow

# Initializing wait variable with wait durations
wait = HR_data['Wait']

for i in range(0,len(wait)): # for all values in wait series
    playback_time = core.getTime() # get current time
    curr_time = core.getTime() - playback_time # get elapsed time
    while curr_time < wait[i]: # until it's time to play next heart beat
        curr_time = core.getTime() - playback_time # continue getting elapsed time
        print("Seconds since last heartbeat: %3.5f" %curr_time)
        core.wait(0.05) # wait 50 milliseconds
    badum_slow.play() # play next heartbeat
    # badum.setVolume(1.0)
    core.wait(sound_dur_slow) # determined by duration of heartbeat