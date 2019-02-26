import socket

IP_ADDRESS = "127.0.0.1"
PORT_NO = 6789
PACKET_SIZE = 1024
TIMEOUT = 30


def udp(stopwait):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind((IP_ADDRESS, PORT_NO))
    sock.settimeout(TIMEOUT)

    nrmsg = 0
    nrbytes = 0
    try:
        while True:
            data, addr = sock.recvfrom(PACKET_SIZE)
            # print(addr)
            print("Received: ", len(data), "bytes")
            if stopwait:
                sock.sendto(b'ACK', addr)
            nrmsg += 1
            nrbytes += len(data)
    except socket.timeout:
        print('[UDP] No message for a while, end of session')
        print('[UDP] Got %s messages, %s bytes' % (nrmsg, nrbytes))
    finally:
        sock.close()


def tcp(stopwait):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP_ADDRESS, PORT_NO))
    sock.settimeout(TIMEOUT)
    nrmsg = 0
    nrbytes = 0
    try:
        sock.listen(1)
        while True:
            connection, client_address = sock.accept()
            try:
                while True:
                    data = connection.recv(PACKET_SIZE)
                    if data:
                        if stopwait:
                            connection.send(b'ACK')
                        print("Received: ", len(data), "bytes")
                        nrmsg += 1
                        nrbytes += len(data)
                    else:
                        break

            finally:
                connection.close()
    except socket.timeout:
        print('[TCP] No message for a while, end of session')
        print('[TCP] Got %s messages, %s bytes' % (nrmsg, nrbytes))
    finally:
        sock.close()


udp(False)
# udp(True)
# tcp(False)
# tcp(True)
