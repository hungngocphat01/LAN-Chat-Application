from socket import *
from queue_msg import *
from client_frontend import *
import threading
import traceback
import time

ENCODING = "utf-8"
MAXSIZE = 10000
THREAD_STOP = False

print("Multithread LAN chatting client.")
print("-----------------------------------------")
ip = input("Enter server IP/hostname: ")
port = input("Enter server port: ")

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

def receive():
    while not THREAD_STOP:
        msg = client_socket.recv(MAXSIZE).decode(ENCODING)
        sender, content = msg.split("|||")
        msg = f"[{sender}] {content}"
        print(f"Message received: {msg}")
        ui.updateMessageHistoryBox(msg)

def send():
    msg = str(ui.messageInputBox.toPlainText())
    if (len(msg) > 0):
        client_socket.sendall(msg.encode(ENCODING))
        ui.updateMessageHistoryBox(msg)
    if (msg == "logout"):
        global THREAD_STOP
        THREAD_STOP = True

ui.sendButton.clicked.connect(send)

# Start background receive services
receive_daemon = threading.Thread(target=receive)
receive_daemon.start()

# Show application information
ui.messageHistoryBox.appendPlainText("Multithread LAN chatting client")
ui.messageHistoryBox.appendPlainText("Front-end powered by Qt5")
ui.messageHistoryBox.appendPlainText("Application by Hung Ngoc Phat\n")
ui.messageHistoryBox.appendPlainText(f"You are {alias}\n")

MainWindow.setWindowTitle(f"LAN Chatting Client - {alias}")

MainWindow.show()
r = app.exec_()

receive_daemon.join()
sys.exit(r)