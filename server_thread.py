from socket import *
import socket
import threading
import logging
import time
import sys
from datetime import datetime

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        logging.warning(f"Client {self.address} connected.")
        
        while True:
            data = self.connection.recv(32)
            try:
                if data:
                    message = data.decode('utf-8').strip()
                    logging.warning(f"Request from {self.address}: {message}")
                
                    if message.upper() == "QUIT":
                        logging.warning(f"Client {self.address} requested to stop the connection.")
                        break
                    elif message.upper().startswith("TIME"):
                        current_time = datetime.now()
                        time_string = current_time.strftime("%H:%M:%S")
                        response = f"JAM {time_string}\r\n"
                        self.connection.sendall(response.encode('utf-8'))
                        logging.warning(f"Sending time to {self.address}: {time_string}")
                else:
                    error_response = "ERROR: Request muest start with 'TIME'\r\n"
                    self.connection.sendall(error_response.encode('utf-8'))
                    logging.warning(f"Not a valid request from {self.address}: {message}")
                    
            except Exception as e:
                logging.error(f"Error when processing the client {self.address}: {e}")
                break
        
        self.connection.close()
        logging.warning(f"Connection with {self.address} closed.")

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.my_socket.bind(('0.0.0.0', 45000))
            self.my_socket.listen(5) 
            logging.warning("Time Server started in port 45000")
            logging.warning("Waiting connection from client...")
            
            while True:
                self.connection, self.client_address = self.my_socket.accept()
                logging.warning(f"connection from {self.client_address}")
                
                clt = ProcessTheClient(self.connection, self.client_address)
                clt.start()
                self.the_clients.append(clt)
       
        except KeyboardInterrupt:
            logging.warning("Server stopped by user.")
        except Exception as e:
            logging.error(f"Error in server: {e}")
        finally:
            self.my_socket.close()

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()