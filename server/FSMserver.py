import socket
import os

port = 9999


def handler(client_sock):
    """
    Handles commands coming from client.
    :param client_sock: Client socket
    :return: None
    """

    # Writing mode toggle.
    write_mode = False
    # Path of dir for writing mode
    write_path = ""
    while True:
        # Establishes a connection
        raw_from_client = client_sock.recv(4096)
        # Un-split version of input from client
        msg_unsplit = raw_from_client.decode()
        # List of input arguments from client
        msg = msg_unsplit.split()
        # Prints out the command list server side
        print(msg)

        if write_mode:
            # If writing mode is engaged, try and open the file and write the message.
            try:
                with open(write_path, "a") as file:
                    file.write(f"{msg_unsplit}")
                    client_sock.send(f"{write_path}: saved".encode())
                    write_mode = False
            except FileNotFoundError:
                # Sends error to client
                client_sock.send(f"{write_path}: Directory does not exist".encode())
                # Disengages writing mode
                write_mode = False
        else:

            if msg[0] == "quit":
                # If user attempts to quit the program
                break

            elif msg[0] == "pwd":
                # Print current working directory
                client_sock.send(os.getcwd().encode())

            elif msg[0] == "ls":
                # List files in directory
                files = os.listdir()
                print(files)
                # Creates a string version of the OS dir list
                if (len(files) > 0):
                    fileString = ""
                    for elm in files:
                        fileString += elm + " "
                    client_sock.send(fileString.encode())
                else:
                    # Handles empty dir
                    client_sock.send("  ".encode())

            elif msg[0] == "mkdir":
                # Creates a new directory
                try:
                    os.mkdir(str(msg[1]))
                    client_sock.send(f"{msg[1]}: directory created".encode())
                # error handling
                except IndexError:
                    client_sock.send("Please enter a name for the directory".encode())
                except FileExistsError as err:
                    client_sock.send(str(err).encode())


            elif msg[0] == "cat":
                read_path = msg[1]
                try:
                    # Opens the file, Compounds it to a string, Sends it to the client.
                    content = ""
                    with open(str(read_path), "r") as file:
                        for line in file:
                            content += f"{line.strip()}\n"
                        client_sock.send(content.encode())
                except FileNotFoundError:
                    # Sends file not found error to user
                    client_sock.send("File not found".encode())

            elif msg[0] == "write":
                # Writes to a new file (dumpster fire)
                write_path = msg[1]
                try:
                    # If path is valid
                    with open(write_path, "a"):
                        # Enter writing mode
                        write_mode = True
                        client_sock.send("Entering Writing mode".encode())
                except FileNotFoundError:
                    # handles file not found.
                    client_sock.send(f"{write_path}: Directory does not exist".encode())
                    # Leaves writing mode
                    write_mode = False

            elif msg[0] == "cd":
                # Directory change
                try:
                    os.chdir(str(msg[1]))
                    client_sock.send(" ".encode())
                except FileNotFoundError:
                    # Invalid Dir
                    client_sock.send(f"{msg[1]}: Directory not found".encode())
            else:
                # Default case, send invalid command msg
                client_sock.send("Please Enter a valid command".encode())
    client_sock.close()


def main():
    """
    Establishes a connection
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Address family and TCP specification
    server_socket.bind(('', port))
    server_socket.listen()  # Listening for a client connection.
    print("Server is listening.")
    (client_sock, addr) = server_socket.accept()
    handler(client_sock)
    client_sock.close()


main()
