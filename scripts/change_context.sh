#!/bin/bash

# Get all parameters
ADB_PATH=$1
CH_ORIENTATION=$2
CH_POWER=$3
CH_INTERNET=$4
CH_BATTERY=$5

# change to landscape
if [[ CH_ORIENTATION -eq 1 ]];
then
  $ADB_PATH shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0
  $ADB_PATH shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:1
fi

# Change to portrait
if [[ CH_PORTRAIT -eq 0 ]];
then
  $ADB_PATH shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0
  $ADB_PATH  shell content insert --uri content://settings/system --bind name:s:user_rotation --bind value:i:0
fi

# power off
if [[ CH_POWER -eq 0 ]];
then
  $ADB_PATH shell dumpsys battery set ac 0
  $ADB_PATH shell settings put global heads_up_notifications_enabled 0
fi

# power on
if [[ CH_POWER -eq 1 ]];
then
  $ADB_PATH shell dumpsys battery set ac 1
fi

# Internet disable
if [[ CH_INTERNET -eq 0 ]];
then
  $ADB_PATH shell svc wifi disable
  $ADB_PATH shell svc data disable
fi

# Internet enable
if [[ CH_INTERNET -eq 1 ]];
then
  $ADB_PATH shell svc wifi enable
  $ADB_PATH shell svc data enable
fi

# Battery high
if [[ CH_BATTERY -eq 2 ]];
then
  $ADB_PATH shell dumpsys battery reset
fi

# Battery Okay
if [[ CH_BATTERY -eq 1 ]];
then
  $ADB_PATH shell dumpsys battery set level 50
fi

# Battery low 15%
if [[ CH_BATTERY -eq 0 ]];
then
  $ADB_PATH shell dumpsys battery set level 15
fi
