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
    def __init__(self, sender: str, content: str):
        self.sender = sender
        self.content = content