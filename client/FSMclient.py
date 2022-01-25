import socket
import os

host = 'localhost'
port = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creates a socket to connect to
client_socket.connect((host, port))  # established a connection
write_mode = False  # Enables writing mode


def write():
    """
    Writes a message that will be sent to the server
    :return: String containing message to be written to a file
    """
    final_str = ""
    while True:
        # Write to a string until no input is given.
        user_input = input("> ")
        if user_input == "":
            print(f"sending: {final_str}")
            # Returns final message
            return final_str
        else:
            final_str += f"{user_input}\n"


while True:
    if write_mode:
        # If we are in write mode, Send the encoded message
        client_socket.send(write().encode())
        # Leave write mode
        write_mode = False
        # Get the server response and print it
        msg_from_server = client_socket.recv(4096)
        print(msg_from_server.decode())
        # Skip to next iteration
        continue

    user_input = input("Enter command: ")  # gets user input

    if user_input == "":
        # Invalid command
        print("please enter a command")
        continue

    elif user_input == "quit":
        # Quits the program.
        client_socket.send("quit".encode())
        break

    elif user_input.split()[0] == "write":
        # Lets the server know to go into writing mode
        client_socket.send(user_input.encode())
        try:
            # Checks to see if file directory exists at location.
            with open(user_input.split()[1], 'a') as f:
                pass
            # Enters write mode if it does
            write_mode = True
        except FileNotFoundError:
            # Passes if the file location does not exist
            pass

    else:
        # Sends command to the server if it is valid
        client_socket.send(user_input.encode())
    msg_from_server = client_socket.recv(4096)  # receiving a message from the server
    if not msg_from_server.decode() == " ":
        # Prints blank space when it is received.
        print(msg_from_server.decode())
client_socket.close()
