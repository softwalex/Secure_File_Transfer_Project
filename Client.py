import socket
import os

# Define the server's host and port
SERVER_HOST = '127.0.0.1'  # Change this to the server's IP address if it's on a different machine
SERVER_PORT = 12345      # Change this to the server's port number

BUFFER_SIZE = 4096

def download_file(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        
        # Send the DOWNLOAD command
        client_socket.send(f"DOWNLOAD {filename}".encode())

        # Receive the file size from the server
        file_size = int(client_socket.recv(BUFFER_SIZE).decode())

        if file_size == -1:
            print("File not found on the server.")
            return

        # Send acknowledgment
        client_socket.send(b"READY")

        # Receive the file contents from the server and save it
        with open(filename, 'wb') as file:
            received_data = client_socket.recv(BUFFER_SIZE)
            total_received = len(received_data)
            file.write(received_data)
            while total_received < file_size:
                received_data = client_socket.recv(BUFFER_SIZE)
                total_received += len(received_data)
                file.write(received_data)

        print(f"File '{filename}' downloaded successfully.")

def upload_file(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        
        # Send the UPLOAD command
        client_socket.send(f"UPLOAD {filename}".encode())

        # Receive acknowledgment from the server
        acknowledgment = client_socket.recv(BUFFER_SIZE).decode()

        if acknowledgment != "READY":
            print("Server is not ready to receive the file.")
            return

        # Send the file contents to the server
        with open(filename, 'rb') as file:
            data = file.read(BUFFER_SIZE)
            while data:
                client_socket.send(data)
                data = file.read(BUFFER_SIZE)

        print(f"File '{filename}' uploaded successfully.")

#Consle program for the user        
def main():
    #Choose upload or download
    print("To upload enter u")
    print("To download enter d")
    method_input = input("enter here: ")
    
    #upload file to server
    if(method_input=='u'):
       file_to_upload = input("Enter the file path for upload:")
       upload_file(file_to_upload)

    #Download file from the server   
    elif(method_input=='d'):
        file_to_download = input("Enter the file name to download:")
        download_file(file_to_download)
        
    else:
        print("input eror...")
        
if __name__ == '__main__':
    main()