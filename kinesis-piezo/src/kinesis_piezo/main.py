import sys
import argparse
import enum
import asyncio


class RunArg(enum.Enum):
    SERVER = 'server'
    CLIENT = 'client'


def parse_args():
        
    parser = argparse.ArgumentParser()
    parser.add_argument('run', type=RunArg, help=', '.join([ra.value for ra in RunArg]))
    return parser.parse_args()


def client():
    from kinesis_piezo.client import run_client
    return asyncio.run(run_client())


def server():
    from kinesis_piezo.server import run_server
    return asyncio.run(run_server())


def main():
    args = parse_args()
    run = {
        fn.__name__: fn
        for fn in (client, server)
    }[args.run.value]
    run()


if __name__ == "__main__":
    sys.exit(main())