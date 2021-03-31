import cv2

cap = cv2.VideoCapture('./data/cross.avi')


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Left Click : {x}x{y}")
    elif event == cv2.EVENT_RBUTTONDOWN:
        print(f"Right Click : {x}x{y}")


cv2.namedWindow('frame', cv2.WINDOW_GUI_NORMAL)
cv2.setMouseCallback('frame', on_mouse)

frame_index = 0
frame_buffer = []

ret, frame = cap.read()
frame_buffer.append(frame)
while True:
    # Show image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)

    key = cv2.waitKey(1) & 0xFF

    # Quit
    if key == ord('q'):
        break
    # Next frame
    elif key == ord('n'):
        ret, frame = cap.read()
        frame_buffer.append(frame)
        frame = frame_buffer[frame_index]
        frame_index += 1
    # Previous frame
    elif key == ord('b'):
        frame_index -= 1
        if frame_index < 0:
            frame_index = 0
        frame = frame_buffer[frame_index]
    elif cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
        break


cap.release()
cv2.destroyAllWindows()


