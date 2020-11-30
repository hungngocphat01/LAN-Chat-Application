# Simple Python LAN chatting application

## Introduction
- This project is a simple LAN chatting application written in Python 3 with multithreading, implemented in client - server model.
- Uses low-level sockets to send/receive data.
- Graphical front-end written using PyQt5.
- Capable of sending/receiving file.

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

## Text message transmission process
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
    - The server will close its connection with the client, and remove the client from list.
    - If there is no client left, the server will stop background threads and stop.
## File transmission process
- The user can require the client to send a file by sending a message in the following structure:
    ```
    file$<path>
    ```
- Client sends ``$$file$$`` signal to server.
- Server prepares to receive the file.
- Clients send filename and file content respectively.
- Server receive both respectively and enqueue it like a normal text message.
- Server distributes the ``$$file`` signal to other clients, then the file sender and filename, waiting for client's approval.
- If an agreement has been detected, the server will send the whole file to the client.
- The clients receive the file by chunks (~10KB each by default), then write it to the current directory with filename:
    ```
    <sender alias>_<original filename>
    ```

## Bugs
- Cannot send and receive file at the moment.

