# Electronic Shelf Label (ESL) Hardware System

## Overview

This repository contains the software and hardware integration code for an Electronic Shelf Label system utilizing Raspberry Pi devices and RF24 wireless communication modules. This system is designed to provide real-time pricing updates to ESLs in a retail setting with a strong focus on power efficiency and reliability.

## System Architecture

### Components

- **Raspberry Pi 4 Model B**: Acts as the central server and access point within the store, handling data synchronization with the backend and broadcasting updates to ESLs.
- **Raspberry Pi Zero 2 with RF24**: Each ESL is powered by a Raspberry Pi Zero 2 equipped with an RF24 module, responsible for receiving data updates wirelessly and managing individual electronic shelf labels.
- **Backend Server**: A remote Node.js application that manages product pricing and information, providing APIs for data retrieval.

### Communication Flow

1. The backend server pushes updates to the Raspberry Pi 4.
2. The Raspberry Pi 4 broadcasts these updates using RF24 modules.
3. Raspberry Pi Zero 2 devices, each connected to an ESL, listen for updates at predefined intervals and update the display accordingly.

## Hardware Setup

1. **Raspberry Pi 4 Setup**:
   - Install Raspberry Pi OS.
   - Configure as a WiFi access point.
   - Install and configure RF24 libraries for broadcasting messages.

2. **Raspberry Pi Zero 2 Setup**:
   - Attach and configure the RF24 module.
   - Install necessary libraries to interface with ESL hardware.

3. **Connecting RF24 Modules**:
   - Diagram and instructions for connecting RF24 modules to Raspberry Pi GPIO pins.

## Software Installation

### Raspberry Pi 4
```bash
sudo apt-get update
sudo apt-get install git
git clone https://github.com/yourrepository/esl-hardware.git
cd esl-hardware/pi4
make install
```
### Raspberry Pi Zero 2
```bash
sudo apt-get update
sudo apt-get install git
git clone https://github.com/yourrepository/esl-hardware.git
cd esl-hardware/pi-zero-2
make install
```
