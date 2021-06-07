import socket
from threading import Thread
from requests import get
import os

# Server global variables
HOST = ""
PORT = 5555
BUFFER = 1024
FORMAT = "utf-8"


def config():
    global server
    print("Server GroupChat: ON")
    print("HOST:", get('https://api.ipify.org').text)
    print("PORT:", PORT)
    print("Initializing the server...", end="")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(" DONE")
    print("Letting the server receive connections...", end="")
    server.bind((HOST, PORT))
    print(" DONE")
    print("Starting the server...", end="")
    server.listen()
    print(" DONE")


def handle_client(client_socket, address):
    try:
        while True:
            # The client always send the same kind of message:
            # [choice, text, username, password]
            # Only "choice" is the same in every case...
            # ... you have to send the "choice" (command) to execute
            # and maybe some parameters, like text, username and password.
            # If the client haven't to send text, username or password,
            # he just fills it with None
            received = eval(client_socket.recv(BUFFER).decode(FORMAT))
            choice = received[0]
            text = received[1]
            username = received[2]
            password = received[3]
            # print(choice, text, username, password)

            # The client wants the list of accounts
            if choice == "read_log_database":
                with open("log_db.txt", "r") as database:
                    accounts = database.readlines()
                # If there's almost one account
                if len(accounts) > 0:
                    client_socket.sendall(str(accounts).encode(FORMAT))
                # Otherwise send the flag variable "no_accounts"
                else:
                    client_socket.sendall(str(["no_accounts"]).encode(FORMAT))

            # The client wants to register a new account
            elif choice == "write_log_database":
                with open("log_db.txt", "a") as database:
                    string = f"{username} {password}\n"
                    database.write(string)

            elif choice == "read_room_database":
                rooms = os.listdir("text_db")
                if len(rooms) > 0:
                    client_socket.sendall(str(rooms).encode(FORMAT))
                else:
                    client_socket.sendall(str(["no_rooms"]).encode(FORMAT))

            elif choice == "write_room_database":
                os.mkdir(f"text_db/{text}")

            # The client wants to post a new text
            elif choice == "post_text_database":
                # Find the new filename (username + _ + num)
                num = 0
                while os.path.exists(f"text_db/{password}/{username}_{num}.txt"):
                    num += 1
                # Write the text into it
                file_name = f"text_db/{password}/{username}_{str(num)}.txt"
                with open(file_name, "w", encoding="utf8") as database:
                    database.write(text)

            # The client wants to read the sorted list of file messages
            elif choice == "read_sorted_text_database":
                # Just get the sorted by date list of file messages
                os.chdir(f"text_db/{text}")
                text_files = sorted(os.listdir(), key=os.path.getctime)
                os.chdir("../..")
                # If there's almost one file
                if len(text_files) > 0:
                    client_socket.sendall(str(text_files).encode(FORMAT))
                # Otherwise send the "no_text" flag variable
                else:
                    client_socket.sendall(str(["no_text"]).encode(FORMAT))

            # The client wants to read the content of a file message
            elif choice == "read_text_database":
                with open(f"text_db/{username}/{text}", "r") as txt:
                    string = "".join(elem for elem in txt.readlines())
                client_socket.sendall(str(string).encode(FORMAT))
    except:
        client_socket.close()


def main():
    config()

    while True:
        try:
            client_socket, address = server.accept()
            # Everytime a new client connect to the server, start a handle_client threading function
            Thread(target=handle_client, args=(client_socket, address)).start()
        except:
            break


if __name__ == '__main__':
    main()