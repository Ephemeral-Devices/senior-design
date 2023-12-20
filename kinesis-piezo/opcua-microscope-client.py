import asyncio
import logging
from asyncua import Client
_logger = logging.getLogger('asyncua')

# -*- coding: utf-8 -*-
#from __future__ import print_function
#from __future__ import division

import clr
import time
# Needed for the use of Decimal class of c#. Requires clr to import System in
# this way.
from System import Decimal
from os import getenv

main_dll_dir = rf"{getenv('USERPROFILE')}\Documents\senior-design-main\kinesis-piezo\libs\kinesis"
dll_names = [
    "Thorlabs.MotionControl.DeviceManagerCLI.dll",
    "Thorlabs.MotionControl.GenericPiezoCLI.dll",
    "Thorlabs.MotionControl.TCube.PiezoCLI.dll",
    "Thorlabs.MotionControl.TCube.StrainGaugeCLI.dll",
    "Thorlabs.MotionControl.KCube.Piezo.dll",
    "Thorlabs.MotionControl.KCube.PiezoCLI.dll",
    # "Thorlabs.MotionControl.KCube.InertialMotor.dll",
    "Thorlabs.MotionControl.KCube.InertialMotorCLI.dll",
]

clr.AddReference("System")
for dll_name in dll_names:
    clr.AddReference(main_dll_dir + dll_name)
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.GenericPiezoCLI import Piezo
#from Thorlabs.MotionControl.TCube.PiezoCLI import *
#from Thorlabs.MotionControl.TCube.StrainGaugeCLI import *
#from Thorlabs.MotionControl.KCube.Piezo import *
#from Thorlabs.MotionControl.KCube.PiezoCLI import *
#from Thorlabs.MotionControl.KCube.InertialMotor import *
from Thorlabs.MotionControl.KCube.InertialMotorCLI import *


from piezo import *

class XHandler(object):
    xPos = 0
    def datachange_notification(self, node, val, data):
        print("Moving X ",val)
        mypiezo.move(xchannel, position=int(val-self.xPos))
        self.xPos=val
    def event_notification(self, event):
        print("New event", event)
class YHandler(object):
    yPos = 0
    def datachange_notification(self, node, val, data):
        print("Moving Y ", val)
        mypiezo.move(ychannel, position=int(val-self.yPos))
        self.yPos=val
    def event_notification(self, event):
        print("New event", event)
async def main(): # insert varibale and wait tiime for while loop
    url = "opc.tcp://192.168.1.232:4840/freeopcua/server/"
    async with Client(url=url) as client:
        _logger.info("Root node is: %r", client.nodes.root)
        _logger.info("Objects node is: %r", client.nodes.objects)
        _logger.info("Children of root are: %r", await client.nodes.root.get_children())
        uri = "http://examples.freeopcua.github.io"
        idx = await client.get_namespace_index(uri)
        _logger.info("index of our namespace is %s", idx)
        SetRate = await client.nodes.root.get_child(["0:Objects","2:StepParameters","2:rate"])
        SetAccel = await client.nodes.root.get_child(["0:Objects","2:StepParameters","2:accel"])
        SetX = await client.nodes.root.get_child(["0:Objects","2:SetPosition","2:SetX"])
        SetY = await client.nodes.root.get_child(["0:Objects","2:SetPosition","2:SetY"])
        _logger.info("Vars is: %s",vars)
        #obj = await client.nodes.root.get_child(["0:Objects", "2:MyObject"])
        #_logger.info("vars is: %r", vars)
        # subscribing to a variable node
        x_handler = XHandler()
        x_sub = await client.create_subscription(500, x_handler)
        x_handle = await x_sub.subscribe_data_change(SetX)
        y_handler = YHandler()
        y_sub = await client.create_subscription(500, y_handler)
        y_handle = await y_sub.subscribe_data_change(SetY)
        #await asyncio.sleep(10)
        while(True):
            await asyncio.sleep(.1)
        #await sub.subscribe_events()
        #res = await obj.call_method("2:multiply", 3, "klk")
        #_logger.info("method result is: %r", res)
if __name__ == "__main__":

    
    #mypiezo = InertialController(97101189)#REAL ONE

    mypiezo = InertialController(97101189)
    xchannel = InertialMotorStatus.MotorChannels.Channel1
    ychannel = InertialMotorStatus.MotorChannels.Channel2
    mypiezo.setStepParameters(xchannel,rate=100,accel=500)
    mypiezo.setStepParameters(ychannel,rate=100,accel=500)
    mypiezo.zeroDevice(xchannel)
    mypiezo.zeroDevice(ychannel)
    xPos=0
    yPos=0
    #mypiezo.move(mychannel, position=100)
    #mypiezo.getPosition()


    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

