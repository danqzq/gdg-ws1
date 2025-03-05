# Workshop Additional Notes

Here are some notes and links to additional sources on the concepts covered in this workshop:

### 1. Understanding Asynchronous Programming

Asynchronous programming allows a program to handle multiple operations concurrently, which is essential for tasks like real-time networking. In Python, the `asyncio` library facilitates this by enabling the writing of asynchronous code using `async` and `await` keywords.

**Key Concepts:**

- **Coroutines:** Functions defined with `async def` that can be paused and resumed, allowing other operations to run during the pause.
- **Event Loop:** The core of `asyncio` that schedules and runs asynchronous tasks and callbacks.
- **Tasks:** Wrappers for coroutines that allow them to run concurrently.

**Recommended Resources:**

- [Using Asyncio With Websockets For Real-time Data Streaming In Python](https://peerdh.com/blogs/programming-insights/using-asyncio-with-websockets-for-real-time-data-streaming-in-python)
- [Building WebSocket Servers and Clients with asyncio](https://www.pythonlore.com/building-websocket-servers-and-clients-with-asyncio/)

### 2. WebSockets Communication

WebSockets provide a full-duplex communication channel over a single TCP connection, making them ideal for real-time applications like multiplayer games. The `websockets` library in Python allows for the creation of both WebSocket servers and clients.

**Key Points:**

- **Establishing Connections:** Using `websockets.connect()` for clients and `websockets.serve()` for servers to initiate communication.
- **Sending and Receiving Messages:** Utilizing `await websocket.send()` and `await websocket.recv()` for data transmission.
- **Handling Multiple Clients:** Managing multiple connections concurrently using asynchronous functions.

**Recommended Resources:**

- [Part 1 - Send & receive - websockets 15.0 documentation](https://websockets.readthedocs.io/en/stable/intro/tutorial1.html)
- [Python WebSockets Example - Python Examples](https://pythonexamples.org/python-websockets-example/)

### 3. Game Loop and Concurrent Networking

Integrating the game loop with networking requires careful handling to ensure smooth gameplay and real-time data synchronization. Pygame manages the game loop, while `asyncio` handles networking tasks.

**Strategies:**

- **Concurrent Execution:** Running the Pygame event loop and networking coroutines concurrently using `asyncio.create_task()`.
- **Synchronization:** Ensuring that game state updates are synchronized across all clients to maintain consistency.

**Recommended Resources:**

- [Python Online Game Tutorial - Sockets and Networking - Tech with Tim](https://www.techwithtim.net/tutorials/python-online-game-tutorial)
- [Advanced Game Networking Protocols with Pygame - Code with C](https://www.codewithc.com/advanced-game-networking-protocols-with-pygame/)

### 4. Resource Collection and State Synchronization

Implementing resource collection mechanics requires the server to manage the game state and synchronize it across all clients.

**Considerations:**

- **Server Authority:** The server should validate all actions (e.g., resource collection) to prevent cheating.
- **State Updates:** The server broadcasts the updated game state to all clients after any change.
- **Latency Handling:** Implementing techniques to mitigate the effects of network latency on gameplay.

**Recommended Resources:**

- [Real-Time P2P Networking in Pygame - Code with C](https://www.codewithc.com/real-time-p2p-networking-in-pygame/)
- [Basics for network communication in python - Medium](https://medium.com/analytics-vidhya/basics-for-network-communication-on-python-af3f677af42c)

### 5. Hosting the Server Publicly

Making the server accessible over the internet involves configuring network settings and ensuring security.

**Steps:**

- **Port Forwarding:** Configuring your router to forward external traffic on a specific port to your server's local IP address.
- **Firewall Configuration:** Ensuring that the server's firewall allows incoming connections on the chosen port.
- **Dynamic DNS:** Using a dynamic DNS service if your public IP address changes frequently.

**Recommended Resources:**

- [Build WebSocket Server and Client Using Python](https://geekpython.in/build-websocket-server-and-client-using-python)
- [How To Build WebSocket Server And Client in Python - PieHost](https://piehost.com/websocket/python-websocket)

### 6. Debugging Multiplayer Issues

Debugging multiplayer games can be complex due to the involvement of networking, concurrency, and real-time interactions.

**Approaches:**

- **Logging:** Implementing comprehensive logging on both the client and server to trace actions and identify issues.
- **Simulating Network Conditions:** Testing the game under various network conditions (e.g., latency, packet loss) to ensure robustness.
- **Automated Testing:** Developing automated tests for game mechanics and networking components to catch issues early.

**Recommended Resources:**

- [Python Online Game Tutorial #1 - Creating a Client Using Sockets](https://www.youtube.com/watch?v=_fx7FQ3SP0U)
- [Online-Multiplayer-game-with-python-networking-using-sockets - GitHub](https://github.com/VISWANTHAN1/Online-Multiplayer-game-with-python-networking-using-sockets)
