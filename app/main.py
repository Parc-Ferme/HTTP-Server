import socket  # noqa: F401
import os

def parse_request (request):

    lines = request.split("\r\n")

    method, path, version = lines[0].split(" ")

    headers = {}
    body    = ''

    index   = 1

    while index < len(lines) and lines[index] != "":

        header       = lines[index]
        key, value   = header.split(":", 1)
        headers[key] = value
        index       += 1
    
    index += 1 
    body   = "\r\n".join(lines[index:])

    return method, path, body

def read_file (path):

    try:
        if os.path.exists(path):

            with open(path, 'rb') as file:

                return file.read(), 200
        else:

            return "File not found", 404
    except Exception as e:

        return f'{e}', 500
    
def handle_post (path, message):

    try:

        with open (path, 'w') as file:
            file.write(message)
            return 'File created successfully', 201
    except Exception as e:
        return f'{e}', 500


def send_response (client_socket, status_code, content):

    status_message = ""
    content_type   = "text/plain" 

    if status_code == 200:

        status_message = 'OK'

        if isinstance (content, bytes):
            content_type = "application/octet-stream"  
    elif status_code == 404:

        status_message = 'Not Found'
    elif status_code == 500:

        status_message = f'Internal Server Error :{content}'
    else:

        status_message = 'Unknown issue'

    headers = [
        f'HTTP/1.1 {status_code} {status_message}',
        f'Content-Type: {content_type}',
        f'Content-Length: {len (content)}',
        'Connection: close',
        '\r\n'
    ]

    response = '\r\n'.join (headers)

    response = response.encode() + content

    try:
        client_socket.sendall (response)
    except Exception as e:
        print (f"Error sending response: {e}")
    finally:
        client_socket.close ()

def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    print (f'Server is running on http://localhost:4221')

    while True:

        client_socket, client_address  = server_socket.accept()

        request = client_socket.recv(1024).decode()

        print (f'Request received:\n{request}')

        method, path, body = parse_request (request)
        
        path = path.removeprefix ("/")

        if method == 'GET':
        
            content, status_code = read_file (path)
            send_response (client_socket, status_code, content.encode() if isinstance(content, str) else content)

        elif method == 'POST':
            content, status_code = handle_post (path, body)
            send_response (client_socket, status_code, content.encode() if isinstance(content, str) else content)

        else:
            send_response (client_socket, 405, 'Method not found'.encode())


if __name__ == "__main__":
    main()
