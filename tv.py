import threading

class Television:
    def __init__(self, c = threading.Semaphore(0), s = threading.Semaphore(1), mutex1 = threading.Semaphore(1), mutex2 = threading.Semaphore(1), channel = 0, w = 0, up = 0):
        self.c = c
        self.s = s
        self.mutex1 = mutex1
        self.mutex2 = mutex2
        self.w = w
        self.up = up
        self.channel = channel
