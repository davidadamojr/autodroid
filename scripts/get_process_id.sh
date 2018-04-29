#!/bin/bash

# get process for package name

ADB_PATH=$1
PACKAGE_NAME=$2
$ADB_PATH shell pidof -s $PACKAGE_NAME


