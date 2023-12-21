import logging
import asyncio
from asyncua import ua, Server
from asyncua.common.methods import uamethod

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

        self.vars = [rate_var, accel_var, set_x_var, set_y_var]

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

                await self.vars[2].write_value(set_x * -1)
                await self.vars[3].write_value(set_y * -1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    opcua_server = OpcuaServer()
    asyncio.run(opcua_server.setup_server())
    asyncio.run(opcua_server.run_server(), debug=True)
