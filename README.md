# SPARCS AOS/LOS Display: Quick Start Guide
written by Ella Greetis 06-18-2025, updated 07-09-2025

### Device Purpose
This device is a countdown display for SPARCS Satellite Acquisition of Signal (AOS) and Loss of Signal (LOS). The user will SSH into the device, input AOS and LOS timestamps (in UTC time), and the device will count down to those times. 

### Device Overview: 
The AOS/LOS Display consists of a Raspberry Pi Model 3B+ and eight ELEGOO MAX7219 8x8 Display Modules (datasheet [here](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX7219-MAX7221.pdf)). To drive these modules, it uses the [Luma LED Matrix Library](https://github.com/rm-hull/luma.led_matrix/tree/main). The device is (at the time of writing this) connected to the RoverNetwork-2.4G wifi network (password ********) and has the IP address 192.168.1.18. For SSH purposes, the username is sparcsdisplay and the password is ***********. <br>
Passwords have been redacted in this README file, but can be seen in the Quick Start Guide in the IPL Google Drive, [here](https://docs.google.com/document/d/1rztsUWNQ_UNla__ePJH0NF1tjyUHg38vNBCQB7ZZ5wE/edit?usp=sharing).

## User Guide
To use the device, one must SSH into the Raspberry Pi. 
One way to do this is with an ethernet cable. attach the ethernet cable to your computer, configure the connection (i'm unsure if the Pi has a different ethernet IP address for each connection) and find the IP address of the pi. 
ssh into it wiht the command:
```
ssh sparcsdisplay@10.42.0.53

First, connect to the RoverNetwork-2.4G wifi network (password MoveOverRover) and open a terminal on your computer. Type the following command and hit enter: 
```
ssh sparcsdisplay@192.168.1.18
```
You'll be prompted to enter the password for the Pi, which is ****. 
Further reading about SSH can be found [here](https://www.raspberrypi.com/documentation/computers/remote-access.html) and [here](https://docs.google.com/document/d/17vDdfAY1T-HF58JBEjj63zTxyzmByy_IIiqRBDq_gu4/edit?tab=t.0#heading=h.i6cid8e0faes).
Once you've successfully SSH'd into the Pi, run the following commands in the terminal: 
```
cd main
source env/bin/activate
python3.11 withluma.py
```
The terminal will ask if you want verbose output. For a more accurate countdown, select no, as it takes extra time to print statements to the terminal. 
The terminal will then prompt you to enter the expected AOS and LOS timestamps in the form of: 
```
AOSyyyy/mm/dd/hh:mm:ss; LOSyyyy/mm/dd/hh:mm:ss
```
By default, the program will pick the first entry to display first. 
After these timestamps are entered, the display will count down the days, hours, minutes, seconds, and deciseconds until the AOS or LOS. Keep your computer powered on and the terminal open for as long as you wish to view the countdown. To stop the program, press Ctrl+C

// The following feature has not yet been implemented: <br>
At the initialization of the program, the screen will flash either "AOS" or "LOS" to let you know which it's counting towards. This will also be displayed when there is less than an hour to AOS/LOS, AKA when the first three digits on the display (d:hh) are zero. 

### Known Issues
- The device has a tendency to lose time noticeably over periods longer than a few minutes. This has been calibrated for slightly in code but should be improved upon by having the device periodically check in with the datetime object
- The device’s Center of Gravity does not allow the “feet” (the pieces at either side of the device which slide out at angles and allow it to sit, slanted slightly upward, on flat surfaces) to be set at shallow angles. In a future redesign, this should be rectified by eliminating the “feet” entirely and redesigning the bottom attachment points (where bolts hold the two main 3D-printed pieces of the body together) to always prop the device up at a slight angle. 
