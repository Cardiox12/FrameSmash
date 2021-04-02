from FrameSmash import FrameSmash
import sys

usage = "usage: ./main.py video.avi"

if len(sys.argv) >= 2:
    path = sys.argv[1]
    print(path)

    fm = FrameSmash(path)
    fm.setup()
    fm.run()
else:
    print(usage)
