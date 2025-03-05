# Online Multiplayer Game Tutorial: Pygame, WebSockets, and Python

## Overview
This tutorial will guide you through the creation of a simple online multiplayer game using **Python**, **Pygame**, and **WebSockets**. The game allows multiple players to connect to a server, move around the screen, and collect resources in real-time.

By the end of this tutorial, you will have:
- A functional multiplayer game with player movement.
- A simple server-client communication system using WebSockets.
- A basic resource collection mechanic.
- A live leaderboard and a scoring system.

## Prerequisites
Before starting, ensure you have the following installed:

1. **Python 3.6+**: If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).
2. **Required Libraries**: You need to install **Pygame** for graphics, **WebSockets** for communication, and **Asyncio** for handling concurrency.

Run the following command to install the required libraries:

```sh
pip install pygame websockets
```

### Base Terminologies & Concepts

**Libraries:**

- **Internal**
    - **`asyncio`**: A library to write concurrent code using the async/await syntax.
    - **`json`**: A built-in Python library for encoding and decoding JSON data.
    - **`random`**: A built-in Python library for generating random numbers.
- **External**
    - **`pygame`**: A set of Python modules designed for writing video games.
    - **`websockets`**: A communication protocol that provides full-duplex communication channels over a single TCP connection.

**Game Concepts:**

- **Window**: Not your typical window, but the area where the game is displayed.
- **Game Loop**: A continuous cycle that processes user input, updates game objects, and renders the scene.
- **Rendering**: The process of drawing graphics on the screen.
- **RGB**: A color model using the three primary colors (Red, Green, Blue) to create a broad array of colors.
- **Frame rate**: The number of frames displayed per second (FPS). The `Clock` object in Pygame helps control the frame rate of our game.
Managing the frame rate of a game is important for ensuring consistent gameplay across different devices.

**Networking Concepts:**

- **Thread**: A separate flow of execution within a program. Think of a thread as a sub-process that runs concurrently with other sub-processes.
- **Multithreading**: A programming technique that allows multiple threads to execute concurrently within a single process.
We will achieve multithreading with the help of the built-in `asyncio` library.
- **Asynchronous Programming**: A programming paradigm that allows multiple tasks to run concurrently without blocking the main execution.
- **`await`**: A keyword used to pause the execution of an asynchronous function until a coroutine is completed.
- **`async`**: A keyword used to define an asynchronous function that can pause and resume
---
- **Server**: A computer or program that provides services to other computers or programs (clients).
- **Client**: A computer or program that requests services from a server.
- **Sending**: The process of transmitting data from one device to another.
- **Receiving**: The process of accepting data from another device.
---
- **JSON (JavaScript Object Notation)**: A lightweight data interchange format that is easy for humans to read and write and easy for machines to parse and generate.
We will be using this format of data to allow communication between the server and clients using WebSockets.
- **JSON Dumping/Encoding**: The process of converting a Python object into a JSON string.
- **JSON Loading/Decoding**: The process of converting a JSON string into a Python object.

**Mathematical Concepts & Functions:**

- **Position**: The location of an object in a 2D space, usually represented by $(x, y)$ coordinates.
    - **x**: The horizontal position from left to right.
    - **y**: The vertical position from top to bottom.
- **Scale**: The size of an object relative to its original size.
   - **x-scale**: The horizontal size.
   - **y-scale**: The vertical size.
- **Distance**: The measure of space between two points in a 2D space. The formula to calculate the distance between two points $(x_1, y_1)$ and $(x_2, y_2)$ is derived from the Pythagorean theorem and is given by:

$$
{Distance} = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}
$$

- **`abs()`**: A function that returns the absolute value of a number. If the number is negative, it returns the positive value.
- **`enumerate()`**: A function that returns an iterator of tuples containing the index and value of each element in a list.
    - **Syntax**: `enumerate(iterable, start=0)`
    - **`iterable`**: The list, tuple, or string to iterate over.
    - **`start`**: The starting index value (default is 0).

**Other Concepts:**

- **`global` keyword**: A keyword used to declare that a variable inside a function is referring to a global variable.
- **`del` keyword**: A keyword used to delete a variable or an element from a list or dictionary.
- **`try`/`except`/`finally`**: A block of code that allows you to handle exceptions (errors) that occur during execution.

---
- **`lambda` function**: A small anonymous function defined using the `lambda` keyword.
    - **Syntax**: `lambda arguments: expression`
    - **`arguments`**: The input parameters.
    - **`expression`**: The output value.

We will use this only once in `main.py` to sort the player scores for the leaderboard:

```python
sorted_players = sorted(players.items(), key=lambda p: p[1]["score"], reverse=True)
```

---
- **List Expansion**: A technique to unpack a list into individual elements. It is done by adding a `*` before the list.

