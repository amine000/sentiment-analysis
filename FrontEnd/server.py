# CODE ADAPTED FROM http://www.bogotobogo.com/python/files/chat/chat_server.py
 
import sys, socket, select

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009
CLIENT_NAMES = {}


def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                CLIENT_NAMES[addr[1]] = len(SOCKET_LIST) - 1
                print "Client (%s, %s) connected; assigned user number %d" % (addr[0], addr[1], CLIENT_NAMES[addr[1]])
                 
                broadcast(server_socket, sockfd, "User %d entered our chatting room\n" % CLIENT_NAMES[addr[1]], "")
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:

                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    name = sock.getpeername()
                    if data:
                    	print "Client (%s, %s) / User %d sent a message" % (name[0], name[1], CLIENT_NAMES[name[1]])
                        message = "\r" + '[ User ' + str(CLIENT_NAMES[name[1]]) + ' ]   ' + data + '\n'
                        self_message = "\r" + '[ Me ]   ' + data + '\n'
                        # there is something in the socket
                        broadcast(server_socket, sock, message, self_message)  
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) / User %d is offline\n" % (name[0], name[1], CLIENT_NAMES[name[1]]), "") 

                # exception 
                except:
                    print("wellll")
                    broadcast(server_socket, sock, "Client (%s, %s) / User %d is offline\n" % (name[0], name[1], CLIENT_NAMES[name[1]]), "") 
                    sys.exit()

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message, self_message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
        elif socket == sock and socket != server_socket:
            try :
                socket.send(self_message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)            
 
if __name__ == "__main__":

    sys.exit(chat_server())


         
