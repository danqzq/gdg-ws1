import asyncio
import json
import pygame
import websockets

# Constants
WIDTH, HEIGHT = 800, 600
FRAME_RATE = 60
WEBSOCKET_SEND_TIMEOUT = 0.1

PLAYER_SPEED = 5
PLAYER_SIZE = 64
RESOURCE_SIZE = 32

BACKGROUND_COLOR = (127, 64, 0)

TEXT_COLOR = (0, 0, 0)
TEXT_SIZE = 24

# Pygame setup
pygame.init()
font = pygame.font.Font(None, TEXT_SIZE)
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load sprites
player_sprite = pygame.image.load("player.png")
player_sprite = pygame.transform.scale(player_sprite, (PLAYER_SIZE, PLAYER_SIZE))

diamond_sprite = pygame.image.load("diamond.png")
diamond_sprite = pygame.transform.scale(diamond_sprite, (RESOURCE_SIZE, RESOURCE_SIZE))


async def game_loop(websocket):
    players = {}
    resources = []

    global font

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Handle player input and movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]: dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]: dx = PLAYER_SPEED
        if keys[pygame.K_UP]: dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN]: dy = PLAYER_SPEED

        # If there's movement, send it to the server
        if dx != 0 or dy != 0:
            await websocket.send(json.dumps({"type": "move", "dx": dx, "dy": dy}))

        # Receive updates from the server
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=WEBSOCKET_SEND_TIMEOUT)
            data = json.loads(response)
            players = data.get("players", {})
            resources = data.get("resources", [])
        except asyncio.TimeoutError:
            pass

        window.fill(BACKGROUND_COLOR)

        for player_id, player in players.items():
            window.blit(player_sprite, (player["x"] - PLAYER_SIZE // 2, player["y"] - PLAYER_SIZE // 2))
            text = font.render(f"P{player_id}: {player['score']}", True, TEXT_COLOR)
            window.blit(text, (player["x"], player["y"] - 15))

        for resource in resources:
            window.blit(diamond_sprite, (resource["x"] - RESOURCE_SIZE // 2, resource["y"] - RESOURCE_SIZE // 2))

        # Display leaderboard
        text = font.render("Leaderboard", True, TEXT_COLOR)
        window.blit(text, (10, 10))

        # Sort players by score
        sorted_players = sorted(players.items(), key=lambda p: p[1]["score"], reverse=True)

        for i, (player_id, player) in enumerate(sorted_players):
            text = font.render(f"P{player_id}: {player['score']}", True, TEXT_COLOR)
            window.blit(text, (10, 30 + i * 20))

        pygame.display.flip()
        clock.tick(FRAME_RATE)


async def main():
    async with websockets.connect("ws://localhost:8765") as websocket:
        await game_loop(websocket)


asyncio.run(main())
