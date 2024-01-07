import logging
import asyncio
from asyncua import ua, Server
from asyncua.common.methods import uamethod

<<<<<<< HEAD
class OpcuaServer:
    def __init__(self):
        self._logger = logging.getLogger('asyncua')
        self.server = None

    @staticmethod
    async def add_variable(server, parent_obj, namespace_idx, variable_name, initial_value):
        return await parent_obj.add_variable(namespace_idx, variable_name, initial_value)

    @staticmethod
    async def add_object(server, parent_obj, namespace_idx, object_name):
        return await parent_obj.add_object(namespace_idx, object_name)

    async def setup_server(self):
        self.server = Server()
        await self.server.init()
        self.server.set_endpoint('opc.tcp://127.0.0.1:4840/freeopcua/server/')
        uri = 'http://examples.freeopcua.github.io'
        idx = await self.server.register_namespace(uri)

        # Add print statements for step_parameters_obj and idx
        step_parameters_obj = await OpcuaServer.add_object(self.server, self.server.nodes.objects, idx, 'StepParameters')
        set_position_obj = await OpcuaServer.add_object(self.server, self.server.nodes.objects, idx, 'SetPosition')


        rate_var = await OpcuaServer.add_variable(self.server, step_parameters_obj, idx, 'rate', 100.0)
        accel_var = await OpcuaServer.add_variable(self.server, step_parameters_obj, idx, 'accel', 500.0)
        set_x_var = await OpcuaServer.add_variable(self.server, set_position_obj, idx, 'SetX', 10.0)
        set_y_var = await OpcuaServer.add_variable(self.server, set_position_obj, idx, 'SetY', 10.0)
=======
class MyServer:
    def __init__(self, set_x=10.0, set_y=10.0, endpoint='opc.tcp://127.0.0.1:4840/freeopcua/server/'):
        self.endpoint = endpoint
        self.set_x_value = set_x
        self.set_y_value = set_y
        self.server = Server()
        self._logger = logging.getLogger('asyncua')  # Define _logger here


    async def initialize(self):
        await self.server.init()
        self.server.set_endpoint(self.endpoint)
        uri = 'http://examples.freeopcua.github.io'
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
>>>>>>> 4f41d8e (Add new feature)

        self.vars = [rate_var, accel_var, set_x_var, set_y_var]

<<<<<<< HEAD
        for var in self.vars:
            await var.set_writable()

    async def run_server(self):
        self._logger.info('Starting server!')
        async with self.server:
            while True:
                await asyncio.sleep(2)
                rate = await self.vars[0].get_value()
                accel = await self.vars[1].get_value()
                set_x = await self.vars[2].get_value()
                set_y = await self.vars[3].get_value()

                self._logger.info('Rate is %.1f', rate)
                self._logger.info('Accel is %.1f', accel)
                self._logger.info('X is %.1f', set_x)
                self._logger.info('Y is %.1f', set_y)
=======
    
    
    async def start(self):
        while True:
            await asyncio.sleep(2)
            rate = await self.rate_var.get_value()
            accel = await self.accel_var.get_value()
            set_x = await self.set_x_var.get_value()
            set_y = await self.set_y_var.get_value()

            self._logger.info('Rate is %.1f', rate)
            self._logger.info('Accel is %.1f', accel)
            self._logger.info('X is %.1f', set_x)
            self._logger.info('Y is %.1f', set_y)

            await self.set_X(set_x * -1)
            await self.set_Y(set_y * -1)

# if __name__ == '__main__':
#     _logger = logging.getLogger('asyncua')
#     logging.basicConfig(level=logging.DEBUG)

#     my_server = MyServer(set_x=5.0, set_y=7.0)
#     asyncio.run(my_server.initialize(), debug=True)
#     asyncio.run(my_server.start(), debug=True)

>>>>>>> 4f41d8e (Add new feature)

                await self.vars[2].write_value(set_x * -1)
                await self.vars[3].write_value(set_y * -1)

if __name__ == '__main__':
<<<<<<< HEAD
    logging.basicConfig(level=logging.DEBUG)

    opcua_server = OpcuaServer()
    asyncio.run(opcua_server.setup_server())
    asyncio.run(opcua_server.run_server(), debug=True)
=======
    async def run_server():
        _logger = logging.getLogger('asyncua')
        logging.basicConfig(level=logging.DEBUG)

        my_server = MyServer(set_x=5.0, set_y=7.0)
        loop = asyncio.get_event_loop()

        # Initialize the server
        await my_server.initialize()

        # Call set_X with a specific value (e.g., 42.0)
        await my_server.set_X(42.0)

        # Get the current value of set_X
        current_set_x_value = await my_server.set_x_var.get_value()
        _logger.info('Current value of set_X is %.1f', current_set_x_value)

        # Run the server start method
        await my_server.start()

    asyncio.run(run_server())
>>>>>>> 4f41d8e (Add new feature)
