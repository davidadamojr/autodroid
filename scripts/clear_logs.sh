#!/bin/bash

# clear adb logs from device

ADB_PATH=$1
DEVICE_ID=$2
$ADB_PATH -s $DEVICE_ID logcat -c


