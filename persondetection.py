import cv2
import os

_proto  = "MobileNetSSD_deploy.prototxt"
_model  = "MobileNetSSD_deploy.caffemodel"

if not os.path.exists(_proto) or not os.path.exists(_model):
    raise FileNotFoundError(
        "Model files missing! Make sure MobileNetSSD_deploy.prototxt "
        "and MobileNetSSD_deploy.caffemodel are in the same folder."
    )

net = cv2.dnn.readNetFromCaffe(_proto, _model)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow",
    "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

def detectPerson(img, confidence_threshold=0.5):
    """
    Returns (annotated_img, person_found).
    person_found is True if at least one person is detected above threshold.
    """
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(img, (300, 300)),
        0.007843,
        (300, 300),
        127.5
    )
    net.setInput(blob)
    detections = net.forward()

    person_found = False

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_threshold:
            idx = int(detections[0, 0, i, 1])
            if CLASSES[idx] == "person":
                person_found = True
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                x1, y1, x2, y2 = box.astype("int")
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    img, "PERSON",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 255, 0), 2
                )

    return img, person_found