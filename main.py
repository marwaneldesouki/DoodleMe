from operator import truediv
import pickle
import socket
import threading
from _thread import *
from PIL import Image
import tkinter as tk
from xml.etree.ElementTree import TreeBuilder
from time import sleep

DEST_IP = socket.gethostbyname(socket.gethostname())
print(DEST_IP)
DEST_PORT = 6969
ENCODER = 'utf-8'
BYTESIZE = 2048*50
foreground_colour = 'white'
current_colour = 'black'
clients=[]
player_turn=""
doodle_turn=""
winners_lossers_List = []
players_notPlayed=[]
players_Played=[]
var = ""
root_listbox=""
wait_players = False
Lobby_countdown = 0
Game_countdown =  0

players_full = 4
canvas =""
#Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((DEST_IP, DEST_PORT))





def paint(canvas,x1y1,x2y2, selected_colour):
    '''Draws a line following the user mouse cursor'''
    try:
        x1, y1 = x1y1[0],x1y1[1]
        x2, y2 = x2y2[0],x2y2[1]
        width=8
        if(selected_colour=="#e3e5e8"):#for eraser
            width = 60
        canvas.create_line(x1, y1, x2, y2, fill=selected_colour, width=width)  # type: ignore
    except Exception as ex:
        print(ex,"error in paint")

def change_colour(selected_colour):
    '''Changes the colour used to draw'''
    global current_colour
    current_colour = selected_colour

def send_chat(chatbox):
    '''send messages to chat'''
    inp = chatbox.get(1.0, "end-1c")
    chatbox.delete(1.0, "end-1c")
    message = pickle.dumps({"message":inp,"msg":"chat"})
    client_socket.send(message)
def end_Round():
    '''endround'''
    message = pickle.dumps({"msg":"end_round"})
    client_socket.send(message)

def clear(canvas):
    '''Clear all drawn objects from the screen'''
    canvas.delete('all')


def send_message(event,color):
    '''Send a message to the server to be broadcast'''
    try:
        x1, y1 = event.x-1, event.y-1
        x2, y2 = (event.x+1), (event.y+1)
        message = pickle.dumps({"name":name,"x1y1":[x1,y1],"x2y2":[x2,y2],"drawing_color":color,"msg":""})
        client_socket.send(message)
    except:
        message = pickle.dumps({"name":name,"x1y1":[],"x2y2":[],"drawing_color":"","msg":"clear"})
        client_socket.send(message)


def save_as_png(canvas,fileName):
    # save postscipt image 
    canvas.postscript(file = f'images/{fileName}.eps')
    img =  Image.open(f'images/{fileName}.eps') 
    img.save(f'images/{fileName}.png')


def recieve_message():
    '''Recieve an incoming message from the server'''
    global clients,Lobby_countdown,canvas,player_turn,players_notPlayed,Game_countdown,var,doodle_turn,winners_lossers_List,root_listbox
    global chat_var
    while True:
        try:
            #Recieve an incoming message from the server.
            message = client_socket.recv(BYTESIZE)
            message = pickle.loads(message)
            #Check for the name flag, else show the message
            if len(message)==2 and message['msg']=="players_name":
                clients = message['players']
            elif len(message)==2 and message['msg']=="Lobbycountdown":
                Lobby_countdown = message['time']
            elif len(message)==2 and message['msg']=="Gamecountdown":
                Game_countdown = message['time']
                var.set(str(Game_countdown))  # type: ignore
                print(Game_countdown)
            elif len(message)==2 and message['msg']=="broadcast_winnerslossers":
                winners_lossers_List=message["winners_lossers"]
                print(winners_lossers_List)
            elif len(message)==3 and message['msg']=="players_turn":
                print(message['clients'])
                player_turn =message['clients'][0]
                print(player_turn,"will play")
                players_notPlayed = message['clients'][1:]
                print(players_notPlayed,"Not played")
                doodle_turn = message['doodle']
            elif len(message)==3 and message['msg']=="chat":
                root_listbox.insert(0,f"{message['user']}:{message['message']}")  # type: ignore
                root_listbox.yview(0)      # type: ignore
                print(message['message'])
            elif(len(message)==3 and message['msg']=='broadcast_img'):
                    name = message['user']
                    file = open(f'clients_images/{name}.png',"wb")
                    try:
                        image_chunk = message['img']
                        print("still loading")
                        file.write(image_chunk)
                    except Exception as ex:
                        print(ex,'in recv img')
                    finally:
                        file.close()
            elif len(message)==2:#only text
                print(message,"normal")
            elif message['x1y1']!=[]:
                start_new_thread(paint,(canvas,message['x1y1'],message['x2y2'],message['drawing_color']))
            elif message['msg']=="":
                print(message,"deso number 1")
            elif message['msg']=="clear":
                canvas.delete('all')  # type: ignore
                
            else:
                print(message,"nooooooo :(")
        except Exception  as ex:
            if not(str(ex).__contains__("main thread is not in")):
                print(ex,"asdasdasd")
            
