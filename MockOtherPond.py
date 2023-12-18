import socket
import time

def get_current_time():
    # Replace this function to return the current time/state
    return time.strftime("%H:%M:%S", time.localtime())
# Set up multicast socket
multicast_group = '224.3.29.71'  # Replace with your multicast group address
port = 8888  # Replace with your multicast port number

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
hello_message = "Hello from Pond Y"  # Replace with pond's identifier
sock.sendto(hello_message.encode(), (multicast_group,port))

current_state = None

sock.settimeout(5)
while True:
    try:
        data, address = sock.recvfrom(1024)
        print(f"Received message from {address}: {data.decode()}")
        
        # print(f"Sent current state: {current_state}")
    except socket.timeout:
        if current_state:
            print(f"Current state: {current_state}")

