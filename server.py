from socket import *
from math import *
import threading
import traceback
from queue_msg import *
import sys

ENCODING = "utf-8"
MAXSIZE = 10000
THREAD_STOP = False

print("Multithread LAN chatting server.")
print("By Hung Ngoc Phat")
print("-----------------------------------------")
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

port = input("Enter server port: ")
server_socket.bind(("localhost", int(port)))
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
                print("All users has logged out. Server stopping...")
                global THREAD_STOP
                THREAD_STOP = True
            self = None
            
        def send_msg(self, msg: Message):
            content = msg.sender + "|||" + msg.content
            self.connector.sendall(content.encode(ENCODING))
            print(f"Message sent to {self.alias}")

        def receive_msg(self):
            while not THREAD_STOP:
                msg = self.connector.recv(MAXSIZE).decode(ENCODING)
                if (msg == "logout"):
                    self.send_msg(Message("Server", "Logout"))
                    self.__del__()
                    continue
                print(f"Received message from {self.alias}: {msg}")
                messages_queue.push(Message(sender = self.alias, content = msg))

    def broadcast():
        while not THREAD_STOP:
            while (messages_queue.size() > 0):
                msg = messages_queue.pop()
                for client in clients:
                    if (client.alias != msg.sender):
                        client.send_msg(msg)     

    def listen_new_clients():
        while not THREAD_STOP:
            c, a = server_socket.accept()
            print(f"Accepted new client at {a}")
            alias = c.recv(MAXSIZE).decode(ENCODING)
            print(f"Assigned alias to {a}: {alias}")
            clients.append(Client(connector = c, alias = alias, addr = a))
            for client in clients:
                if (client.alias != alias):
                    client.send_msg(Message("Server", "New client has joined"))    

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
        del clients[i]