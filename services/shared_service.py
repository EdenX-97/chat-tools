class State:
    interrupted = False

    def interrupt(self):
        self.interrupted = True

    def recover(self):
        self.interrupted = False


state = State()
