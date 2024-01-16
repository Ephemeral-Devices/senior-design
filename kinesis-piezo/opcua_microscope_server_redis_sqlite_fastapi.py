import logging
import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from asyncua import ua, Server
from asyncua.common.methods import uamethod
from asyncua.server.history_sql import HistorySQLite
import aioredis

app = FastAPI()

@uamethod
def func(parent, value):
    return value * 2

async def init_server():
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
    step_parameters_obj = await server.nodes.objects.add_object(idx, 'StepParameters')
    set_position_obj = await server.nodes.objects.add_object(idx, 'SetPosition')

    rate_var = await step_parameters_obj.add_variable(idx, 'rate', 100.0)
    accel_var = await step_parameters_obj.add_variable(idx, 'accel', 500.0)
    set_x_var = await set_position_obj.add_variable(idx, 'SetX', 10.0)
    set_y_var = await set_position_obj.add_variable(idx, 'SetY', 10.0)

    vars = [rate_var, accel_var, set_x_var, set_y_var]

    # Set vars to be writable by clients
    for var in vars:
        await var.set_writable()

    # Initialize historized nodes in SQLite database
    await sqlite_history.new_historized_node(node_id=rate_var.nodeid, period=None, count=None)
    await sqlite_history.new_historized_node(node_id=accel_var.nodeid, period=None, count=None)
    await sqlite_history.new_historized_node(node_id=set_x_var.nodeid, period=None, count=None)
    await sqlite_history.new_historized_node(node_id=set_y_var.nodeid, period=None, count=None)

    _logger.info('Starting server!')

    return server, redis, sqlite_history

async def save_values(redis, var_name, value):
    await redis.hmset_dict(var_name, {"value": value})

@app.on_event("startup")
async def startup_event():
    global server, redis, sqlite_history
    server, redis, sqlite_history = await init_server()

@app.get("/")
async def read_root():
    rate = await server.nodes.objects.StepParameters.rate.read_value()
    accel = await server.nodes.objects.StepParameters.accel.read_value()
    set_x = await server.nodes.objects.SetPosition.SetX.read_value()
    set_y = await server.nodes.objects.SetPosition.SetY.read_value()

    # Additional logic as needed
    await server.nodes.objects.SetPosition.SetX.write_value(set_x * -1)
    await server.nodes.objects.SetPosition.SetY.write_value(set_y * -1)

    # Save historized values in the SQLite database
    datavalue_rate = ua.DataValue(ua.Variant(rate))
    datavalue_accel = ua.DataValue(ua.Variant(accel))
    datavalue_set_x = ua.DataValue(ua.Variant(set_x))
    datavalue_set_y = ua.DataValue(ua.Variant(set_y))

    await sqlite_history.save_node_value(node_id=server.nodes.objects.StepParameters.rate.nodeid, datavalue=datavalue_rate)
    await sqlite_history.save_node_value(node_id=server.nodes.objects.StepParameters.accel.nodeid, datavalue=datavalue_accel)
    await sqlite_history.save_node_value(node_id=server.nodes.objects.SetPosition.SetX.nodeid, datavalue=datavalue_set_x)
    await sqlite_history.save_node_value(node_id=server.nodes.objects.SetPosition.SetY.nodeid, datavalue=datavalue_set_y)

    # Save values in Redis
    await save_values(redis, "rateVar", rate)
    await save_values(redis, "accelVar", accel)
    await save_values(redis, "setXVar", set_x)
    await save_values(redis, "setYVar", set_y)

    return JSONResponse(content={"message": "Values updated successfully"})

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
