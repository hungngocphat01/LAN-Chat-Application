#!/usr/bin/python3
from socket import *
from math import *
import threading
import traceback
from queue_msg import *
import sys
import time

ENCODING = "utf-8"
MAXSIZE = 10000
THREAD_STOP = False

print("Multithread LAN chatting server.")
print("By Hung Ngoc Phat")
print("-----------------------------------------")
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

ip = input("Enter server IP (blank for localhost): ")
port = input("Enter server port (blank for 8000): ")
if len(ip) == 0: ip = "localhost"
if len(port) == 0: port = 8000

server_socket.bind((ip, int(port)))
server_socket.listen(5)

clients = []
messages_queue = Queue()

try:
    class Client:
        def __init__(self, connector: socket, alias: str, addr: tuple):
            self.connector = connector
            self.alias = alias
            self.addr = addr

            self.recv_daemon = threading.Thread(target = self.receive_msg)
            self.recv_daemon.start()

        def __del__(self):
            self.connector.close()
            # Remove from client list
            for i in range(0, len(clients)):
                if (clients[i] == self):
                    clients.pop(i) 
                    break
            # If their is no client left, stop the server
            if (len(clients) == 0):
                print("All users had logged out. Server stopping...")
                global THREAD_STOP
                THREAD_STOP = True
            self = None
            
        def send_msg(self, msg: Message):
            if (msg.mtype == "file"):
                self.connector.sendall("$$file$$".encode(ENCODING))
                self.connector.sendall(msg.sender.encode(ENCODING))
                self.connector.sendall(msg.content[0].encode(ENCODING))
                consent = self.connector.recv(MAXSIZE).decode(ENCODING)
                if (consent == "$$accept$$"):
                    # Send
                    self.connector.sendall(msg.content[1])
                else:
                    print(f"{self.alias} refused to receive file.")

            else:
                content = msg.sender + "|||" + msg.content
                self.connector.sendall(content.encode(ENCODING))
                print(f"Message sent to {self.alias}")

        def receive_msg(self):
            while not THREAD_STOP:
                msg = self.connector.recv(MAXSIZE).decode(ENCODING)
                if (msg == "$$file$$"):
                    time.sleep(0.2)
                    filename = self.connector.recv(MAXSIZE).decode(ENCODING)
                    content = b""
                    filebytes = []
                    time.sleep(0.2)
                    while len(content) > 0:
                        content = self.connector.recv(MAXSIZE)
                        filebytes.append(content)
                    pkg = (filename, filebytes)
                    print(f"Received file from {self.alias}: {filename}")
                    messages_queue.push(Message(sender=self.alias, content=pkg, mtype="file"))
                elif (msg == "logout"):
                    self.__del__()
                    break
                else:
                    print(f"Received message from {self.alias}: {msg}")
                    messages_queue.push(Message(sender = self.alias, content = msg))
    def sendtoall(msg: Message):
        if (len(clients) <= 1):
            print("Not enough client to distrubute message.")
            return
        for client in clients:
            if (client.alias != msg.sender):
                client.send_msg(msg)     

    def broadcast():
        while not THREAD_STOP:
            while (messages_queue.size() > 0):
                msg = messages_queue.pop()
                sendtoall(msg)

    def listen_new_clients():
        while not THREAD_STOP:
            c, a = server_socket.accept()
            print(f"Accepted new client at {a}")
            alias = c.recv(MAXSIZE).decode(ENCODING)
            print(f"Assigned alias to {a}: {alias}")
            clients.append(Client(connector = c, alias = alias, addr = a))
            for client in clients:
                if (client.alias != alias):
                    client.send_msg(Message("Server", f"New client has joined: {alias}"))    

    listen_daemon = threading.Thread(target = listen_new_clients)
    broadcast_daemon = threading.Thread(target = broadcast)

    listen_daemon.daemon = True
    broadcast_daemon.daemon = True

    listen_daemon.start()
    broadcast_daemon.start()

    broadcast_daemon.join()

except:
    print(traceback.format_exc())
finally:
    print("Closing all connections.")
    server_socket.close()

    for i in range(0, len(clients)):
        clients[i].__del__()