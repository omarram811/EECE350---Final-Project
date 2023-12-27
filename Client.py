# -- coding: utf-8 --
"""
Created on Wed Apr 12 14:23:49 2023

@author: Maya
"""

#Disclaimer: Throughout the project, we -Maya, Kareem, and Omar-made sure to collaborate closely on
# each part of the project. For each functionality of the code, we worked on it together, ensuring that 
#all team members contributed equally. We maintained a highly cooperative approach, addressing any issues
# that arose as a team and working together to find effective solutions.
import socket
#Socket intialization
Player= socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#gethostbyname :IP address of the local host
#gethostname:returns the host name of the current system under
#which the Python interpreter is executed.
Name= socket.gethostbyname(socket.gethostname())
Port= 3566
Player.connect((Name,Port))
Response= Player.recv(4096).decode() #recieving the welcome message
Rematch="yes"
print(Response)

while(Rematch=="yes"): 
    for i in range (3): # for 3 rounds, do the below
        number= Player.recv(4096).decode() #recieve the random integer between 0 and 9
        print("Round "+ str(i+1)) #display Round number
        print("Enter the Integer "+ str(number)+" ASAP!") # ask them to input the same integer as displayed
        x=input() #waits for user's input
        Player.send(x.encode()) #send the response to the server to compare "x" with the "number"
        WrongCorrect=Player.recv(4096).decode() # the server will compare and send to the client whether it's correct or wrong 
        print(WrongCorrect) #display the server's message
        details=Player.recv(4096).decode() #details contain both RTTs and Scores for all the players
        print(details)
       
        
    Announcment=Player.recv(4096).decode() #Announcment of the winner(s) + asks if the players want to rematch
    print(Announcment)
    print(" ")
    #answer=input("Yes/No? ") #waits for the player's input
    answer=input("") 
    while (answer.lower() != "yes" and answer.lower() != "no"): # loop until valid input is given
            answer=input("Invalid answer, try again: ") #waits for the player's input
    Player.send(answer.encode())   #send the response to the server to conclude whether a rematch will happen or not
    # NoRematch=Player.recv(4096).decode() #announce if a rematch will not happen, or send an empty string if it will happen
    # print(NoRematch)
    Rematch=Player.recv(4096).decode() #announce that we will be playing again if a rematch happen, if not we will only close connections
    print(Rematch)
    if Rematch[-17:]=="Let's Play Again!": #exclude the header of the message and only compare the actual message sent by the server 
        Rematch="yes"
    else:
        Rematch="No" #the code will exit the while loop
    

Player.close()