# networks_python

## Disclaimer:
The files in this repository were developed with instruction and guidance from Oregon State University's Intro to Computer Networks course (CS 372) in Spring 2023.

## Files include:
chatgame_server.py,
chatgame_client.py,
rdt_segment.py,
rdt_layer.py,
main.py,
unreliable.py.

### Client-Server Multiplayer Chat and Game
This program creates a chatroom between a client and server. At any point, either the client or server can exit the chat by typing /q into the message input to exit the program.
Also, either the client or server can initiate a multiplayer game (in this instance, 20 Questions). The chatroom will transition to a turn-taking multiplayer game with instructions and code structure. 
When the game ends--or if either player choose to end the game prematurely--the client and server are then redirected back to the original chatroom.



### Reliable Data Transmission
Some skeleton code was provided by OSU CS 372. This program acts as a simplified RDT layer that allows the transfer of string data through an unreliable channel in a simulated environment. 
A full data set is divided into individual packets or segments and then is transmitted from client to server in accordance of a sliding window. 
Once received, there is a check for reliable data transmission using checksum and segment numbering. The server will send cumulative acks back to client. 
In the event of an error or timeout event, this program utilizes the Go-Back-N protocol. 


