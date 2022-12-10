#Server Side Chat Room
import socket, threading
import pickle
from time import sleep
from _thread import *
import random
from Doodle_Ai import *

#Define constants to be used
HOST_IP = socket.gethostbyname(socket.gethostname())
print(HOST_IP)
HOST_PORT = 6969
ENCODER = 'utf-8'
BYTESIZE = 2048*50
players_full = 4
#Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()
end_round = False
client_socket_list = []
client_name_list = []
DOODLE_names = list(DOODLES.values())
winners = [] #name,predict_value,win or loss
lossers=[]
doodle_turn=""
def broadcast_message(message):
    '''Send a message to ALL clients connected to the server'''
    for client_socket in client_socket_list:
        client_socket.send(message)

def broadcast_info(message):
    global client_name_list
    for client_socket in client_socket_list:
        client_socket.send(message)
def broadcast_countdown(count,msg):
    global end_round
    while(count>=0):
        if(client_socket_list.__len__()==0 or end_round):
            count = 0
            end_round = False
        for client_socket in client_socket_list:
            client_socket.send(pickle.dumps({"time":count,"msg":msg}))
        count=count-1
        sleep(1)
        print(count)
def broadcast_ClientTurn():
    global doodle_turn
    random.shuffle(client_name_list)
    random.shuffle(DOODLE_names)
    doodle_turn = DOODLE_names[0]
    clients_turn = client_name_list
    print(clients_turn)
    for client_socket in client_socket_list:
            client_socket.send(pickle.dumps({"clients":clients_turn,"doodle":doodle_turn,"msg":"players_turn"}))
def recieve_message(client_socket):
    '''Recieve an incoming message from a specific client and forward the message to be broadcast'''
    while True:
        global client_name_list,doodle_turn,end_round
        try:
            #Get the name of the given client
            index = client_socket_list.index(client_socket)
            name = client_name_list[index]
            
            #Recieve message from the client
            message = client_socket.recv(BYTESIZE)
            try:
                message = pickle.loads(message)
            except Exception as ex:
                print(ex,"first")

            print(message)
            try:
                if(message['msg']=="start_Lobbycountdown"):
                    start_new_thread(broadcast_countdown,(5,"Lobbycountdown"))
                elif(message['msg']=="start_Gamecountdown"):
                    start_new_thread(broadcast_countdown,(40,"Gamecountdown"))
                elif(message['msg']=="clients_turn"):
                    start_new_thread(broadcast_ClientTurn,())
                elif(message['msg']=="who_is_the_winner"):
                    winners.extend(lossers)
                    winners_lossers_List = winners
                    print(winners_lossers_List)
                    message = pickle.dumps({"winners_lossers":winners_lossers_List,"msg":"broadcast_winnerslossers"})
                    broadcast_message(message)
                elif(message['msg']=="end_round"):
                    end_round = True
                elif(message['msg']=='recv_image'):
                    name = message['user']
                    file = open(f'server_images/{name}.png',"wb")
                    try:
                        image_chunk = message['image']
                        print("still loading")
                        file.write(image_chunk)
                    
                    except Exception as ex:
                        print(ex,'in recv img')
                    finally:
                        file.close()
                        file = open(f'server_images/{name}.png',"rb")
                        image_data = file.read(BYTESIZE)
                        print("sending image")
                        message = pickle.dumps({"user":name,"img": image_data,"msg":"broadcast_img"})
                        broadcast_message(message)  # type: ignore
                        image_data= file.read(BYTESIZE)
                        file.close()

                        val,pred =  detect_sketch(name,doodle_turn)  # type: ignore
                        if(pred == doodle_turn):
                            winners.append({"name":name,"pred":pred,"val":val,"status":"winner"})
                            if(winners.__len__()>1):
                                for winner in winners:
                                    if(winner['val']>val):
                                        lossers.append({"name":name,"pred":pred,"val":val,"status":"loser"})
                                        winners.pop()
                                    elif(winner['val']<val):
                                        lossers.append(winner)
                                        del winners[winners.index(winner)]
                        else:
                            lossers.append({"name":name,"pred":pred,"val":val,"status":"loser"})
                elif(message['msg']=='chat'):
                    message = pickle.dumps({"user":name,"message": message['message'],"msg":"chat"})
                    broadcast_message(message)  # type: ignore

                else:
                    start_new_thread(broadcast_message,(pickle.dumps(message),))

            except:
                    start_new_thread(broadcast_message,(message,))
                
        except Exception as ex:
            print(ex,)
            #Find the index of the client socket in our list
            index = client_socket_list.index(client_socket)
            name = client_name_list[index]

            #Remove the client socket and name from lists
            client_socket_list.remove(client_socket)
            client_name_list.remove(name)
            winners.clear()
            lossers.clear()

            #Close the client socket

            #Broadcast that the client has left the chat.
            print(client_name_list)
            start_new_thread(broadcast_info,(pickle.dumps({"players": client_name_list,"msg": "players_name"}),))
            start_new_thread(broadcast_message,(pickle.dumps({"name":name,"msg": "has left the chat!"}),))
            client_socket.close()
            break



def connect_client():
    '''Connect an incoming client to the server'''
    
    global client_name_list
    while True:
        try:
            #Accept any incoming client connection
            client_socket, client_address = server_socket.accept()
            if(len(client_name_list)<=players_full-1):
                print(f"Connected with {client_address}...")
                #Send a NAME flag to prompt the client for their name
                client_socket.send("NAME".encode(ENCODER))
                client_name = pickle.loads(client_socket.recv(BYTESIZE))['msg']
                print(client_name)
                #Add new client socket and client name to appropriate lists
                client_socket_list.append(client_socket)
                client_name_list.append(client_name)
                #Update the server, individual client, and ALL clients
                print(f"Name of new client is {client_name}\n") #server
                client_socket.send(pickle.dumps({"name":client_name,"msg": "you have connected to the server!"})) #Individual client
                sleep(0.7)
                start_new_thread(broadcast_message,(pickle.dumps({"name": client_name,"msg": "has joined the chat!"}),))
                sleep(0.7)
                start_new_thread(broadcast_info,(pickle.dumps({"players": client_name_list,"msg": "players_name"}),))
                #Now that a new client has connected, start a thread
                recieve_thread = threading.Thread(target=recieve_message, args=(client_socket,))
                recieve_thread.start()
            else:
                print("server is full")
                client_socket.send(pickle.dumps({"server": "server","msg": "server is full"}))
        except Exception as ex:
            print("connect_function",ex)

#Start the server
print("Server is listening for incoming connections...\n")
connect_client()


