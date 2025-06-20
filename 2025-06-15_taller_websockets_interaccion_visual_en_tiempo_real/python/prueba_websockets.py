import asyncio
import websockets
import json
import random
async def handler(websocket):
    while True:
        data = {
            "x": random.uniform(-5, 5),
            "y": random.uniform(-5, 5),
            "color": random.choice(["red", "green", "blue"])
        }
        await websocket.send(json.dumps(data))
        await asyncio.sleep(0.5)
async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()
asyncio.run(main())