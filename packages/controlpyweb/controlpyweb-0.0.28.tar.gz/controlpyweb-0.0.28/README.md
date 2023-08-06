# ControlPyWeb
A project to facilitate easy read/write to the ControlByWeb line of Automation/SCADA IO products. 


## Description
Xytronic Research makes a handy line of remote IO products useful for home and industrial 
automation. Interacting with these modules generally requires the use 
of a url library such as requests, and then requires dissecting the response to be dissected
and processed. While not terribly difficult to do, it is repetitive. 

This module seeks to abstract out some of that effort in a thought out and tested way. 

## Installation
pip install controlpyweb


## Usage
The basis of functionality is the WebIOModule class. It both acts as a container for individual
IO and handles interaction with the hardware. 

~~~~
from controlpyweb.webio_module import WebIOModule
from controlpyweb.single_io import DiscreteIn, DiscreteOut, AnalogIn, AnalogOut


class X404DigitalIn(WebIOModule):   # Name the class whatever you like
    StartButton = DiscreteIn("Start Button", "startButton")
    StopButton = DiscreteIn("Stop Button", "stopButton")
    DoorClosed = DiscreteIn("Door Closed", "doorClosed")


class X410DigitalOut(WebIOModule):
    StartLamp = DiscreteOut("Start Lapm", "redLamp")
    MaintLight = DiscreteOut("Maintenance Lamp", "lamp1")


digital_in = X404DigitalIn("192.168.1.1")
relay_out = X410DigitalOut("192.168.1.2")


digital_in.update_from_module()

relay_out.StartLamp = digital_in.StartButton
relay_out.MaintLight = not digital_in.DoorClosed

relay_out.send_changes_to_module()
~~~~

Though it is possible to do immediate reads/writes, the most efficient pattern is to first to 
do an update from the module, make all changes, then send the results.