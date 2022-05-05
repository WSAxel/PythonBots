import socket
import random
import threading
import sys
import time
import argparse
# array with name of the bots
bots=["mia","pia","peter","john"]

# We need to see if correct argument parsers are given, --help gives these instructions for how to do it.
argParser = argparse.ArgumentParser(description='Connect to the chat room. Example: client.py localhost 4242 mia')

argParser.add_argument('ip', type=str, help='the client needs the ip address of the server, please submit. localhost')

argParser.add_argument('port', type=int, help='The server has a port you must connect to. like: 8080')

argParser.add_argument('name', type=str, help='The name of the bot you want to be in the conversation. Like: mia')

args = argParser.parse_args()
# ip address that is needed for connection
ip = args.ip
# WHat port to connect to
port = args.port
# Name of the client for the conversation
name = args.name

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Actively initiates a TCP server connection with ip address and port we gave
clientSocket.connect((ip, port))

# These are the standard list for good and not so good sodas for the bots
good_things=["cola", "solo", "sprite", "drpepper", "juice"]
bad_things=["pepsi", "fanta", "7up", "zingo", "water"]


# the bots and their functionality, they have answers for good sodas, bad sodas and others
def mia(word):
    if word in good_things:
        altAnswers = [
            "{}: Sure i would love some {}, that is one of my favorites".format(name,word),
            "{}: Yea im fine with {}. That could work, but i would rather want {} because of the orange colour".format(name,word,good_things[1])
        ]
        return random.choice(altAnswers)

    elif word in bad_things:
        altAnswers2 = [
            "{}: Yuck no! {} has a horrible taste! i'll only take {}".format(name,word,good_things[1]),
            "{}: No sorry, im not a fan of {}".format(name,word)
        ]
        return random.choice(altAnswers2)

    else:
        return "{}: I have never heard of that, i think i'll skip it".format(name)

def pia(word):
    # This bot has it's own list of products and doesn't agree with the standard good or bad list
    nonSodas = ["water", "juice", "coffe", "tea"]
    alternativeToSoda = random.choice(nonSodas)
    if word not in nonSodas:
        altAnswer3 = "{}: Sorry i don't drink soda, i want to be careful with my health and only drink {}".format(name, alternativeToSoda)
        return altAnswer3
    else:
        return "{}: Yea sure, i'll have {}. It sounds delicious".format(name, word)

def peter(word):
    # this bot seem more hungry then thirsty
    food = ["chips", "icecream", "peanuts"]
    if word in bad_things:
        altAnswers4 = [
            "{}: That doesn't sound very good, could i just get something to eat instead like {}?".format(name,random.choice(food))
        ]
        return altAnswers4
    else:
        return "{}: Yea whatever i'll take that".format(name)

def john(word):
    # this bot has different arrays for what it likes and hates
    johnFavorites = ["pepsi", "fanta", "7up"]
    johnHates = ["cola", "solo", "sprite"]
    if word in johnFavorites:
        altAnswers5 = [
            "{}: My taste is different then the other, i really like {}".format(name,word),
            "{}: Yes i enjoy a glass of {}, thank you!".format(name,word)
        ]
        return random.choice(altAnswers5)
    elif word in johnHates:
        altAnswers6 = [
            "{}: Ewww no! the others might enjoy it but i personally hate {}".format(name,word),
            "{}: I will have some {} only to be nice".format(name,word)
        ]
        return random.choice(altAnswers6)
    else:
        return "{}: Ok that sounds fine to me".format(name)

# when message comes from another bot/client the others ignore. Bots should be used with lowercase
def clientGetMessage():
    while True:
        msg = clientSocket.recv(1024).decode('utf-8')

        if msg == "name?":
            clientSocket.send(name.encode('utf-8'))

        else:
            if ":" in msg:

                msgSplit = msg.split(": ")

                if msgSplit[0] not in bots:
                    v=""
                    i=0
                    while i<len(bad_things):
                        if bad_things[i] in msg.lower():
                            v=bad_things[i]

                        if good_things[i] in msg.lower():
                            v=good_things[i]
                        i+=1

                    client_message=""
                    if name.lower() == "mia":
                        client_message=mia(v)

                    elif name.lower() == "pia":
                        client_message=pia(v)

                    elif name.lower() == "peter":
                        client_message=peter(v)

                    elif name.lower() == "john":
                        client_message=john(v)

                    print(msg)
                    clientSendMessage(client_message)

                else:
                    time.sleep(0.7)
                    print(msg)

            else:
                print(msg)

# message is sent
def clientSendMessage(msg):
    print(msg)
    clientSocket.send(msg.encode('utf-8'))

def clientForMessage():
    while True:
        try:
            msg = f'{name}: {input()}'
            split = msg.split(": ")
            if(split[1].isspace() or split[1] == ""):
                print("The sentence must have atleast some letters, please fill in more")
                continue
            else:
                time.sleep(0.4)
                print(msg)
                clientSocket.send(msg.encode('utf-8'))
        except:
            print("\nYou are not part of the conversation anymore\n")
            sys.exit()
            break


receive_thread = threading.Thread(target=clientGetMessage)
receive_thread.start()

# checking name given to program
if name not in bots:
    send_thread = threading.Thread(target=clientForMessage)
    send_thread.start()