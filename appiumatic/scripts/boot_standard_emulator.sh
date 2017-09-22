SDK_PATH=$1
DEVICE_NAME=$2

$SDK_PATH/tools/emulator -avd $DEVICE_NAME -wipe-data -no-audio -writable-system