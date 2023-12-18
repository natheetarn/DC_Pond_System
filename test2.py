import socket
import time

def setup_function():
    # Replace this function with your setup logic
    print("Running setup function...")

def get_current_time():
    # Replace this function to return the current time/state
    return time.strftime("%H:%M:%S", time.localtime())

# Create a UDP socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Allow other sockets to bind to this port
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
multicast_group = '239.255.255.250'
port = 1900
receiver_socket.bind(('', port))

# Tell the kernel that this is a multicast socket
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

# Add the socket to the multicast group on all interfaces
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton('0.0.0.0'))

# Set timeout for receiving messages
receiver_socket.settimeout(1.0)  # Set the timeout to 1 second

# Flag to track if setup function has been called
setup_done = False

# State variable to store current time/state
current_state = None

# Flag to track if this pond is the only one in the vivisystem
is_single_pond = True

# Receive/respond loop
while True:
    print("\nWaiting to receive messages...")
    try:
        data, address = receiver_socket.recvfrom(1024)
        received_message = data.decode()
        
        if received_message == "STATE_UPDATE_REQUEST":
            print("Received state update request. Sending current state...")
            current_state = get_current_time()
            sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sender_socket.sendto(current_state.encode(), (multicast_group, port))
            print(f"Sent current state: {current_state}")
            is_single_pond = False  # Other ponds are present
        # Add other processing for different types of received messages if needed
    except socket.timeout:
        if not setup_done:
            print("No reply received within 1 second. Setting up necessary data structures...")
            setup_function()
            setup_done = True  # Set the flag to True after setup is called
            
            if is_single_pond:
                print("This pond is the only one in the vivisystem.")
                # Perform setup for a single pond
                
            # Here, you can return to any saved state if needed for a multi-pond system
            # Placeholder for restoring saved state logic

        if current_state:
            print(f"Current state: {current_state}")
