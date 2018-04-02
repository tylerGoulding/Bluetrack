#!/bin/bash

sleep 10

set -x

export BLUETOOTH_DEVICE=hci0
export BID="00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02"


sudo hciconfig hci0 up
sudo hcitool -i $BLUETOOTH_DEVICE cmd 0x08 0x0008 1e 02 01 1a 1a ff 4c 00 02 15 $BID 00 00 00 00 c5 00 00 00 00 00 00 00 00 00 00 00 00 00
sudo hcitool -i $BLUETOOTH_DEVICE cmd 0x08 0x0006 A0 00 A0 00 03 00 00 00 00 00 00 00 00 07 00
sudo hcitool -i $BLUETOOTH_DEVICE cmd 0x08 0x000a 01
