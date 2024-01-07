import logging
import asyncio
from asyncua import ua, Server
from asyncua.common.methods import uamethod


from .log import get_log
from .config import HOST, PORT, ENDPOINT


log = get_log(__name__)


class MyServer:
    def __init__(self, set_x=10.0, set_y=10.0, endpoint=ENDPOINT):
        self.endpoint = endpoint
        self.set_x_value = set_x
        self.set_y_value = set_y
        self.server = Server()


    async def initialize(self):
        await self.server.init()
        self.server.set_endpoint(self.endpoint)

        # uri = 'http://examples.freeopcua.github.io'
        uri = f"http://{HOST}"
        self.idx = await self.server.register_namespace(uri)

        # Populating address space
        self.step_parameters_obj = await self.server.nodes.objects.add_object(self.idx, 'StepParameters')
        self.set_position_obj = await self.server.nodes.objects.add_object(self.idx, 'SetPosition')

        self.rate_var = await self.step_parameters_obj.add_variable(self.idx, 'rate', 100.0)
        self.accel_var = await self.step_parameters_obj.add_variable(self.idx, 'accel', 500.0)

        self.set_x_var = await self.set_position_obj.add_variable(self.idx, 'SetX', self.set_x_value)
        self.set_y_var = await self.set_position_obj.add_variable(self.idx, 'SetY', self.set_y_value)

        # Set variables to be writable by clients
        vars = [self.rate_var, self.accel_var, self.set_x_var, self.set_y_var]
        for var in vars:
            await var.set_writable()
        
        return self.server

    async def set_X(self, x_value):
        self.set_x_value = x_value
        await self.set_x_var.write_value(x_value)

    async def set_Y(self, y_value):
        self.set_y_value = y_value
        await self.set_y_var.write_value(y_value)
    
    
    async def start(self):
        while True:
            await asyncio.sleep(2)
            rate = await self.rate_var.get_value()
            accel = await self.accel_var.get_value()
            set_x = await self.set_x_var.get_value()
            set_y = await self.set_y_var.get_value()

            log.info('Rate is %.1f', rate)
            log.info('Accel is %.1f', accel)
            log.info('X is %.1f', set_x)
            log.info('Y is %.1f', set_y)

            await self.set_X(set_x * -1)
            await self.set_Y(set_y * -1)

# if __nxame__ == '__main__':
#     _logger = logging.getLogger('asyncua')
#     logging.basicConfig(level=logging.DEBUG)

#     my_server = MyServer(set_x=5.0, set_y=7.0)
#     asyncio.run(my_server.initialize(), debug=True)
#     asyncio.run(my_server.start(), debug=True)

async def run_server():
    my_server = MyServer(set_x=5.0, set_y=7.0)
    # loop = asyncio.get_event_loop()

    # Initialize the server
    await my_server.initialize()

    # Call set_X with a specific value (e.g., 42.0)
    await my_server.set_X(42.0)

    # Get the current value of set_X
    current_set_x_value = await my_server.set_x_var.get_value()
    log.info('Current value of set_X is %.1f', current_set_x_value)

    # Run the server start method
    await my_server.start()


# if __name__ == '__main__':
#     asyncio.run(run_server())