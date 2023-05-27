import asyncio
import datetime
import json

import websockets


class CoPaintingServer:
    def __init__(self):
        self._clients = []

    async def run(self):
        async def handler(websocket, path):
            self._clients.append(websocket)

            try:
                while True:
                    input_data = await websocket.recv()
                    # TO DO: validate the data
                    current_time = datetime.datetime.now()
                    data = json.loads(input_data)
                    data['timestamp'] = current_time.isoformat()
                    output_data = json.dumps(data)
                    for other_websocket in self._clients:
                        asyncio.create_task(other_websocket.send(output_data))
            except websockets.ConnectionClosed:
                pass
            finally: self._clients.remove(websocket)

        async with websockets.serve(handler, 'localhost', 8765):
            await asyncio.Future()  # run forever


def main():
    server = CoPaintingServer()
    print('Starting server')
    asyncio.run(server.run())


if __name__ == '__main__':
    main()
