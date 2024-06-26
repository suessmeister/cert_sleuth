# testing file
import socket

test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
test_socket.settimeout(5)
host = "www.utsystem.edu"
port = 443

try:
    test_socket.connect((host, port))
    print('worked!')
except:
    print ("no connection")


