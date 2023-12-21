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
        print("\nWaiting to receive messages...")
        data, address = sock.recvfrom(1024)  # Adjust buffer size if needed
        received_message = data.decode()
        print(received_message)
        if received_message == "STATE_UPDATE_REQUEST":
                print("Received state update request. Sending current state...")
                current_state = get_current_time()
                sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                sender_socket.sendto(current_state.encode(), (multicast_group, port))
                sender_socket.close()
                print(f"Sent current state: {current_state}")
    except socket.timeout:
        if current_state:
            print(f"Current state: {current_state}")

