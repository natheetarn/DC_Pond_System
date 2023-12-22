import time
import Shutdown
import Fish

class Startup:
    def __init__(self, pond_id):
        self.pond_id = pond_id
        self.shutdown = Shutdown
        self.fish = Fish
        self.choices = {
            1: self.fish.addFish(),
            2: self.fish.moveFish(),
            3: self.shutdown.shutdown_menu()
        }

    def startUp(self):
        print("Pond ID:", self.pond_id)
        print("Starting the server")

        # TODO: implement something else that doesn't use threading
        # server_thread = threading.Thread(target=MulticastServer.run_server, args=(12345,))
        # server_thread.start()

        while True:
            try:
                user_input = int(input("1: Add fish\n2: Move fish\n3: Shutdown\nPlease enter your choice: "))
                
                if user_input in self.choices:
                    self.choices[user_input]()
                else:
                    print("Invalid input")

            except ValueError:
                print("Invalid input. Please enter a number.")

            time.sleep(0.5)

if __name__ == "__main__":
    startup_instance = Startup(1)  # Replace 1 with the desired pond ID
    startup_instance.startUp()
