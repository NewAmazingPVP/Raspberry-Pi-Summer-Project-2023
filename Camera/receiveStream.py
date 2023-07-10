import cv2
import socket
import struct
import numpy as np
import asone
from asone import utils
from asone import ASOne

SERVER_HOST = "192.168.1.167"
SERVER_PORT = 10001

OUTPUT_HOST = '0.0.0.0'
OUTPUT_PORT = 10003

detector = ASOne(detector=asone.YOLOV8L_PYTORCH, use_cuda=True)

filter_classes = [
    'backpack', 'umbrella', 'handbag', 'suitcase', 'sports ball',
    'baseball bat', 'baseball glove', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'potted plant', 'bed', 'dining table', 'toilet',
    'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 'person', 'tv'
]

# Create a socket connection to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Create a socket for sending processed frames
output_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
output_socket.bind((OUTPUT_HOST, OUTPUT_PORT))
output_socket.listen(1)

while True:
    # Wait for a new client connection
    output_conn, addr = output_socket.accept()
    print("Client connected:", addr)

    try:
        # Receive and display the frames
        while True:
            # Receive the frame size as a 4-byte integer
            frame_size_data = client_socket.recv(4)

            frame_size = struct.unpack("!I", frame_size_data)[0]

            # Receive the frame data
            frame_data = b""
            while len(frame_data) < frame_size:
                remaining_size = frame_size - len(frame_data)
                frame_data += client_socket.recv(min(4096, remaining_size))

            # Decode the frame using OpenCV
            frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

            # Perform image detection on the frame
            dets, img_info = detector.detect(frame, filter_classes=filter_classes)

            bbox_xyxy = dets[:, :4]
            class_ids = dets[:, 5]
            
            frame = utils.draw_boxes(frame, bbox_xyxy, class_ids=class_ids)
                        
            # Encode the processed frame and send it over the network
            _, frame_data = cv2.imencode('.jpg', frame)
            frame_size = len(frame_data)

            try:
                # Send the frame size as a 4-byte integer
                output_conn.send(struct.pack("!I", frame_size))

                # Send the frame data
                output_conn.sendall(frame_data.tobytes())
            except ConnectionAbortedError:
                print("Connection with client aborted.")
                break

    except ConnectionResetError:
        print("Connection with client reset.")
    finally:
        output_conn.close()
