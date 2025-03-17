import socket

receiver_ip = socket.gethostbyname(socket.gethostname())
print("Receiver's IP Address:", receiver_ip)
