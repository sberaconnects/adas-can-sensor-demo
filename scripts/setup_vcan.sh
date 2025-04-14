#!/bin/bash

# Load vcan module
sudo modprobe vcan

# Create virtual CAN interface
sudo ip link add dev vcan0 type vcan

# Bring it up
sudo ip link set up vcan0

# Confirm
echo "✅ vcan0 setup complete. Interfaces:"
ip a | grep vcan