def recievex_message():
    '''Recieve an incoming message from the server'''
    global name,clients
    while True:
        try:
            #Recieve an incoming message from the server.
            message = client_socket.recv(BYTESIZE).decode(ENCODER)
            import string
            import random
            #Check for the name flag, else show the message
            if message == "NAME":
                # name = input("What is your name: ")
                name = random.choice(string.ascii_letters + string.digits)+ random.choice(string.ascii_letters + string.digits)+ random.choice(string.ascii_letters + string.digits)+ random.choice(string.ascii_letters + string.digits)
                while name in clients or (name.__len__()<3 or name.__len__()>9):
                    if((name.__len__()<3 or name.__len__()>9)):
                        print("Type username length between 3 to 8")
                    name = input("What is your name: ")
                    
                message = pickle.dumps({"msg":name})
                client_socket.send(message)
                print(name,"encoded name")
                main_thread = threading.Thread(target=lobbyScreen())  # type: ignore
                main_thread.start()

        except Exception  as ex:
            print(ex,"Server Is Full.")
            #An error occured, close the connection
            client_socket.close()
            break
    recievex_message()


def lobbyScreen():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
    root.geometry("+{}+{}".format(positionRight, positionDown))
    root.resizable(False, False) 
    root.title("LobbyScreen")
    root.config(background='white')
    waiting_lbl = tk.Label(root,text = f"Waiting Lobby",   bg='#c4c4c4',
                                            relief='flat',
                                            width=25,
                                            height=2,)
    waiting_lbl.grid(row=0,column=4)
    # Create a canvas object and place it at the bottom of the window
    canvasx = tk.Canvas(root, borderwidth=0,width = 600,height = 450, highlightthickness=0, background='white')
    global wait_players,clients
    wait_players = True
    canvasx.grid(column=0, row=1, columnspan=10)
    global lbl1,lbl2,lbl3,lbl4 
    try:
        while wait_players:
            if clients.__len__()>=1:
                lbl1 = tk.Label(canvasx,text = f"playerName:{clients[0]}")
                lbl1.place(x = 110,y = 100)
                try:
                    canvasx.delete("player2")
                    canvasx.delete("player3")
                    canvasx.delete("player4")
                    lbl2.destroy()
                    lbl3.destroy()
                    lbl4.destroy()
                except:
                    pass
                canvasx.create_rectangle(50,20,250,200,fill="#fb0",tags="player1",)
                if(players_full==1):
                    wait_players = False
                    sleep(3.5)
                    root.destroy()
            if clients.__len__()>=2:
                lbl2 = tk.Label(canvasx,text = f"playerName:{clients[1]}",name="player2_lbl")
                lbl2.place(x = 410,y = 100)
                try:
                    canvasx.delete("player3")
                    canvasx.delete("player4")
                    lbl3.destroy()
                    lbl4.destroy()
                except:
                    pass
                canvasx.create_rectangle(350,20,550,200,fill="#ff0000",tags="player2")
                if(players_full==2):
                    wait_players = False
                    sleep(3.5)
                    root.destroy()
            if clients.__len__()>=3:
                lbl3 = tk.Label(canvasx,text = f"playerName:{clients[2]}")
                lbl3.place(x = 110,y = 310)
                try:
                    canvasx.delete("player4")
                    lbl4.destroy()
                except:
                    pass
                canvasx.create_rectangle(50,220,250,410,fill="#00ff00",tags="player3")
                if(players_full==3):
                    wait_players = False
                    sleep(3.5)
                    root.destroy()
            if clients.__len__()==4:
                lbl4 = tk.Label(canvasx,text = f"playerName:{clients[1]}")
                lbl4.place(x = 410,y = 310)
                canvasx.create_rectangle(350,220,550,410,fill="#0000ff",tags="player4")
                countdown_label = tk.Label(text="Lobby is ready",
                                    fg='black',
                                    bg='#c4c4c4',
                                    relief='flat',
                                    width=20,
                                    height=2,
            )
                countdown_label.grid(column=5)
                wait_players = False
                sleep(1.5)
                root.destroy()
            start_new_thread(recieve_message, ())
            root.update()
        thread = threading.Thread(countdown_screen())
        thread.start()
    except Exception as ex:
        if(str(ex).__contains__("has been destroyed")):
            print(ex,'zxcxxxxxx')
            root.quit()
            quit()





