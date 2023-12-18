import socket
import time

set_up = False

def setup_function():
    print("No replies, setting up system")




# Create a UDP socket
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Allow other sockets to bind to this port
receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
multicast_group = '224.3.29.71'
port = 8888
receiver_socket.bind(('', port))

# Tell the kernel that this is a multicast socket
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

# Add the socket to the multicast group on all interfaces
receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicast_group) + socket.inet_aton('0.0.0.0'))
receiver_socket.settimeout(10.0)  # Set the timeout to 1 second

hello_message = "Hello from Pond X"  # Replace with pond's identifier
receiver_socket.sendto(hello_message.encode(), (multicast_group,port))
def request_update():
    message = "STATUS_UPDATE_REQUEST"
    receiver_socket.sendto(message.encode(), (multicast_group, port))
    data, address = receiver_socket.recvfrom(1024)
    data = data.decode()
    print("UPDATED: ", address, data)
    return data
# Receive/respond loop
while True:
    try:
        print("\nWaiting to receive messages...")
        data, address = receiver_socket.recvfrom(1024)
        print(f"Received message from {address}: {data.decode()}")
        #request_update()
        set_up = True

    except socket.timeout:
        if not set_up:
            print("No reply received within 1 second. Calling setup function...")
            setup_function()
            set_up = True
        

