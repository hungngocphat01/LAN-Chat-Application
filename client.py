#!/usr/bin/python3
from socket import *
from queue_msg import *
from qt5_frontend_client import *
import threading
import traceback
import time

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
        client_socket.sendall(msg.encode(ENCODING))
        print(f"Message sent: {msg}")
        ui.updateMessageHistoryBox("[Me] " + msg)
        ui.clearMessageBox()
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