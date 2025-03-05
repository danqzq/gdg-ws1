import asyncio
import json
import random
import websockets

# Constants
WIDTH, HEIGHT = 800, 600
RESOURCE_SPAWN_TIME = 5
PLAYER_SIZE = 64
RESOURCE_SIZE = 32

# Player and Resource data
players = {}
resources = []
next_player_id = 1
next_resource_id = 1
clients = set()


async def handle_client(websocket):
    global next_player_id
    player_id = next_player_id
    next_player_id += 1
    players[player_id] = {"x": random.randint(PLAYER_SIZE, WIDTH - PLAYER_SIZE),
                          "y": random.randint(PLAYER_SIZE, HEIGHT - PLAYER_SIZE),
                          "score": 0}
    clients.add(websocket)

    try:
        async for message in websocket:
            data = json.loads(message)
            if data["type"] == "move":
                players[player_id]["x"] += data["dx"]
                players[player_id]["y"] += data["dy"]

                # Check for resource collection
                for resource in resources[:]:
                    if abs(players[player_id]["x"] - resource["x"]) < PLAYER_SIZE / 2 and abs(
                            players[player_id]["y"] - resource["y"]) < PLAYER_SIZE / 2:
                        resources.remove(resource)
                        players[player_id]["score"] += 1

            # Broadcast updates to all clients
            update = json.dumps({"type": "update", "players": players, "resources": resources})
            await asyncio.gather(*(client.send(update) for client in clients))
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        del players[player_id]
        clients.remove(websocket)


async def spawn_resources():
    global next_resource_id
    while True:
        await asyncio.sleep(RESOURCE_SPAWN_TIME)
        resources.append(
            {"id": next_resource_id,
             "x": random.randint(RESOURCE_SIZE, WIDTH - RESOURCE_SIZE),
             "y": random.randint(RESOURCE_SIZE, HEIGHT - RESOURCE_SIZE)})
        next_resource_id += 1

        update = json.dumps({"type": "update", "players": players, "resources": resources})
        await asyncio.gather(*(client.send(update) for client in clients))


async def server():
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # Keep server running


async def main():
    asyncio.create_task(spawn_resources())
    await server()


asyncio.run(main())