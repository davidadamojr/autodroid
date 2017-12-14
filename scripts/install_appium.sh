#!/bin/bash

sudo apt-get update && \
sudo apt-get install curl && \
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.4/install.sh | bash && \
source ~/.nvm/nvm.sh && \
source ~/.profile && \
source ~/.bashrc && \
nvm install 8.5.0 && \
npm install -g appium@1.7.0