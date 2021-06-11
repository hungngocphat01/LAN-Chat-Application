# Simple Python LAN chatting application

**Disclaimer: I did it wrong by not sending the message size prior to the actual message, so the program is very buggy. It is not recommended to use this program as a reference for your project.**

## Introduction
- This project is a simple LAN chatting application written in Python 3 with multi-threading, implemented in client - server model.
- Uses low-level sockets to send/receive data.
- Graphical front-end written using PyQt5.
- Capable of sending/receiving file.

## Prerequisites
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
        sender_alias\nmessage_content
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
- Client packages the file and sends to server in the following format:
    ```
    <FILE_SIGNAL><filename>\n<file content>

    FILE_SIGNAL is b"FILESIGNAL\r\n\x00" by default.
    ```
- Server reveives and broadcast to all other clients in the following format:
    ```
    <FILE_SIGNAL><sender>\n<filename>\n<file content>
    ```
- Finally, client receives the file and saves in the below filename structure:
    ```
    <sender alias>_<original filename>
    ```

## Bugs
- Receive/send file works, but not as expected (information order seems to have been fcked up).
