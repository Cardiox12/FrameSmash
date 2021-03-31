import cv2
from FramesSerializer import FramesSerializer

class FrameSmash:
    QUIT_KEY = ord('q')
    NEXT_KEY = ord('n')
    PREV_KEY = ord('b')
    MAX_CLICK = 4
    def __init__(self, path):
        self.path = path
        self.click_count = 0
        self.frame_index = 0
        self.click_buffer = []
        self.frame_buffer = []
        self.frame = None
        self.appname = "frame"
        self.cap = None

        self.header = ["Header"] + [f"{c}{i}" for i in range(4) for c in ['X', 'Y']] + [f"feat{i}" for i in range(4)]
        self.csv_name = None
        self.serializer = None

    def setup(self):
        self.cap = cv2.VideoCapture(self.path)
        cv2.namedWindow(self.appname, cv2.WINDOW_GUI_NORMAL)
        cv2.setMouseCallback(self.appname, self.on_mouse)
        self.csv_name = self._get_csv_filename(self.path)

    def run(self):
        with open(self.csv_name, "w") as f:
            self.serializer = FramesSerializer(f, self.header)
            self.serializer.write_header()

            ret, self.frame = self.cap.read()
            self.frame_buffer.append(self.frame)

            while True:
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                cv2.imshow(self.appname, gray)

                key = cv2.waitKey(1) & 0xFF

                if key == FrameSmash.QUIT_KEY:
                    break
                elif key == FrameSmash.NEXT_KEY:
                    self.get_next_frame()
                    self.serialize()
                    self.click_buffer = []
                    self.click_count = 0
                elif key == FrameSmash.PREV_KEY:
                    self.get_prev_frame()
                elif cv2.getWindowProperty(self.appname, cv2.WND_PROP_VISIBLE) < 1:
                    break

        self.cap.release()
        cv2.destroyAllWindows()

    def get_next_frame(self):
        ret, self.frame = self.cap.read()
        self.frame_buffer.append(self.frame)
        self.frame = self.frame_buffer[self.frame_index]
        self.frame_index += 1

    def get_prev_frame(self):
        self.frame_index -= 1
        if self.frame_index < 0:
            self.frame_index = 0
        self.frame = self.frame_buffer[self.frame_index]

    def on_mouse(self, event, x, y, flags, param):
        if event in [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_RBUTTONDOWN]:
            if self.click_count < FrameSmash.MAX_CLICK:
                feat = event == cv2.EVENT_RBUTTONDOWN
                self.click_buffer.append(
                    (x, y, feat)
                )
                self.click_count += 1
            else:
                print("Limit exceeded")

    def serialize(self):
        features = [item[-1] for item in self.click_buffer]
        clicks = [coord for item in self.click_buffer for coord in item[:-1]]
        row = [self.frame_index] + clicks + features
        self.serializer.write_data(row)

    @staticmethod
    def _get_csv_filename(path):
        filename = path.split('/')[-1].split('.')[0]
        return f"{filename}.csv"