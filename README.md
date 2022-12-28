# Project Title
- DoodleMe

## Description
- The project’s idea is a collaborative whiteboard game. Different players
  connect to the server and wait for other players to join where each
  player takes a turn in drawing the same item drawn by the first player
  and randomly selected by the server. Players’ drawings are assigned by
  the AI, and the losers and winners are then announced along with their
  drawings and how the AI interpreted them. Players have different
  options in the drawing panel including choosing different colours,
  erasing, and clearing all drawing options.


## DataSet used
-https://console.cloud.google.com/storage/browser/quickdraw_dataset/full/numpy_bitmap?pageState=(%22StorageObjectListTable%22:(%22f%22:%22%255B%255D%22))&prefix=&forceOnObjectsSortingFiltering=false
-![Untitled-1](https://user-images.githubusercontent.com/37198610/209829676-3f519a0b-10aa-4bb6-8cf1-6585fd9f0f57.png)


## Libraries used
•	Pickle: to dump/load (decode and encode) messages from client to
server and vice versa.
• Socket: to initiate the connection between the clients and the
server.
• Threading: to allow handling of more than one client/player
simultaneously.
• Tkinter: used for GUI and graphics.
• PIL: used for image manipulation.

## Requirements
•	Python 3.3+ or Python 2.7
• Install all libraries

## Project’s main functions:
 Client-side:
    •paint(): allows the user to draw on the canvas
    •change color(): allows the user to change the colour of the brush/pen
    •send_chat(): allows user to communicate through text messages
    •end_round(): allows the user to end the round before the countdown ends
    •clear(): allows the user to delete the whole drawing
    •send_grid(): sends the grids where the user is drawn into the server
    •save_as_png(): saves the images in .png format instead of .esp
    •receive message(): receives different messages from the server
    •recievex_message(): receives name message from the server(only used
    once to ask for the user’s name)
    •lobbyscreen(): waiting screen (room) for the players.
    •countdown_screen(): screen where the countdown starts indicating the
    game starts
    •class APP: where the game takes place and ends.
    Server•side:
    •broadcast_message(): receives a message and broadcasts it to all clients
    •broadcast_info(): broadcasts the clients’ information
    •boradcast_countdown(): keeps track of the timing as long as it is not 0 and the user did not press the end round.
    •boradcast_cluenturn(): selects random player and random
    drawing(doodle) to play.
    • receive_message(): receives a message from one client and broadcasts it
    • connect_client(): connects the clients to the server.




## Project Scenario:
  •Lobby: The game begins when the first player joins the server,
  where he/she waits in the lobby (where all players wait until their
  number is complete so that the game could start) and waits for
  other players to join the game.
  -![Screenshot (163)](https://user-images.githubusercontent.com/37198610/209830505-a711c53d-deeb-45ad-a74e-813086edc47c.png)
  
  •Countdown: once the players are complete the countdown screen appears as it signals the game is about to start
  -![Screenshot (164)](https://user-images.githubusercontent.com/37198610/209830576-c7c613eb-3984-4bb4-ad85-4bc2cabe72e5.png)

  •Player screen (canvas): once the countdown is over the players' screen
   appears for each player where the player with the current turn has a
   canvas with all the options including the colours and erase/ delete
   buttons, However; other players’ buttons will be disabled until their
   turns take place.
![Screenshot (167)](https://user-images.githubusercontent.com/37198610/209830682-5736a45d-0f11-4afc-872c-5e9587015615.png) - ![Screenshot (166)](https://user-images.githubusercontent.com/37198610/209830684-eaadc243-32f4-44ce-94a1-b69868bbe5e1.png)

## Developer
marwan eldesouki
