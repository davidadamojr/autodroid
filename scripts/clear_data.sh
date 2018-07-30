#!/bin/bash

# clear SD card data

ADB_PATH=$1
DEVICE_ID=$2
$ADB_PATH -s $DEVICE_ID shell rm -rf /mnt/sdcard/*


