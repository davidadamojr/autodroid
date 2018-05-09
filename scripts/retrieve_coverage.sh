#!/bin/bash

# retrieve_coverage - a shell script to retrieve a coverage.ec file from the android device, rename the coverage file and then remove if from the device

ADB_PATH=$1
DEVICE_PATH=$2
COVERAGE_PATH=$3
COVERAGE_NAME=$4
BROADCAST=$5

$ADB_PATH shell am broadcast -a $BROADCAST && \
sleep 2 && \
$ADB_PATH pull $DEVICE_PATH $COVERAGE_PATH && \
mv $COVERAGE_PATH'/coverage.ec' $COVERAGE_PATH'/'$COVERAGE_NAME && \
$ADB_PATH shell rm $DEVICE_PATH
