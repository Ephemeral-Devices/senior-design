import logging
import asyncio
import sys
from tkinter_camera_live_view import *
sys.path.insert(0, "..")

from asyncua import ua, Server
from asyncua.common.methods import uamethod

@uamethod
def func(parent, value):
    return value * 2


async def main():
    _logger = logging.getLogger('asyncua')
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://169.254.35.94:4840/freeopcua/server/')

    # setup our own namespace, not really necessary but should as spec
    uri = 'http://examples.freeopcua.github.io'
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    stepParametersObj = await server.nodes.objects.add_object(idx, 'StepParameters')
    setPositionObj = await server.nodes.objects.add_object(idx, 'SetPosition')
    
    startCameraObj = await server.nodes.objects.add_object(idx, 'startCamera')
    startCameraVar = await startCameraObj.add_variable(idx, 'startCamera', "start")
    await startCameraVar.set_writable()

    #don't know what this does
    #await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), func, [ua.VariantType.Int64], [ua.VariantType.Int64])
    _logger.info('Starting server!')
    async with server:
        while True:
            await asyncio.sleep(2)
            await startCameraVar.write_value("start")



if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main(), debug=True)
