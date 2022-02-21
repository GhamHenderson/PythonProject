import socket
import threading
import wsgiref.simple_server

from time import gmtime, strftime
import time

HOST = '127.0.0.1'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))


listofsongs = list()

# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = ""


# custom say hello command
def sayHello():
    print("----> The hello function was called")


# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a 
# command it will then need to extract the command.
def parseInput(data, s):
    print("parsing...")
    print(str(data))

    # Checking for commands 
    if "<hello>" in data:
        print("hello command run.")
    elif "<addsong" in str(data):
        print("adding a song")
        parts = str(data).split('-')
        func = parts[0]
        print(func[3:])
        print(parts[1])
        hostAddress = parts[2]
        print(hostAddress[0:-3])
        listofsongs.append(parts[1])

        f = open('c0.mp3', 'wb')
        partoffile = s.recv(1000)

        while partoffile:
            f.write(partoffile)
            partoffile = s.recv(1000)
        f.close()
# we a new thread is started from an incoming connection
# the manageConnection funnction is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.

def manageConnection(conn, addr):
    global buffer
    print('Connected by', addr)

    data = conn.recv(1024)

    parseInput(str(data), conn)  # Calling the parser, passing the connection

    print("rec:" + str(data))
    buffer += str(data)

    # conn.send(str(buffer))

    conn.close()


while 1:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args=(conn, addr))

    t.start()
