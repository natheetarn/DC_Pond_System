import socket
import time
import threading

# importing shoutdown function
# import Shutdown
# Shutdown.shutdown_menu()

MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5007
INTERVAL = 2

def listen_to_signal():
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    multicast_socket.bind(('', MULTICAST_PORT))
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton('0.0.0.0'))
    
    multicast_socket.settimeout(5)
    try:
        while True:
            data, _ = multicast_socket.recvfrom(1024)
            print(f"Received: {data.decode()}")
            if data == "STATE_UPDATE_REQUEST":
                print("Received state update request. Sending current state...")
                current_state = time.strftime('%H:%M:%S', time.localtime())
                sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                sender_socket.sendto(current_state.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
                sender_socket.close()
                print(f"Sent current state: {current_state}")
    except socket.timeout:
        print("No signal received within 10 seconds.")
        set_up()
        
def set_up():
    print("SETTING UP AS FIRST POND")
    listen_thread = threading.Thread(target=listen_to_signal)
    listen_thread.start()

def send_multicast():
    multicast_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    multicast_send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    
    while True:
        current_time = time.strftime('%H:%M:%S', time.localtime())
        message = f"Current time1: {current_time}"
        multicast_send_socket.sendto(message.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
        print("Sent: ", message)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    listen_thread = threading.Thread(target=listen_to_signal)
    listen_thread.start()
    time.sleep(10)
    send_thread = threading.Thread(target=send_multicast)
    send_thread.start()