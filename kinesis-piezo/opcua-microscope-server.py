import logging
import asyncio
import sys
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
    server.set_endpoint('opc.tcp://localhost:4840/freeopcua/server/')

    # setup our own namespace, not really necessary but should as spec
    uri = 'http://examples.freeopcua.github.io'
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    stepParametersObj = await server.nodes.objects.add_object(idx, 'StepParameters')
    setPositionObj = await server.nodes.objects.add_object(idx, 'SetPosition')

    rateVar = await stepParametersObj.add_variable(idx, 'rate', 100.0)
    accelVar = await stepParametersObj.add_variable(idx, 'accel', 500.0)

    setXVar = await setPositionObj.add_variable(idx, 'SetX', 0.0)
    setYVar = await setPositionObj.add_variable(idx, 'SetY', 0.0)

    vars=[rateVar,accelVar,setXVar,setYVar]
    # Set vars to be writable by clients
    for var in vars:
        await var.set_writable()

    #don't know what this does
    #await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), func, [ua.VariantType.Int64], [ua.VariantType.Int64])
    _logger.info('Starting server!')
    async with server:
        while True:
            await asyncio.sleep(1)
            rate = await rateVar.get_value()
            accel = await accelVar.get_value()
            setX = await setXVar.get_value()
            setY = await setYVar.get_value()
            
            _logger.info('Rate is %.1f', rate)
            _logger.info('Accel is %.1f', accel)
            _logger.info('X is %.1f', setX)
            _logger.info('Y is %.1f', setY)
            #_logger.info('Set value of %s to %.1f', myvar2, new_val_2)
            await setXVar.write_value(setX+0.1)
            await setYVar.write_value(setY+0.2)
            #await myvar.write_value(new_val)
            #await myvar2.write_value(new_val_2)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main(), debug=True)
