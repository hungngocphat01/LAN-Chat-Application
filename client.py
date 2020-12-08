#!/usr/bin/python3
from socket import *
from common_definitions import *
from qt5_frontend_client import *
import threading
import traceback
import time
import os.path

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
                msg = recvall(client_socket)
                L = len(FILE_SIGNAL)

                if (msg[:L] == FILE_SIGNAL):
                    # FILESIGNALsender\nfilename\ncontent
                    D = msg.find(b"\n", L + 1)
                    sender = msg[L:D].decode(ENCODING)
                    K = msg.find(b"\n", D + 1)
                    filename = msg[D + 1:K].decode(ENCODING)
                    content = msg[K + 1:]
                    print(f"File received: {sender}_{filename}")

                    with open(f"{sender}_{filename}", mode="wb") as f:
                        f.write(content)
                    
                    print(f"File written: {sender}_{filename}")
                    self.msg_received.emit(f"File received: {sender}_{filename}")
                else:
                    sender, content = msg.decode(ENCODING).split("\n")
                    msg = f"[{sender}] {content}"
                    print(f"Message received: {msg}")
                    self.msg_received.emit(msg)
            except:
                # Probably disconnected
                print(f"Received: {msg}")
                print("Server sent trash information. Disconnecting...")
                return
            

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
                # Read file to memory
                with open(path, mode="rb") as f:
                    file_content = f.read()
                # Parse filename
                path = path.replace("\\", "/")
                filename = path.split("/")[-1]

                msg_content = FILE_SIGNAL + filename.encode(ENCODING) + b"\n" + file_content

                client_socket.sendall(msg_content)
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