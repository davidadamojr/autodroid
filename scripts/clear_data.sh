#!/bin/bash

# clear SD card data

ADB_PATH=$1
$ADB_PATH shell rm -rf /mnt/sdcard/*


