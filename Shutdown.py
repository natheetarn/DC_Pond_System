def shutdown_menu():
    while True:
        print("press Q to quit")
        # print("press B to go back to main menu")
        choice = input("Please enter your choice: ")

        if choice == "Q" or choice == "q":
            print("Quitting...")
            break  # shutdown the system
        # elif chioce == "B" | choice == "b":
        #     print("Going back to main menu...")
        #     break


if __name__ == "__main__":
    shutdown_menu()
