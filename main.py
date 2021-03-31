import cv2
from FramesSerializer import FramesSerializer
from FrameSmash import FrameSmash

path = "./data/cross.avi"

fm = FrameSmash(path)
fm.run()
