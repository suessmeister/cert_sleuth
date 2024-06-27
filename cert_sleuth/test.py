# testing file with random features to be implemented!
# do not mind this file.
# this is only for minor testing characteristics.

import socket
import time



def socket_test():
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_socket.settimeout(5)
    host = "www.utsystem.edu"
    port = 443


    try:
        test_socket.connect((host, port))
        print('worked!')
    except:
        print ("no connection")


def counter_test():
    for i in range(50000):
        print('\r', str(i), end='', flush=True)
        time.sleep(0.2)

counter_test()

