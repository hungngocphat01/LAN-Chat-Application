#!/usr/bin/python3
from socket import *
from queue_msg import *
from qt5_frontend_client import *
import threading
import traceback
import time
import os.path

ENCODING = "utf-8"
MAXSIZE = 10000
THREAD_STOP = False

print("Multithread LAN chatting client.")
print("-----------------------------------------")
ip = input("Enter server IP/hostname (blank for localhost): ")
port = input("Enter server port (blank for 8000): ")
if len(port) == 0: port = 8000

client_socket = socket (AF_INET, SOCK_STREAM)
client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
client_socket.connect((ip, int(port)))
print("Connection established\n")
alias = input("Enter this client's alias: ")
client_socket.sendall(alias.encode('ascii'))

# Setup client front-end
app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_Form()
ui.setupUi(MainWindow)

class MsgRetrieveThread(QThread):
    msg_received = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        
    def run(self):
        while True:
            try:
                msg = client_socket.recv(MAXSIZE).decode(ENCODING)
                # Server wants to send file
                if (msg == "$$file$$"):
                    time.sleep(0.2)
                    sender = client_socket.recv(MAXSIZE).decode(ENCODING)
                    time.sleep(0.2)
                    filename = client_socket.recv(MAXSIZE).decode(ENCODING)
                    accept = QMessageBox(parent=MainWindow, text=f"Do you want to receive {filename} from {sender}?", buttons=QMessageBox.Yes | QMessageBox.No)
                    if (accept == QMessageBox.Yes):
                        # Notify to server
                        client_socket.sendall("$$accept$$".encode(ENCODING))
                        # Receive the whole file
                        filebytes = []
                        time.sleep(0.2)
                        while True:
                            content = client_socket.recv(MAXSIZE)
                            if (len(content) == 0):
                                break
                            filebytes.append(content)
                        with open(f"{sender}_{filename}", mode="wb") as f:
                            for chunk in filebytes:
                                f.write(chunk)
                    else:
                        client_socket.sendall("$$refuse$$".encode(ENCODING))

                # Normal text message
                else:
                    sender, content = msg.split("|||")
            except:
                # Probably disconnected
                print(f"Received: {msg}")
                print("Server sent trash information. Disconnecting...")
                return
            
            msg = f"[{sender}] {content}"
            print(f"Message received: {msg}")

            self.msg_received.emit(msg)

def send():
    msg = str(ui.messageInputBox.toPlainText())
    if (len(msg) > 0):
        # If user wants to send a file
        if (msg.find("file$") == 0):
            path = msg.split("file$")
            if (len(path) <= 1 or not os.path.exists(path[1])):
                QMessageBox(parent=MainWindow, text="Invalid path. Please check again!")
            else:
                path = path[1]
                # Send: "$$file$$"
                client_socket.sendall("$$file$$".encode(ENCODING))
                # Send filename
                path = path.replace("\\", "/")
                filename = path.split("/")[-1]
                client_socket.sendall(filename.encode(ENCODING))
                # Send file content
                with open(path, mode="rb") as f:
                    client_socket.sendall(f.read())
        # Normal text:
        else:
            client_socket.sendall(msg.encode(ENCODING))
            print(f"Message sent: {msg}")
            ui.updateMessageHistoryBox("[Me] " + msg)
            ui.clearMessageBox()
        # If user wants to logout
        if (msg == "logout"):
            print("Connection closure requested.")
            client_socket.close()
            MainWindow.close()

# Bind Send button and Enter key to send function
ui.sendButton.clicked.connect(send)

# Start background receive thread
receive_daemon = MsgRetrieveThread()
receive_daemon.msg_received.connect(ui.updateMessageHistoryBox)
receive_daemon.start()

# Show application information
ui.messageHistoryBox.appendPlainText("Multithread LAN chatting client")
ui.messageHistoryBox.appendPlainText("Front-end powered by Qt5")
ui.messageHistoryBox.appendPlainText("Application by Hung Ngoc Phat\n")
ui.messageHistoryBox.appendPlainText(f"You are {alias}\n")

MainWindow.setWindowTitle(f"LAN Chatting Client - {alias}")

MainWindow.show()
r = app.exec_()

client_socket.close()
print("Connection closed.")

sys.exit(r)