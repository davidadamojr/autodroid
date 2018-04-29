#!/bin/bash

# clear adb logs from device

ADB_PATH=$1
$ADB_PATH logcat -c


