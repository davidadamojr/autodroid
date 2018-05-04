#!/bin/bash

# retrieve adb logs with level WARNING and above

ADB_PATH=$1
LOG_FILE_PATH=$2
PROCESS_ID=$3

if [ "$PROCESS_ID" = "" ]
then
    $ADB_PATH logcat -d *:W > $LOG_FILE_PATH
else
    $ADB_PATH logcat -d *:W | grep $PROCESS_ID > $LOG_FILE_PATH
fi


