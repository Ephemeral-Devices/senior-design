import os


PROJECT_NAME = "KINESIS_PIEZO"


HOST = os.environ.get(f"{PROJECT_NAME}__HOST", '127.0.0.1')
PORT = int(os.environ.get(f"{PROJECT_NAME}__PORT", '4840'))
SERVER_ROOT = os.environ.get(f"{PROJECT_NAME}__SERVER_ROOT", 'freeopcua/server').rstrip('/')

ENDPOINT = f"opc.tcp://{HOST}:{PORT}/{SERVER_ROOT}/"


LOG_LEVEL = os.environ.get(
    f"{PROJECT_NAME}__LOG_LEVEL", "debug"
).upper()
