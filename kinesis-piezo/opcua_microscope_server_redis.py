import logging
import asyncio
from asyncua import ua, Server
from asyncua.common.methods import uamethod
from asyncua.server.history_sql import HistorySQLite
import aioredis

@uamethod
def func(parent, value):
    return value * 2

async def main():
    _logger = logging.getLogger('asyncua')
    
    # Connect to Redis
    redis = await aioredis.create_redis('redis://127.0.0.1:6379', encoding='utf-8')

    # Initialize and configure the SQLite database
    sqlite_history = HistorySQLite("test.db")
    await sqlite_history.init()

    # Setup our server
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://127.0.0.1:4840/freeopcua/server/')

    # Setup our own namespace
    uri = 'http://examples.freeopcua.github.io'
    idx = await server.register_namespace(uri)

    # Populating our address space
    stepParametersObj = await server.nodes.objects.add_object(idx, 'StepParameters')
    setPositionObj = await server.nodes.objects.add_object(idx, 'SetPosition')

    rateVar = await stepParametersObj.add_variable(idx, 'rate', 100.0)
    accelVar = await stepParametersObj.add_variable(idx, 'accel', 500.0)
    setXVar = await setPositionObj.add_variable(idx, 'SetX', 10.0)
    setYVar = await setPositionObj.add_variable(idx, 'SetY', 10.0)

    vars = [rateVar, accelVar, setXVar, setYVar]

    # Set vars to be writable by clients
    for var in vars:
        await var.set_writable()

    # Initialize historized nodes in SQLite database
    await sqlite_history.new_historized_node(node_id=rateVar.nodeid, period=None, count=None)
    await sqlite_history.new_historized_node(node_id=accelVar.nodeid, period=None, count=None)
    await sqlite_history.new_historized_node(node_id=setXVar.nodeid, period=None, count=None)
    await sqlite_history.new_historized_node(node_id=setYVar.nodeid, period=None, count=None)

    _logger.info('Starting server!')

    async with server:
        while True:
            await asyncio.sleep(2)
            rate = await rateVar.get_value()
            accel = await accelVar.get_value()
            setX = await setXVar.get_value()
            setY = await setYVar.get_value()

            _logger.info('Rate is %.1f', rate)
            _logger.info('Accel is %.1f', accel)
            _logger.info('X is %.1f', setX)
            _logger.info('Y is %.1f', setY)

            # Save historized values in the SQLite database
            datavalue_rate = ua.DataValue(ua.Variant(rate))
            datavalue_accel = ua.DataValue(ua.Variant(accel))
            datavalue_setX = ua.DataValue(ua.Variant(setX))
            datavalue_setY = ua.DataValue(ua.Variant(setY))

            await sqlite_history.save_node_value(node_id=rateVar.nodeid, datavalue=datavalue_rate)
            await sqlite_history.save_node_value(node_id=accelVar.nodeid, datavalue=datavalue_accel)
            await sqlite_history.save_node_value(node_id=setXVar.nodeid, datavalue=datavalue_setX)
            await sqlite_history.save_node_value(node_id=setYVar.nodeid, datavalue=datavalue_setY)

            # Save values in Redis
            await redis.hmset_dict("rateVar", {"value": rate})
            await redis.hmset_dict("accelVar", {"value": accel})
            await redis.hmset_dict("setXVar", {"value": setX})
            await redis.hmset_dict("setYVar", {"value": setY})

            # Additional logic as needed
            await setXVar.write_value(setX * -1)
            await setYVar.write_value(setY * -1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)



