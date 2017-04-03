DEBUG_NET = False

def tcp_server():
    print ("starting server server on TCP port 2323")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 2323))
    sock.listen(1)
    while True:
        try:
            conn, addr = sock.accept()
            data = conn.recv(1024)
            if data:
                message = data.decode("utf-8")
                if DEBUG_NET: print ("recieved message: " + message + " from " + str(addr[0]))
        except Exception as e:
            print (e)
            pass
