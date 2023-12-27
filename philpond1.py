import socket
import time
import threading
import json
import logging

MULTICAST_GROUP = "224.1.1.1"
MULTICAST_PORT = 5008
INTERVAL = 2
STATE_FILE = "pond1_state.json"
LOG_FILE = "pond1_log.txt"


def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def save_state(state):
    with open(STATE_FILE, "w") as file:
        json.dump(state, file)


def load_state():
    try:
        with open(STATE_FILE, "r") as file:
            state = json.load(file)
        return state
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def listen_to_signal(state):
    multicast_socket = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
    )
    multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    multicast_socket.bind(("", MULTICAST_PORT))
    multicast_socket.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(MULTICAST_GROUP) + socket.inet_aton("0.0.0.0"),
    )

    multicast_socket.settimeout(5)
    try:
        while True:
            data, _ = multicast_socket.recvfrom(1024)
            decoded_data = data.decode()
            print(f"Received: {decoded_data}")
            logging.info(f"Received: {decoded_data}")
            if decoded_data == "STATE_UPDATE_REQUEST":
                print("Received state update request. Sending current state...")
                logging.info("Received state update request. Sending current state...")
                current_state = time.strftime("%H:%M:%S", time.localtime())
                sender_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
                )
                sender_socket.sendto(
                    current_state.encode(), (MULTICAST_GROUP, MULTICAST_PORT)
                )
                sender_socket.close()
                print(f"Sent current state: {current_state}")
                logging.info(f"Sent current state: {current_state}")
                state["last_update"] = current_state
                save_state(state)
    except socket.timeout:
        print("No signal received within 5 seconds.")
        logging.warning("No signal received within 5 seconds.")
        set_up(state)


def set_up(state):
    print("SETTING UP AS FIRST POND")
    logging.info("SETTING UP AS FIRST POND")
    listen_thread = threading.Thread(target=listen_to_signal, args=(state,))
    listen_thread.start()


def send_multicast():
    multicast_send_socket = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
    )
    multicast_send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    while True:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        message = f"Current time1: {current_time}"
        multicast_send_socket.sendto(
            message.encode(), (MULTICAST_GROUP, MULTICAST_PORT)
        )
        print("Sent: ", message)
        logging.info("Sent: %s", message)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    setup_logging()
    state = load_state() or {"last_update": None, "is_set_up": False}
    if not state["is_set_up"]:
        set_up(state)
        state["is_set_up"] = True
        save_state(state)

    listen_thread = threading.Thread(target=listen_to_signal, args=(state,))
    listen_thread.start()

    time.sleep(10)
    send_thread = threading.Thread(target=send_multicast)
    send_thread.start()
