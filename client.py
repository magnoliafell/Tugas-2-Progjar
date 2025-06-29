import socket
import logging

logging.basicConfig(level=logging.INFO)

def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 45000)
    logging.info(f"connecting to {server_address}")
    sock.connect(server_address)

    try:
        while True:
            user_input = input("TIME/QUIT: ").strip().upper()
            
            if user_input not in ("TIME", "QUIT"):
                    print("User input must be TIME or QUIT.\r\n")
            else:
                sock.sendall(user_input.encode())

                if user_input == "QUIT":
                    logging.info("Connection closed.")
                    break

                response = sock.recv(1024).decode()
                print(response)

    finally:
        logging.warning("closing")
        sock.close()
    return

if __name__ == "__main__":
  main()