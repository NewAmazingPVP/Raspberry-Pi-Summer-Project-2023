import cv2
import socket
import struct
import numpy as np
import time
import asone
from asone import utils
from asone import ASOne

# Server host and port
SERVER_HOST = "192.168.1.157"
SERVER_PORT = 10001

# Create a socket connection to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

#detector = ASOne(detector=asone.YOLOV8L_PYTORCH , use_cuda=True)

"""filter_classes = [
    'backpack', 'umbrella', 'handbag','suitcase','sports ball',
    'baseball bat', 'baseball glove', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'sofa', 'potted plant', 'bed', 'dining table', 'toilet', 'tvmonitor',
    'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 'person'
]"""

# Receive and display the frames
try:
    while True:
        # Receive the frame size as a 4-byte integer
        frame_size_data = client_socket.recv(4)

        # Unpack the frame size
        frame_size = struct.unpack("!I", frame_size_data)[0]

        # Receive the frame data
        frame_data = b""
        while len(frame_data) < frame_size:
            remaining_size = frame_size - len(frame_data)
            frame_data += client_socket.recv(min(4096, remaining_size))

        # Decode the frame using OpenCV
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
        
        # Resize the frame to a smaller resolution
        #frame = cv2.resize(frame, (640, 480))

        # Perform image detection on the resized frame
        #dets, img_info = detector.detect(frame, filter_classes=filter_classes)

        # Convert dets to a numpy array if it's not already
        #dets = np.array(dets)

        # Filter out detections with confidence less than 0.7
        #dets = dets[dets[:, 4] > 0.3]

        # Sorting the detections based on confidence scores in descending order
        #dets = dets[dets[:, 4].argsort()[::-1]]

        # Limit to top 3 detections
        #dets = dets[:1]

        #bbox_xyxy = dets[:, :4]
        #scores = dets[:, 4]
        #class_ids = dets[:, 5]

        #frame = utils.draw_boxes(frame, bbox_xyxy, class_ids=class_ids)


        # Display the frame
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


finally:
    # Clean up the connection
    cv2.destroyAllWindows()
    client_socket.close()
