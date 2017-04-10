import socket
import threading
import datetime
import os
import random

threads = []

art_text = []

HOST = "0.0.0.0"
PORT = 3333

try:
    os.mkdir("art")
except Exception:#FileExistsError:
    pass
try:
    os.mkdir("logs")
except Exception:#FileExistsError:
    pass

def generateFilename(client):
    return "{}~{}.log".format(client.getpeername()[0].replace('.','_'), datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

def handler(client, address):
    try:
        filename = "logs/" + generateFilename(client)
        ip = client.getpeername()[0]
        print("[Info]: New Client: {}".format(ip))
        report = open(filename, "w+")
        ida = random.random() * numart
        welcometext = "{}\nLogin:\n".format(art_text[int(ida)])
        client.send(welcometext.encode("utf-8"))
        report.write(welcometext);
        client.settimeout(2)
        more = client.recv(64)
        report.write(str(more))
        client.send("Password: ".encode("utf-8"))
        report.write("Password: ")
    except Exception as e:
        print("Error in initial spot: {}".format(e))
    while True:
        try:
            client.settimeout(60)
            data = client.recv(1024)
            try:
                data = data.decode("utf-8")
            except Exception as e:
                data = str(data)
                print("[Warning]: Decoding Error: {}".format(e))
                pass
            report.write(str(data));
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
        except Exception as e:
            print("[Error]: {}".format(e))
            client.close()
            report.close()
            break
    print("[Info]: Lost Client: {}".format(ip))

arts = os.listdir("art")
for splashfile in arts:
    splashfilename = "art/" + splashfile
    spfile = open(splashfilename)
    splash = ""
    for line in spfile:
        splash = splash + line
    art_text.append(splash)
numart = len(art_text)
# Start TCP Stream, with automatic resource deallocation (so that the resource can be reused)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind server to HOST and PORT
server.bind((HOST, PORT))
# Listen to up to 100 connections
server.listen(100)
print("Server started on TCP port {}.".format(PORT))
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
