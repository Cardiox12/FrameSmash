import csv

class FramesSerializer:
    def __init__(self, filename, header):
        self.filename = filename
        self.header = header

        with open(filename, 'w') as f:
            self.writer = csv.writer(f, delimiter=',')

    def write_header(self):
        self.writer.writerow(self.header)

