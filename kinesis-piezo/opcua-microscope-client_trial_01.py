import asyncio
import logging
from asyncua import Client

class NodeHandler:
    def __init__(self, piezo, channel, initial_position=0):
        self.piezo = piezo
        self.channel = channel
        self.current_position = initial_position
        self.logger = logging.getLogger(f'{self.__class__.__name__}_{self.channel.name}')

    def datachange_notification(self, node, val, data):
        self.logger.info(f"Moving {self.channel.name} to {val}")
        self.piezo.move(self.channel, position=int(val - self.current_position))
        self.current_position = val

    def event_notification(self, event):
        self.logger.info("New event: %s", event)

class MockInertialController:
    def move(self, channel, position):
        print(f"Mock Move: Channel {channel.name}, Position {position}")

    def zeroDevice(self, channel):
        print(f"Mock Zero Device: Channel {channel.name}")

class OpcuaClient:
    def __init__(self, url):
        self.url = url
        self.client = None
        self.logger = logging.getLogger(f'{self.__class__.__name__}')

    async def connect(self):
        async with Client(url=self.url) as client:
            self.client = client
            await self.client.connect()
            self.logger.info("Connected to OPC UA server")

    async def disconnect(self):
        await self.client.disconnect()
        self.logger.info("Disconnected from OPC UA server")

    async def subscribe_to_variable(self, node_path, handler):
        variable_node = await self.client.nodes.root.get_child(node_path)
        subscription = await self.client.create_subscription(500, handler)
        handle = await subscription.subscribe_data_change(variable_node)
        return handle

async def main():
    opcua_url = "opc.tcp://127.0.0.1:4840/freeopcua/server/"
    opcua_client = OpcuaClient(opcua_url)
    await opcua_client.connect()

    mypiezo = MockInertialController()

    xchannel = MockInertialController()
    ychannel = MockInertialController()

    x_handler = NodeHandler(mypiezo, xchannel)
    y_handler = NodeHandler(mypiezo, ychannel)

    x_handle = await opcua_client.subscribe_to_variable(["0:Objects", "2:SetPosition", "2:SetX"], x_handler)
    y_handle = await opcua_client.subscribe_to_variable(["0:Objects", "2:SetPosition", "2:SetY"], y_handler)

    try:
        while True:
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        await opcua_client.disconnect()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
