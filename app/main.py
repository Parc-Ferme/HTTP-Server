import socket  # noqa: F401
import os

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address  = server_socket.accept() # wait for client

    request = client_socket.recv(1024).decode('utf-8')  # Reading the HTTP request
    print(f"Request received: {request}")


    http_response = 'HTTP/1.1 200 OK \r\n\r\n'

    client_socket.sendall(http_response.encode('utf-8'))


if __name__ == "__main__":
    main()
