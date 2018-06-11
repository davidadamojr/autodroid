#!/bin/bash

function start_appium {
    source ~/.nvm/nvm.sh && \
    source ~/.profile && \
    source ~/.bashrc && \
    nvm use node && \
    appium > appium.log &
}

function start_autodroid {
    export PYTHONPATH=$PYTHONPATH:appiumatic
    source venv/bin/activate && \
    python3 main.py
}

TEST_SUITES_TO_GENERATE=$1
TEST_SUITES_GENERATED=0
while [ $TEST_SUITES_GENERATED -lt $TEST_SUITES_TO_GENERATE ]
do
    start_appium
    sleep 20
    start_autodroid
    killall node
    ((TEST_SUITES_GENERATED++))
done
