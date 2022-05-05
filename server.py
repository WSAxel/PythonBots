import socket
import threading
import time
import argparse

# We need to see if correct argument parsers are given, --help gives these instruction.
argParser = argparse.ArgumentParser(description='In this stage you activate server to recieve client connections: server.py 8080')

argParser.add_argument('port', type=int, help='You must give a port for the server to run on, this is an integer: 8080')

args = argParser.parse_args()
# WHat port are we using that clients must connect to later?
port = args.port

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binds address to socket
serverSocket.bind(('localhost', port))
serverSocket.listen() # set up and start TCP listener
clientlist = []       # the different clients
clientNames = []   # the name of the clients


# from client to clientlist
def sendMessageToAll(message, client):
    for i in clientlist:
        if i is not client:
            i.send(message)


# for stopping all client connections and server give input "close"
def stopClient(client):
    while True:
        try:
            message = client.recv(1024)
            msg = message.decode().split(": ")

            if(msg[1] == "close"):
                time.sleep(1)
                print("clientlist will now be removed and stopped")
                for i in clientlist:
                    i.close()
                print("No more for clients")
                exit()

            else:
                time.sleep(0.7)
                sendMessageToAll(message, client)

        except:
            spot = clientlist.spot(client)
            clientlist.remove(client)
            client.close()
            botname = clientNames[spot]
            # closing and removing a bot
            sendMessageToAll(f'{botname} is gone and doesnt have a connection anymore'.encode('utf-8'), client)
            print(f'{botname} bot has left us')
            clientNames.remove(botname)
            break


# connecting the client to the conversation through server
def receiving():
    print('Waiting for bot connections')
    while True:
        client, address = serverSocket.accept()  # accept connection

        client.send('name?'.encode('utf-8'))
        botname = client.recv(1024).decode('utf-8')
        clientNames.append(botname)
        clientlist.append(client)
        print(f' The bot {botname} has decided to join us with address {str(address)}')
        sendMessageToAll(f'{botname} is now here'.encode('utf-8'), client)
        client.send('Welcome, you are part of the conversation now'.encode('utf-8'))

        thread = threading.Thread(target=stopClient, args=(client,))
        thread.start()

receiving()