import socket
import threading
from time import sleep

UDP_IP = "192.168.1.55"
UDP_PORT = 8765
MESSAGE = "Hello, World!"

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
#sock.bind((UDP_IP, UDP_PORT))

def send():
    while True:
        try:
            sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
            sleep(1)
            print("sent message:", MESSAGE)
        except Exception as e:
            print("send:", e)
            sock.close()
            break

'''def receive():
    while True:
        try:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            print ("received message:", data)
        except Exception as e:
            print("receive:", e)
            sock.close()
            break

threading.Thread(target=receive).start()'''
threading.Thread(target=send).start()