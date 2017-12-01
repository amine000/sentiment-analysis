# CODE ADAPTED FROM http://www.bogotobogo.com/python/files/chat/chat_client.py

import sys, socket, select, random
from tkinter import *
import threading, time
import atexit
import errno
import GIFSearch
import re

inputPort = 54321
global_sock = None 
inputReady = False
inputClient = None
fuck = False
s = None
chatBox = None
st = None
quitProgram = False
root = None
suggestion = None


class myThread (threading.Thread):
    def __init__(self, proc):
        threading.Thread.__init__(self)
        self.process = proc
    def run(self):
        print ("Starting " + self.process)
        if (self.process == "GUI") :
            startGUI()
        elif (self.process == "inputSock") :
            inputSocket()
        else :
            chat_client()


def exitFunc():
    inputClient.close()
    global_sock.close()
    s.send(None)
    s.close()
    print("closed everything")

# Windows doesn't support select on sys.stdin, so use a socket for input messages
def inputSocket():
    global inputPort
    global global_sock
    global inputReady

    port = random.randrange(1000, 9999)
    while (port == 9009):
        port = random.randrange(1000, 9999)
    inputPort = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', port))
    sock.listen(5)
    print("input sock listening at " , port)
    myThread("GUI").start()
    while (not quitProgram):
        try:
            if (not fuck):
                global_sock, addr = sock.accept()
                print("input sock connected to ", addr)
                inputReady = True
                sys.exit()
        except KeyboardInterrupt:
            print("lols")
            sys.exit()
    print("broke out here")

def chat_client():
    global s
    global suggestion
    while (not inputReady):
        pass

    print("yee")
    if(len(sys.argv) < 3) :
        print ('Usage : python chat_client.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print ('Unable to connect')
        sys.exit()
     
    chatBox.insert(END, 'Connected to remote host. You can start sending messages now!\n')

    while (not quitProgram):
        socket_list = [global_sock, s]
        # Get the list sockets which are readable
        try:
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [], 0)
            for sock in read_sockets:            
                if sock == s:
                    # incoming message from remote server, s
                    data = sock.recv(4096)
                    if not data :
                        print ('\nDisconnected from chat server')
                        sys.exit()
                    else :
                        #print data
                        message = data.decode("utf-8")
                        chatBox.config(state=NORMAL)
                        chatBox.insert(END, message) 
                        chatBox.config(state=DISABLED)  

                        # Remove current suggestion and replace
                        if (suggestion is not None):
                            suggestion.destroy()
                        if (re.match('User', message) == None):
                            suggestion = GIFSearch.search(message, 'lit.gif', root) 
                            suggestion.grid(row=0, column = 2, rowspan=3)
                else :
                    # user entered a message
                    msg = sock.recv(4096)
                    s.send(msg)
                    st.set("Enter message here")
        except KeyboardInterrupt:
            print("HAHAHAHAHAHAHA")
            sys.exit()
    print ("quit")

def sendMsg(searchBox):
    msg = searchBox.get()
    inputClient.send(str.encode(msg))

def close(root):
    global quitProgram
    quitProgram = True
    root.destroy()
    print ("Root destroyed")

def startGUI():
    global inputReady
    global inputClient
    global chatBox
    global st
    global root 

    inputClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Attempting to connect to input port ", inputPort)
    fuck = True
    try :
        inputClient.connect(('localhost', inputPort))
    except:
        print("fucked up")
    root = Tk()

    S = Scrollbar(root)
    chatBox = Text(root, height=30, width=50)
    S.grid(row=0, column=1)
    chatBox.grid(row=0, column=0)
    S.config(command=chatBox.yview)
    chatBox.config(yscrollcommand=S.set)

    st = StringVar()
    st.set("Enter message here")
    searchBox = Entry(root, textvariable=st, width=45)
    searchBox.grid(row=1, column=0)
    Button(root, text='send', command= lambda: sendMsg(searchBox)).grid(row=1, column=1)
    myThread("client").start()

    Button(root, text='close', command= lambda: close(root)).grid(row=2)
    root.mainloop()
    sys.exit()
    print("broke out here?")

if __name__ == "__main__":
    try:
        atexit.register(exitFunc)
        inputSocket()
        app = myThread("inputSock")
        app.start()
        print("hi")
    except SystemExit:
        print("teamm")

