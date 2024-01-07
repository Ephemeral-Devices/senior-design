import asyncio
from asyncua import Client

from .config import ENDPOINT
from .log import get_log


log = get_log(__name__)

RECEIVED_COMMAND = """Received command:
Rate is {rate:.1f}
Accel is {accel:.1f}
X is {set_x:.1f}
Y is {set_y:.1f}"""



async def read_and_execute_commands(client):
    while True:
        # Get the root node
        root = client.get_root_node()

        # Browse for the StepParameters object
        step_parameters_obj = await root.get_child(['0:Objects', '2:StepParameters'])

        # Get the rate variable
        rate_var = await step_parameters_obj.get_child(['2:rate'])

        # Get the accel variable
        accel_var = await step_parameters_obj.get_child(['2:accel'])

        # Browse for the SetPosition object
        set_position_obj = await root.get_child(['0:Objects', '2:SetPosition'])

        # Get the SetX variable
        set_x_var = await set_position_obj.get_child(['2:SetX'])

        # Get the SetY variable
        set_y_var = await set_position_obj.get_child(['2:SetY'])

        # Read values
        rate = await rate_var.read_value()
        accel = await accel_var.read_value()
        set_x = await set_x_var.read_value()
        set_y = await set_y_var.read_value()

        log.info(
            RECEIVED_COMMAND.format(rate=rate, accel=accel, set_x=set_x, set_y=set_y)
        )

        # print(f'Received command:')
        # print(f'Rate is {rate:.1f}')
        # print(f'Accel is {accel:.1f}')
        # print(f'X is {set_x:.1f}')
        # print(f'Y is {set_y:.1f}')

        # Perform actions based on the received values
        # Add your logic here to execute commands based on the values

        # Sleep for a short duration before reading again
        await asyncio.sleep(2)


async def run_client():
    async with Client(url=ENDPOINT) as client:
        # Connect to the server
        log.info(
            "run_client with hostname %s port %s" %
            (client.server_url.hostname, client.server_url.port)
        )

        # await client.connect()

        # Start the continuous reading and execution loop
        # await read_and_execute_commands(client)
        assert False, 'resume work - it is able to connect to server'

# if __name__ == '__main__':
#     asyncio.run(run_client())


# import asyncio
# import logging
# from asyncua import Client
# from piezo import InertialController, InertialMotorStatus
# _logger = logging.getLogger('asyncua')
# class NodeHandler:
#     def __init__(self, piezo, channel, initial_position=0):
#         self.piezo = piezo
#         self.channel = channel
#         self.current_position = initial_position
#     def datachange_notification(self, node, val, data):
#         print(f"Moving {self.channel.name} to {val}")
#         self.piezo.move(self.channel, position=int(val - self.current_position))
#         self.current_position = val
#     def event_notification(self, event):
#         print("New event", event)
# class OpcuaClient:
#     def __init__(self, url):
#         self.url = url
#         self.client = None
#     async def connect(self):
#         self.client = await Client(url=self.url)
#         await self.client.connect()
#         _logger.info("Connected to OPC UA server")
#     async def disconnect(self):
#         await self.client.disconnect()
#         _logger.info("Disconnected from OPC UA server")
#     async def subscribe_to_variable(self, node_path, handler):
#         variable_node = await self.client.nodes.root.get_child(node_path)
#         subscription = await self.client.create_subscription(500, handler)
#         handle = await subscription.subscribe_data_change(variable_node)
#         return handle
# async def main():
#     opcua_url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
#     opcua_client = OpcuaClient(opcua_url)
#     await opcua_client.connect()
#     mypiezo = InertialController(97101189)
#     xchannel = InertialMotorStatus.MotorChannels.Channel1
#     ychannel = InertialMotorStatus.MotorChannels.Channel2
#     x_handler = NodeHandler(mypiezo, xchannel)
#     y_handler = NodeHandler(mypiezo, ychannel)
#     x_handle = await opcua_client.subscribe_to_variable(["0:Objects", "2:SetPosition", "2:SetX"], x_handler)
#     y_handle = await opcua_client.subscribe_to_variable(["0:Objects", "2:SetPosition", "2:SetY"], y_handler)
#     try:
#         while True:
#             await asyncio.sleep(0.1)
#     except KeyboardInterrupt:
#         await opcua_client.disconnect()
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(main())