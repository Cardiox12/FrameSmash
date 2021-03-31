import cv2

class FrameSmash:
    QUIT_KEY = ord('q')
    NEXT_KEY = ord('n')
    PREV_KEY = ord('b')

    def __init__(self, path):
        self.click_count = 0
        self.frame_index = 0
        self.click_buffer = []
        self.frame_buffer = []
        self.frame = None
        self.appname = "frame"
        self.cap = cv2.VideoCapture(path)

        cv2.namedWindow(self.appname, cv2.WINDOW_GUI_NORMAL)
        cv2.setMouseCallback(self.appname, self.on_mouse)

    def run(self):
        ret, self.frame = self.cap.read()
        self.frame_buffer.append(self.frame)

        while True:
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow(self.appname, gray)

            key = cv2.waitKey(1) & 0xFF

            if key == FrameSmash.QUIT_KEY:
                break
            elif key == FrameSmash.NEXT_KEY:
                ret, self.frame = self.cap.read()
                self.frame_buffer.append(self.frame)
                self.frame = self.frame_buffer[self.frame_index]
                self.frame_index += 1
            elif key == FrameSmash.PREV_KEY:
                self.frame_index -= 1
                if self.frame_index < 0:
                    self.frame_index = 0
                self.frame = self.frame_buffer[self.frame_index]
            elif cv2.getWindowProperty(self.appname, cv2.WND_PROP_VISIBLE) < 1:
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def on_mouse(self, event, x, y, flags, param):
        if event in [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_RBUTTONDOWN]:
            print("Mouse clicked")

