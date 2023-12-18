import socket
import time

def get_current_time():
    # Replace this function to return the current time/state
    return time.strftime("%H:%M:%S", time.localtime())

# Create a UDP socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Set the socket to allow broadcasting
sender_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

# Define the multicast address and port
multicast_group = '239.255.255.250'
port = 1900

# Flag to track if any ponds have responded
ponds_responded = False

while True:
    # Multicast state update request
    sender_socket.sendto(b"STATE_UPDATE_REQUEST", (multicast_group, port))
    print("Sent state update request to all ponds.")

    # Listen for responses within a certain period
    sender_socket.settimeout(5.0)  # Set timeout for responses
    try:
        data, address = sender_socket.recvfrom(1024)
        received_state = data.decode()
        print(f"Received state from {address}: {received_state}")
        ponds_responded = True  # Flag that at least one pond responded
    except socket.timeout:
        if not ponds_responded:
            print("No response received within 1 second.")

    # Process current state
    current_state = get_current_time()
    print(f"Current state: {current_state}")

    time.sleep(5)  # Wait for a certain period before sending the next state update request