def countdown_screen():
    try:
        global Lobby_countdown
        root = tk.Tk()
        root.attributes('-topmost', True)
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        # Gets both half the screen width/height and window width/height
        positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
        root.geometry("+{}+{}".format(positionRight, positionDown))
        root.resizable(False, False) 
        root.title("CountDownScreen")
        root.config(background='white')
        if(clients[0]==name):
            message = pickle.dumps({"msg":"start_Lobbycountdown"})
            client_socket.send(message)
        sleep(1.5)
        message = pickle.dumps({"msg":"clients_turn"})
        client_socket.send(message)

        _label = tk.Label(text="Time Left To start the game",fg='black',
                                            bg='#c4c4c4',
                                            relief='flat',
                                            width=20,
                                            height=2,
                    )
        _label.grid(column=5)
        countdown_label = tk.Label(fg='black',
                                            bg='#c4c4c4',
                                            relief='flat',
                                            width=20,
                                            height=2,
                    )
        countdown_label.grid(column=5)
        while True:
            countdown_label['text'] = Lobby_countdown
            if(Lobby_countdown==0):
                break
            root.update()
        root.destroy()
        main_thread = threading.Thread(target=__main__())
        main_thread.start()
    except Exception as ex:
        print("error in countdown_screen",ex)




class App(tk.Tk):
    def __init__(self,screen):#0main_1winner
        try:
            super().__init__()

            
            if(screen==0):
                self.title('Webpage Download')
                self.geometry('680x430')
                self.__main__()
            else:
                self.title('Webpage Download')
                self.geometry('820x700')
                self.winner_screen()

        except Exception as ex:
            if(str(ex).__contains__("has been destroyed")):
                print(ex,'zxcxxxxxx')
                self.quit()
                quit()
            else:
                print("error in winner_screen",ex)
            print("error in init")
    def endGame(self):
        global current_colour,canvas,var,players_notPlayed,player_turn,players_Played,Game_countdown
        try:
            while Game_countdown!=-1:
                if(Game_countdown==0 and (len(players_notPlayed)==0 and len(players_Played)==players_full)):
                    if(player_turn == name):
                        save_as_png(canvas,name)
                        print('last round')
                        file = open(f'images/{name}.png',"rb")
                        image_data = file.read(BYTESIZE)
                        print("sending image")
                        message = pickle.dumps({'user':name,'image':image_data,'msg':'recv_image'})
                        client_socket.send(message)  # type: ignore
                        image_data= file.read(BYTESIZE)
                        file.close()
                    Game_countdown= Game_countdown-1
                    print("sending done")
                    print("end")
                elif(Game_countdown==0):
                    if(player_turn == name):
                        save_as_png(canvas,name)
                        print('end round')
                        file = open(f'images/{name}.png',"rb")
                        image_data = file.read(BYTESIZE)
                        print("sending image")
                        message = pickle.dumps({'user':name,'image':image_data,'msg':'recv_image'})
                        client_socket.send(message)  # type: ignore
                        image_data= file.read(BYTESIZE)
                        file.close()
                    print("sending done")
                    Game_countdown= Game_countdown-1
                self.update()
            self.destroy()
            
                
        except Exception as ex:
            if not (str(ex).__contains__("can't delete Tcl")or str(ex).__contains__("in main loop")):
                print(ex,"error in end game")
    def winner_screen(self):
        try:
            print("hi winner")
            if(clients[0]==name):
                message = pickle.dumps({"msg":"who_is_the_winner"})
                client_socket.send(message)
            sleep(1.5)
            while True:
                try:
                    for item in winners_lossers_List:
                        if(item['status']=='winner'):
                            label = tk.Label(self,text=f'the Winner is:{item["name"]},Answer is {doodle_turn}', fg='white', bg='green',font=("Arial", 20))
                            label.place(x = 230,y = 20)
                            break
                        else:
                            label = tk.Label(self,text=f'All Losers,Answer is {doodle_turn}', fg='white', bg='red',font=("Arial", 20))
                            label.place(x = 230,y = 20)
                except:
                    pass
                if(len(clients)>=1):
                    label_p1 = tk.Label(self,text=winners_lossers_List[0]['name'], fg='white', bg='black',font=("Arial", 15))
                    label_p1.place(x = 150,y = 80)
                    canvas_p1= tk.Canvas(self, width= 300, height= 200)
                    canvas_p1.place(x = 30,y = 110)
                    try:
                        img_p1 = tk.PhotoImage(file= f'clients_images/{winners_lossers_List[0]["name"]}.png')
                        canvas_p1.create_image(150,95,image=img_p1)
                    except Exception as ex:
                        print(ex,"img_1")
                    label_predict_1 = tk.Label(self,text=f"{winners_lossers_List[0]['pred']}", fg='white', bg='red',font=("Arial", 15))
                    label_predict_1.place(x = 30,y = 315)
                if(len(clients)>=2):
                    label_p2 = tk.Label(self,text=f"{winners_lossers_List[1]['name']}", fg='white', bg='black',font=("Arial", 15))
                    label_p2.place(x = 630,y = 80)
                    canvas_p2= tk.Canvas(self, width= 300, height= 200)
                    canvas_p2.place(x = 500,y = 110)
                    try:
                        img_p2 = tk.PhotoImage(file=(f'clients_images/{winners_lossers_List[1]["name"]}.png'))
                        canvas_p2.create_image(150,95,image=img_p2)
                    except Exception as ex:
                        print(ex,"img_2")

                    label_predict_2 = tk.Label(self,text=f"{winners_lossers_List[1]['pred']}", fg='white', bg='red',font=("Arial", 15))
                    label_predict_2.place(x = 500,y = 315)
                if(len(clients)>=3):
                    label_p3 = tk.Label(self,text=f"{winners_lossers_List[2]['name']}", fg='white', bg='black',font=("Arial", 15))
                    label_p3.place(x = 150,y = 360)
                    canvas_p3= tk.Canvas(self, width= 300, height= 200)
                    canvas_p3.place(x = 30,y = 390)
                    try:
                        img_p3 = tk.PhotoImage(file=(f'clients_images/{winners_lossers_List[2]["name"]}.png'))
                        canvas_p3.create_image(150,95,image=img_p3)
                    except Exception as ex:
                        print(ex,"img_3")
                    label_predict_3 = tk.Label(self,text=f"{winners_lossers_List[2]['pred']}", fg='white', bg='red',font=("Arial", 15))
                    label_predict_3.place(x = 30,y = 595)
                if(len(clients)==4):
                    label_p4 = tk.Label(self,text=f"{winners_lossers_List[3]['name']}", fg='white', bg='black',font=("Arial", 15))
                    label_p4.place(x = 630,y = 360) 
                    canvas_p4= tk.Canvas(self, width= 300, height= 200)
                    canvas_p4.place(x = 500,y = 390)
                    try:
                        img_p4 = tk.PhotoImage(file=(f'clients_images/{winners_lossers_List[3]["name"]}.png'))
                        canvas_p4.create_image(150,95,image=img_p4)
                    except:
                        pass
                    label_predict_4 = tk.Label(self,text=f"{winners_lossers_List[3]['pred']}", fg='white', bg='red',font=("Arial", 15))
                    label_predict_4.place(x = 500,y = 595)
                self.mainloop()
                
        except Exception as ex:
            if(str(ex).__contains__("has been destroyed")):
                print(ex,'zxcxxxxxx')
                self.quit()
                quit()
                self.destroy()
            else:
                print("error in winner_screen",ex)
    def __main__(self):
        global current_colour,canvas,var,players_notPlayed,player_turn,players_Played,Game_countdown,chat_var
        try:        
            var =tk.StringVar()
            chat_var = tk.StringVar()

            # root =tk.Tk()
            # Create the window
            self.title("Whiteboard_Game")
            self.config(background='white')
            # Create and style buttons
            self.red_button = tk.Button(self,text='red',
                                foreground='white',
                                background='red',
                                relief='flat',
                                command=lambda: change_colour('red')
                                )

            self.blue_button = tk.Button(self,text='blue',
                                    foreground='white',
                                    background='blue',
                                    relief='flat',
                                    command=lambda: change_colour('blue')
                                    )

            self.green_button = tk.Button(self,text='green',
                                    foreground='white',
                                    background='green',
                                    relief='flat',
                                    command=lambda: change_colour('green')
                                    )

            self.black_button = tk.Button(self,text='black',
                                    foreground='white',
                                    background='black',
                                    relief='flat',
                                    command=lambda: change_colour('black')
                                    )

            self.clear_button = tk.Button(self,text='Clear',
                                    fg='black',
                                    bg='#c4c4c4',
                                    relief='flat',
                                    command=lambda:  send_message("",current_colour)
                                    )
            self.erase_button = tk.Button(self,text='Erase',
                                    fg='black',
                                    bg='#c4c4c4',
                                    relief='flat',  
                                    command=lambda: change_colour('white')
                                    )
            self.client_scrollbar = tk.Scrollbar(self, orient='vertical')
            self.client_listbox = tk.Listbox(self, height=14, width=35, borderwidth=3, bg='light grey', yscrollcommand=self.client_scrollbar.set)
            self.client_scrollbar.config(command=self.client_listbox.yview)
            global root_listbox
            root_listbox = self.client_listbox
            # self.readchatBox = tk.Entry(self, 
            #     bg = "light grey",state='disabled',textvariable=chat_var)  # type: ignore
            self.chatBox = tk.Text(self, height = 2,
                width = 27,
                bg = "light grey",)
            self.sendmsg = tk.Button(self,text='Send',
                                    fg='black',
                                    bg='#c4c4c4',
                                    relief='flat',  
                                    command= lambda: send_chat(self.chatBox)  # type: ignore
                                    )
            self.endround = tk.Button(self,text='endround',
                                    fg='red',
                                    bg='#c4c4c4',
                                    relief='flat',  
                                    command= lambda: end_Round()  # type: ignore
                                    )
            self.client_listbox.place(x=420,y=20)
            self.chatBox.place(x=420,y=260)
            self.sendmsg.place(x=420,y=300)
            # Place buttons horizontally above drawing area
            print(name,player_turn)
            if(name==player_turn):
                self.red_button.grid(column=0, row=0)
                self.blue_button.grid(column=1, row=0)
                self.green_button.grid(column=2, row=0)
                self.black_button.grid(column=3, row=0)
                self.clear_button.grid(column=4, row=0)
                self.erase_button.grid(column=5, row=0)
                self.endround.place(x=575,y=300)
                # self.chatBox.place(x=420,y=20,height=200,width=120)
                

                


            notplayed_turn=''
            try:
                notplayed_turn = players_notPlayed[0]
            except:pass
            if(name==player_turn or notplayed_turn==name or name in players_Played ):
                canvas = tk.Canvas(self,borderwidth=0,width = 400,height = 300, highlightthickness=4, background='white')
                canvas.grid(column=0, row=1, columnspan=10)
            else:
                canvas = tk.Canvas( self,borderwidth=0,width = 400,height = 300, highlightthickness=0, background='black')
                label = tk.Label(text='Wait until Your turn', fg='white', bg='black')
                label.grid(column=5, row=5)
            label = tk.Label(text=str(player_turn), fg='white', bg='black')
            label.grid(column=8)
            if(player_turn==name):
                if(players_Played.__len__()==0):
                    self.Label = tk.Label(text=f'Draw:{doodle_turn}', fg='white', bg='black')
                    self.Label.grid(column=6, row=0)
                message = pickle.dumps({"msg":"start_Gamecountdown"})
                client_socket.send(message)
            sleep(.5)

            while Game_countdown!=-1:
                try:
                    label = tk.Label(self,textvariable=var, fg='white', bg='black')
                    label.grid(column=7, row=0)
                except:
                    pass
                # print(Game_countdown)
                try:
                    start_new_thread(recieve_message, ())
                    start_new_thread(App.endGame,(self,))
                except:
                    pass
                sleep(1)
                if(name==player_turn):
                    try:
                        canvas.bind("<B1-Motion>", lambda event: start_new_thread(send_message,(event,current_colour,)))  # type: ignore
                    except:pass
                    
                self.mainloop()
            try:
                players_Played.append(player_turn)
                try:
                    player_turn = players_notPlayed.pop()
                except:
                    pass
                print(players_Played,"players played")
                print(players_notPlayed,"players not played")
                print(player_turn,"player turn")
                sleep(1)
                if(len(players_notPlayed)!=0):
                    main_thread = threading.Thread(target=App.__init__(self,0))
                    main_thread.start()
                elif(len(players_notPlayed)==0):
                    players_Played.append(player_turn)
                    if(len(players_Played)==players_full):
                        main_thread = threading.Thread(target=App.__init__(self,0))
                        main_thread.start()
                    else:
                        print("done el7amdollah")
                        main_thread = threading.Thread(target=App.__init__(self,1))
                        main_thread.start()
                self.destroy()
            except:
               pass
        except Exception as ex:
            print(ex,"error in main")            
def __main__():
    try:
        app = App(0)
        app.update()
    except:
        print("error in main __main__")
    
#Create threads to continuously send and recieve messages
try:
    recieve_thread = threading.Thread(target=recievex_message)
    #Start the client
    recieve_thread.start()
except:
    print("main test ??")