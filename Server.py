import socket
import os

#Server IP address and PORT
HOST = '127.0.0.1'
PORT = 12345

#Folder name and BUFFER size
UPLOAD_FOLFER = 'SERVER_FOLDER'
BUFFER_SIZE = 4096

def handle_client(client_socket):
    # Receive the command from the client
    command = client_socket.recv(BUFFER_SIZE).decode()

    # Split the command into action and filename
    action, filename = command.split()

    if action == "DOWNLOAD":
        # Check if the file exists
        file_path = os.path.join(UPLOAD_FOLFER, filename)
        if os.path.exists(file_path):
            # Send the file size to the client
            client_socket.send(str(os.path.getsize(file_path)).encode())
            client_socket.recv(BUFFER_SIZE)  # Wait for acknowledgment

            # Send the file contents to the client
            with open(file_path, 'rb') as file:
                data = file.read(BUFFER_SIZE)
                while data:
                    client_socket.send(data)
                    data = file.read(BUFFER_SIZE)
        else:
            client_socket.send(b"FILE_NOT_FOUND")

    elif action == "UPLOAD":

        # Send acknowledgment
        client_socket.send(b"READY")

        # Receive the file contents from the client and save it
        file_path = os.path.join(UPLOAD_FOLFER, filename)
        with open(file_path, 'wb') as file:
            received_data = client_socket.recv(BUFFER_SIZE)
            file.write(received_data)
                                
    client_socket.close()
    
def main():
    if not os.path.exists(UPLOAD_FOLFER):
        os.makedirs(UPLOAD_FOLFER)

    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the address and port
        server_socket.bind((HOST, PORT))

        # Listen for incoming connections
        server_socket.listen()

        print("Server is listening on port", PORT)

        while True:
            # Accept connections from client
            connection, address = server_socket.accept()
            print("Connected to", address)

            # Handle the client connection in a separate thread
            handle_client(connection)
            break
            

if __name__ == '__main__':
    main()