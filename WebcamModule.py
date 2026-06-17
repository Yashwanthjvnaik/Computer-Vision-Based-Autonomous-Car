import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("❌ Could not open webcam on index 0")

cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def getImg():
    success, img = cap.read()
    if success:
        return img
    return None

