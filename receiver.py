import socket
import os
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
DEFAULT_PORT = 12345
DEFAULT_SAVE_FOLDER = "Received_Files"

def receive_file(port, save_folder):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        logging.info(f"Created save folder: {save_folder}")

    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))  # Listen on all available interfaces
    server_socket.listen(1)

    logging.info(f"Waiting for a connection on port {port}...")

    try:
        # Accept a connection
        client_socket, client_address = server_socket.accept()
        logging.info(f"Connected by {client_address}")

        file_name = client_socket.recv(1024).decode()
        file_path = os.path.join(save_folder, file_name)

        total_bytes_received = 0
        with open(file_path, "wb") as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
                total_bytes_received += len(data)
                logging.info(f"Received {total_bytes_received} bytes...")

        logging.info(f"File '{file_name}' received successfully!")

        client_socket.send(b"File received successfully!")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        client_socket.close()
        server_socket.close()
        logging.info("Connection closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Receiver")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to listen on")
    parser.add_argument("--save-folder", type=str, default=DEFAULT_SAVE_FOLDER, help="Folder to save received files")
    args = parser.parse_args()

    receive_file(args.port, args.save_folder)