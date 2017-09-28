#!/bin/bash

ps T | grep 'node' | awk '{print $1}' | xargs kill