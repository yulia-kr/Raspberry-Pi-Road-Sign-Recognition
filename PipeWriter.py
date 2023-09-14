import os


class PipeWriter:
    def __init__(self, pipePath):
        self.pipeHndl = os.open(pipePath, os.O_WRONLY)


    def write(self, line):
        os.write(self.pipeHndl, str.encode(line + "\n"))


    def close(self):
        os.close(self.pipeHndl)
