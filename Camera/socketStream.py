import cv2
import socket
import struct
import threading

from picamera2 import Picamera2
from libcamera import controls

# Initialize the camera

tuning = Picamera2.load_tuning_file("imx708_noir.json")
picam2 = Picamera2(tuning=tuning)
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.set_controls({"AwbMode": controls.AwbModeEnum.Auto})
picam2.set_controls({"AeConstraintMode": controls.AeConstraintModeEnum.Normal})
picam2.set_controls({"AeExposureMode": controls.AeExposureModeEnum.Normal})
picam2.set_controls({"AeMeteringMode": controls.AeMeteringModeEnum.Matrix})
#picam2.set_controls({'ColourGains': (1.0, 1.2)})

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 10001
BUFFER_SIZE = 4096

# Function to handle a client connection
def handle_client(client_socket):
    try:
        while True:
            frame = picam2.capture_array()
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            # Prepare the frame for sending
            frame_data = buffer.tobytes()
            frame_size = len(frame_data)

            # Pack the frame size as a 4-byte integer
            frame_size_data = struct.pack("!I", frame_size)

            client_socket.sendall(frame_size_data)

            client_socket.sendall(frame_data)

    except:
        # Error occurred, close the client socket
        client_socket.close()

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New client connected: {client_address}")

        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

except KeyboardInterrupt:
    server_socket.close()
    print("Server stopped")
