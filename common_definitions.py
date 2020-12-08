MAXSIZE = 10000
FILE_SIGNAL = b"FILESIGNAL\r\n\x00"
ENCODING = "utf-8"

class Queue():
    def __init__(self):
        self.containter = []
    def size(self):
        return len(self.containter)
    def push(self, data):
        self.containter.append(data)
    def pop(self):
        if (self.size() > 0):
            val = self.containter[0]
            self.containter.pop(0)
            return val
        else:
            return None

class Message():
    def __init__(self, sender: str, content, mtype: str = "text"):
        self.mtype = mtype
        self.sender = sender
        self.content = content

class MessageHandler():
    def send(self, msg: Message):
        pass
    def receive(self):
        pass

def recvall(s):
    content = b""
    while True:
        recv = s.recv(MAXSIZE)
        content += recv
        if (len(recv) < MAXSIZE):
            break
    return content