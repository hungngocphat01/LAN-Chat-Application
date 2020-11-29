# Simple Python LAN chatting application

## Introduction
- This project is a simple LAN chatting application written in Python 3 with multithreading, implemented in client - server model.
- Uses low-level sockets to send/receive data.
- Graphical front-end written using PyQt5.

## Prequisites
- Python 3 (tested on 3.8.6).
- pyqt5.

## Source code
- **client.py** and **server.py**: implementation of the client and server side respectively.
- **queue_msg.py**: definition of ``Queue`` and ``Message`` classes.

## Initialization process
- Server should be started first. Upon starting up, a server port has to be specified.
- Then client(s) should also be started. Server IP and server port will be asked.
- Server accepts connection from client.
- On the client side, an alias will be required.
- Server retrieves and assigns client's alias.
- Client starts its receiving and sending threads.
- The same process is repeated for all other clients.

## Message transmission process
- User consents to send a message to server.
- Server receives message from client.
- The message will be enqueued, waiting to be processed.
- Message processing:
    - The message will be packaged in the following structure:
        ```
        sender_alias|||message_content
        ```
    - Finally, it will be distributed to all other clients.
- If *"logout"* message is sent
    - The background threads from the client side will cease.
    - The server will close its connection with the client, and remove the client from connection list.
    - If there is no client left, the server will stop its background threads and exit.

## Bugs
- When a new message arrives at the client side, the user have to click on the message box to update it (problems of multithreading, will fix later).
- Even when all clients have been left, the server has to be stopped manually by sending ``Ctrl-C``.

