import socket
import threading
import datetime

threads = []

art_text = []

HOST = "0.0.0.0"
PORT = 3333
ART_PATH = "./art"

def generateFilename(client):
    return "{}~{}.log".format(client.getpeername()[0].replace('.','_'), datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

def handler(client, address):
    filename = "logs/" + generateFilename(client)
    ip = client.getpeername()[0]
    print("[Info]: New Client: {}".format(ip))
    report = open(filename, "w+");
    welcometext = "welcome\n"
    client.send(welcometext.encode("utf-8"))
    report.write(welcometext);
    while True:
        try:
            data = client.recv(1024).decode("utf-8")
            report.write(data);
            if data:
                if "exit\r\n" in str(data):
                    #print("Client executed \"exit\" and disconnected")
                    client.close()
                    report.close()
                    break
                if "quit\r\n" in str(data):
                    #print("Client executed \"quit\" and disconnected")
                    client.close()
                    report.close()
                    break
                #print(data)
            else:
                #print("Client disconnected")
                client.close()
                report.close()
                break
        except:
            #print("Client disconnected")
            client.close()
            report.close()
            break
    print("[Info]: Lost Client: {}".format(ip))

# Start TCP Stream, with automatic resource deallocation (so that the resource can be reused)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind server to HOST and PORT
server.bind((HOST, PORT))
# Listen to up to 100 connections
server.listen(100)
while True:
    # While we have clients..
    client, address = server.accept()
    # ... make sure they don't go over 60 seconds of inactivity ...
    client.settimeout(60)
    # ... and start it in a new thread.
    thread = threading.Thread(target=handler, args = (client, address))
    thread.setDaemon(True)
    thread.start()
    threads.append(thread)
    count = 0
    for thread in threads:
        if thread.isAlive():
            count += 1
    print("[Info]: Number of clients: " + str(count))
