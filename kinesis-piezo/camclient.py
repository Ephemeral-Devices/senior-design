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
clr.AddReference("System")

from tkinter_camera_live_view import *

def event_notification(self, event):
        print("New event", event)
async def main(): # insert varibale and wait tiime for while loop
    url = "opc.tcp://169.254.35.94:4840/freeopcua/server/"
    async with Client(url=url) as client:
        _logger.info("Root node is: %r", client.nodes.root)
        _logger.info("Objects node is: %r", client.nodes.objects)
        _logger.info("Children of root are: %r", await client.nodes.root.get_children())
        uri = "http://examples.freeopcua.github.io"
        idx = await client.get_namespace_index(uri)
        _logger.info("index of our namespace is %s", idx)
        startCameraVar = await client.nodes.root.get_child(["0:Objects","2:startCamera"])        
        with TLCameraSDK() as sdk:
            camera_list = sdk.discover_available_cameras()
            with sdk.open_camera(camera_list[0]) as camera:
                # create generic Tk App with just a LiveViewCanvas widget
                print("Generating app...")
                root = tk.Tk()
                root.title(camera.name)
                image_acquisition_thread = ImageAcquisitionThread(camera)
                camera_widget = LiveViewCanvas(parent=root, image_queue=image_acquisition_thread.get_output_queue())

                print("Setting camera parameters...")
                camera.frames_per_trigger_zero_for_unlimited = 0
                camera.arm(2)
                camera.issue_software_trigger()

                print("Starting image acquisition thread...")
                image_acquisition_thread.start()

                print("App starting")
                root.mainloop()

                print("Waiting for image acquisition thread to finish...")
                image_acquisition_thread.stop()
                image_acquisition_thread.join()

                print("Closing resources...")
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
