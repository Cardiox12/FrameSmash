import csv

class FramesSerializer:
    def __init__(self, file, header):
        self.header = header
        self.writer = csv.writer(file, delimiter=',')

    def write_header(self):
        self.writer.writerow(self.header)
