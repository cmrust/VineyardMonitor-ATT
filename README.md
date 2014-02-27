VineyardMonitor-ATT
====================

AT&T Hackathon Dallas 2014 M2X Category Winner

Overview
--------

This project was created for an entry to the AT&T Hackathon on Feb. 21 and 22nd in Dallas, TX.

This project was built from a [Sparkfun Inventor's Kit](https://www.sparkfun.com/products/12643) and a Raspberry Pi.

From the provided kit, we used the SparkFun RedBoard (Arduino Uno equivalent), temperature sensor, photoresistor, piezo speaker and LCD.

The goal of this project is to create a portable sensor unit that can detect useful data for plant growers such as light levels and temperature. The unit, wirelessly connected to the internet, then relays data back to the AT&T M2X servers where it's stored for analysis.

The temperature and light logs are graphed in real time, and this data is viewable immediately. We're leveraging another feature of M2X called 'triggers' that sends alerts based on user defined conditions. For instance, if the temperature gets too hot. We're using a web-service called requestb.in to catch those alerts from M2X for us. When a trigger is caught, we print an alert to the unit's screen, play a sound and send a text message.

Included Files
--------------

- tem.py - this reads the arduino's serial port for sensor updates to push to M2X
- tempy.ino - this code is compiled and run on the arduino
- triggers.py - this code polls requestb.in for updates to our triggers on M2X
- schema.sql - the definition file for the sqlite phone number database
- m2x-screenshot.png - screenshot of our data graphed in the M2X dashboard

About the setup
---------------

The Arduino code gathers the sensor data and waits for user input to trigger the alerts. 

The Raspberry Pi runs two Python scripts, one that pulls data from the Arduino and one that sends a text message and tells the Arduino to alert.

The Arduino is plugged in to and powered over USB by the Raspberry Pi. The Raspberry Pi, with a WiFi dongle in it's second USB slot, is then plugged into the wall. It could just as easily be set up to run off of batteries.

We also setup a local SMTP mail server on the Raspberry Pi to send text messages as emails to AT&T phone numbers at <phonenumber>@txt.att.net.