We only use this once in `server.py` to send updates to all clients simultaneously using
```python
await asyncio.gather(*(client.send(update) for client in clients))
```

---

## File Structure

You will work with two main scripts and you will also be given two sprite images to use in the game.
The file structure will look like this:

```plaintext
project_folder/
│-- main.py  # Client-side game logic
│-- server.py  # Server-side WebSocket logic
│-- player.png  # Player sprite
│-- diamond.png  # Resource sprite
```

---

## Documentations

Refer to these documentations for more information and better understanding throughout the tutorial:

- **Pygame**: [Pygame Documentation](https://www.pygame.org/docs/)
- **WebSockets**: [WebSockets Documentation](https://websockets.readthedocs.io/en/stable/)
- **Asyncio**: [Asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

**Alright, now that we're ready, let's *actually* get started!**

## Part 1: Creating the Game Client

### Explanation: Game Loop
A game loop is a continuous cycle that updates the game state and renders graphics. It consists of three main steps:
1. Processing user input
2. Updating game objects
3. Rendering the scene

### Implementing the Game Client
In this section, we will set up Pygame and create a basic game loop to handle player movement.

`main.py`
```python
import pygame

# Constants
WIDTH, HEIGHT = 800, 600

PLAYER_SPEED = 5
PLAYER_SIZE = 64

BACKGROUND_COLOR = (127, 64, 0)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Player position
player_x, player_y = WIDTH // 2, HEIGHT // 2

# Load sprites
player_sprite = pygame.image.load("player.png")
player_sprite = pygame.transform.scale(player_sprite, (PLAYER_SIZE, PLAYER_SIZE))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]: player_x += PLAYER_SPEED
    if keys[pygame.K_UP]: player_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]: player_y += PLAYER_SPEED

    window.fill(BACKGROUND_COLOR)
    window.blit(player_sprite, (player_x - PLAYER_SIZE // 2, player_y - PLAYER_SIZE // 2))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

> [!NOTE]
> `window.blit()` takes in the position of the top-left corner of the sprite, so we subtract half the sprite size to center it.

---

## Part 2: Creating the Game Server

### Explanation: WebSockets and Multithreading
- **WebSockets** allow full-duplex communication between the client and server, making it ideal for real-time multiplayer games.
- **Multithreading** lets us handle multiple connections simultaneously without blocking the main execution.

### Implementing the Game Server
We will now set up a simple WebSocket server using `websockets` to handle player connections and updates.

`server.py`
```python
import asyncio
import json
import random
import websockets

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 64

# Store player data
players = {}
next_player_id = 1
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
            
            # Broadcast updates to all clients
            update = json.dumps({"type": "update", "players": players})
            await asyncio.gather(*(client.send(update) for client in clients))
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        del players[player_id]
        clients.remove(websocket)

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # Keep server running

asyncio.run(main())
```

---

## Part 3: Connecting the Client and Server

### Explanation: Sending and Receiving Messages
In a multiplayer game, the client sends movement updates to the server, which then broadcasts them to all connected clients.

### Updating the Game Client to Connect to the Server
Now, we'll modify the client to send movement data to the server and receive updates about other players.

```python
import asyncio
import json
import pygame
import websockets

WIDTH, HEIGHT = 800, 600
FRAME_RATE = 60

PLAYER_SPEED = 5
PLAYER_SIZE = 64

BACKGROUND_COLOR = (127, 64, 0)

# Pygame setup
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load sprites
player_sprite = pygame.image.load("player.png")
player_sprite = pygame.transform.scale(player_sprite, (PLAYER_SIZE, PLAYER_SIZE))

async def game_loop(websocket):
    players = {}
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]: dx = PLAYER_SPEED
        if keys[pygame.K_UP]: dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN]: dy = PLAYER_SPEED

        if dx != 0 or dy != 0:
            await websocket.send(json.dumps({"type": "move", "dx": dx, "dy": dy}))

        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=0.1)
            data = json.loads(response)
            players = data.get("players", {})
        except asyncio.TimeoutError:
            pass

        window.fill(BACKGROUND_COLOR)
        for player_id, player in players.items():
            window.blit(player_sprite, (player["x"] - PLAYER_SIZE // 2, player["y"] - PLAYER_SIZE // 2))
        pygame.display.flip()
        clock.tick(FRAME_RATE)

async def main():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await game_loop(websocket)

asyncio.run(main())
```

---

## Part 4: Adding Resources and a Scoreboard

### Explanation: Managing Game Objects
- **Game objects** like resources and players are tracked using dictionaries or lists.
- **Collisions** between players and resources are detected by checking distance.

### Updating the Server to Spawn Resources
Modify the server to generate collectible resources.

Let's define constants for the time interval between resource spawns and the size of resources as well as a list to store resources,
along with a variable to assign unique IDs to each resource.

```python
RESOURCE_SPAWN_TIME = 5

RESOURCE_SIZE = 32

resources = []
next_resource_id = 1
```

Create an asynchronous function to spawn resources at random positions every few seconds.

```python
async def spawn_resources():
    global next_resource_id
    while True:
        await asyncio.sleep(5)
        resources.append({"id": next_resource_id, "x": random.randint(RESOURCE_SIZE, WIDTH - RESOURCE_SIZE), "y": random.randint(RESOURCE_SIZE, HEIGHT - RESOURCE_SIZE)})
        next_resource_id += 1

        update = json.dumps({"type": "update", "players": players, "resources": resources})
        await asyncio.gather(*(client.send(update) for client in clients))
```

We'll come back to `server.py` to add this function to the main coroutine.

### Updating the Client to Display Resources and Score
Let's first modify the client to render resources and show a simple scoreboard.

Start by defining the size of the resource sprite as a constant.

```python
RESOURCE_SIZE = 32
```

Load the sprite of the resource. In this case, we use a diamond image for the resource.

```python
diamond_sprite = pygame.image.load("diamond.png")
diamond_sprite = pygame.transform.scale(diamond_sprite, (RESOURCE_SIZE, RESOURCE_SIZE))
```

In the game loop, render the resources at their respective positions.

```python
for resource in resources:
    window.blit(diamond_sprite, (resource["x"] - RESOURCE_SIZE // 2, resource["y"] - RESOURCE_SIZE // 2))
```

Add a scoreboard displaying the number of resources collected by each player.

First, let's define constants for the text color and font size.

```python
TEXT_COLOR = (0, 0, 0)
TEXT_SIZE = 24
font = pygame.font.Font(None, TEXT_SIZE)
```

Let's render the "Leaderboard:" text on the screen.

```python
# Display leaderboard
font = pygame.font.Font(None, TEXT_SIZE)
text = font.render("Leaderboard", True, TEXT_COLOR)
window.blit(text, (10, 10))
```

Before displaying the player scores, sort the players based on their scores.

```python
# Sort players by score
sorted_players = sorted(players.items(), key=lambda p: p[1]["score"], reverse=True)
```

In the game loop, render the player scores on the screen.

```python
for i, (player_id, player) in enumerate(sorted_players):
    text = font.render(f"P{player_id}: {player['score']}", True, TEXT_COLOR)
    window.blit(text, (10, 30 + i * 20))
```

Finally, finalize the server to handle resource collection by players.

`server.py`
```python
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
next_player_id = 1
clients = set()

#---NEW CODE---
resources = []
next_resource_id = 1
#---------------

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
#-----------------NEW CODE-----------------
                # Check for resource collection
                for resource in resources[:]:
                    if abs(players[player_id]["x"] - resource["x"]) < PLAYER_SIZE / 2 and abs(
                            players[player_id]["y"] - resource["y"]) < PLAYER_SIZE / 2:
                        resources.remove(resource)
                        players[player_id]["score"] += 1
#------------------------------------------
            # Broadcast updates to all clients
            update = json.dumps({"type": "update", "players": players, "resources": resources})
            await asyncio.gather(*(client.send(update) for client in clients))
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        del players[player_id]
        clients.remove(websocket)

#-----------------NEW CODE-----------------
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
#------------------------------------------

#-----------------NEW CODE-----------------
async def server():
    async with websockets.serve(handle_client, "localhost", 8765):
        await asyncio.Future()  # Keep server running


async def main():
    asyncio.create_task(spawn_resources())
    await server()
#------------------------------------------

asyncio.run(main())
```

---

## Part 5: Running the Game and Server

To start the game, run the following commands in your terminal or command prompt:

1. **Start the Server**:

```sh
python server.py
```

2. **Start the Client**:

```sh
python main.py
```


4. **Allow Firewall Access**:
   Make sure your firewall allows incoming connections on port `8765`.

5. **Run the Server**:
   Start the server again, and players can now connect using your public IP.


---


## Part 6: Hosting the Server Publicly

To host the server publicly so players can connect from anywhere, follow these steps:

1. **Find Your Public IP**:
   Use a service like [whatismyip.com](https://www.whatismyip.com/) to find your public IP address.

2. **Port Forwarding**:
   Log into your router’s configuration page and forward port `8765` (or any other port you prefer) to your computer's local IP address.

3. **Update Server Code**:
   Modify the server code in `server.py` to listen on your public IP instead of `localhost`.

```python
async with websockets.serve(handle_client, "0.0.0.0", 8765):
    await asyncio.Future()  # Keep server running
```

## Conclusion
Congratulations! You have built a simple online multiplayer game with movement, resource collection, and a scoreboard - a perfect basis for a metaverse! Further enhancements could include animations, different player colors, or network optimizations. Happy coding!
