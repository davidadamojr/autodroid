#!/bin/bash

# get process for package name

ADB_PATH=$1
PACKAGE_NAME=$2
DEVICE_ID=$3
$ADB_PATH -s $DEVICE_ID shell pidof -s $PACKAGE_NAME


