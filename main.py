from FrameSmash import FrameSmash
from PyQt5.QtWidgets import QApplication, QFileDialog

app = QApplication([])
filename, mode = QFileDialog.getOpenFileName(None, "Select File")

if len(filename) != 0:
    fm = FrameSmash(filename)
    fm.setup()
    fm.run()

