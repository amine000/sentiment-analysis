# CODE ADAPTED FROM http://www.bogotobogo.com/python/files/chat/chat_client.py

import sys, socket, select, random
from tkinter import *
from nltk.corpus import brown
import nltk
import threading, time
import atexit
import errno
import GIFSearch
import re
import os
from PIL import Image, ImageTk

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
suggestions = []
gifs_used = []


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
    s.close()
    #print("closed everything")
    sys.exit()

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

def is_gif(message):
    return (re.search('\[GIF\]', message) != None)

def new_temp_file():
    global gifs_used
    filename = str(random.randint(0,99999)) + 'temp.gif'
    #print(filename)
    gifs_used.append(filename)
    return filename

def chat_client():
    global s
    global suggestions
    global root
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

    text = brown.words(categories=['news', 'editorial','humor','reviews','fiction','lore'])
    fdist = nltk.FreqDist(w.lower() for w in text)

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
                        if (is_gif(message)):
                            #print('hello')
                            parsed_message = re.split('\[GIF\]', message)
                            gifUrl = parsed_message[1]
                            i = parsed_message[2]
                            gif = GIFSearch.create_GIF_label(gifUrl, new_temp_file(), root, i)
                            chatBox.config(state=NORMAL)
                            chatBox.insert(END, parsed_message[0]) 
                            chatBox.window_create(END, window=gif)
                            chatBox.insert(END, '\n')
                            chatBox.config(state=DISABLED) 
                            if (len(suggestions) != 0):
                                for x in suggestions:
                                    x.destroy()
                                suggestions = []
                            gif.config(cursor='arrow')
                        else:
                            chatBox.config(state=NORMAL)
                            chatBox.insert(END, message) 
                            chatBox.config(state=DISABLED)  

                            # Remove current suggestion and replace
                            if (len(suggestions) != 0):
                                for x in suggestions:
                                    x.destroy()
                            # If not user entered message or your own message, suggest
                            if ((re.match('User', message) == None) and (re.search('\[ Me \]', message) == None)):
                                suggestions = GIFSearch.search(message, 'lit.gif', root, fdist) 
                                for i, suggestion in enumerate(suggestions):
                                    suggestion.grid(row=1 + i, column = 2, padx=(1,7))
                                    suggestion.bind("<Button-1>", lambda e, gif = suggestion: sendGIF(gif))
                else :
                    # user entered a message
                    msg = sock.recv(4096)
                    s.send(msg)
                    st.set("Enter message here")
        except KeyboardInterrupt:
            print("HAHAHAHAHAHAHA")
            sys.exit()
    #print ("quit naturally")
    close(root)
    for gif in gifs_used:
        print('removing ' + gif)
        os.remove(gif)

def sendMsg(searchBox):
    msg = searchBox.get()
    inputClient.send(str.encode(msg))

def sendGIF(GIFLabel):
    inputClient.send(str.encode('[GIF]' + GIFLabel.url + '[GIF]' + str(GIFLabel.result_index)))

def close(root):
    global quitProgram
    quitProgram = True
    root.destroy()
    #print ("Root destroyed")
    return (exitFunc())

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
    root.configure(background="#e8eff4")

    title = Label(root, text="GIF SUGGESTER CHAT ROOM", bg="#e8eff4", fg='#13243f', font=('Courier',24), 
        borderwidth=10, relief=RIDGE, padx=10, pady=5).grid(row=0, columnspan=2, pady=(10,20))

    scroll = Scrollbar(root)
    chatBox = Text(root, height=25, width=60, font=('Arial',12), spacing1=5, padx=5)
    scroll.grid(sticky=N+S,row=1, column=1, rowspan=3, pady=10, padx=5)
    chatBox.grid(row=1, column=0, rowspan=3, pady=10, padx=10)
    scroll.config(command=chatBox.yview)
    chatBox.config(yscrollcommand=scroll.set)

    st = StringVar()
    st.set("Enter message here")
    searchBox = Entry(root, textvariable=st, width=45, font=('Arial',12))
    searchBox.grid(row=4, column=0, pady=10, padx=10, sticky=W+E)
    searchBox.bind("<Return>", lambda e, x = searchBox: sendMsg(x))
    Button(root, text='>', font=('Arial',14) , command= lambda: sendMsg(searchBox)).grid(row=4, column=1, pady=10, padx=5)
    myThread("client").start()

    #Button(root, text='close', command= lambda: close(root)).grid(row=4)
    root.mainloop()
    sys.exit()

if __name__ == "__main__":
    try:
        atexit.register(exitFunc)
        inputSocket()
        app = myThread("inputSock")
        app.start()
        print("hi")
    except SystemExit:
        print("teamm")
        for gif in gifs_used:
            os.remove(gif)

