# -- coding: utf-8 --
"""
Created on Wed Apr 12 14:16:22 2023

@author: Maya
"""

#Disclaimer: Throughout the project, we -Maya, Kareem, and Omar-made sure to collaborate closely on
# each part of the project. For each functionality of the code, we worked on it together, ensuring that 
#all team members contributed equally. We maintained a highly cooperative approach, addressing any issues
# that arose as a team and working together to find effective solutions.
import socket
import random
from datetime import datetime
import time
import sys

#time functions
Date= datetime.now()
Time= Date.strftime("%H:%M:%S")

#Socket intialization
Server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)

Address=[]
p=2       #number of players
RTTs=[]
score=[]
for i in range(p):
    RTTs.append([])
    score.append(0)

#gethostbyname :IP address of the local host
#gethostname:returns the host name of the current system under
#which the Python interpreter is executed.
Name= socket.gethostbyname(socket.gethostname())
Port= 3566
#Binding
Server.bind((Name,Port))


#Listen 
Server.listen()
n=sys.maxsize
print("Waiting for Connection...")

Rematch="yes"
Rematcharr=[]


try: #checks if all the players are still connected 
    for i in range(p): #we accept connection for only "p" players , it's adjustable in the begining of the code.
        Address.append(Server.accept())
        print("Player "+str(i+1)+" joined")
        WelcomeM="You've connected sucessfully! \nYou are Player"+str(i+1)  #we send a welcome message to all the players
        Address[i][0].send(WelcomeM.encode())
    
    while(Rematch=="yes"):# the rematch is intially yes, so for round 1 it can run automatically
        for i in range(p): #we in re-intialize the RTTs and scores to 0 at the begining of each match
            RTTs[i]=[]
            score[i]=0
        print(" ")
        for i in range(3): #loop for 3 rounds
            for j in range(p): #for each player, send the random integer between 0-9
                x=random.randint(0,9) 
                Address[j][0].send(str(x).encode())
                RTTBegin= time.time()  #start timer for RTT, where we sent the message(recieved by the player)
                Player1Ans=Address[j][0].recv(4096).decode() #recieve the answer 
                RTTEnd= time.time() #end the timer for RTT, when we just recieved the response of the client
                RTTs[j].append(RTTEnd-RTTBegin) # we're storing the RTTs in an array, so that we can sort then display in decending order
                if Player1Ans!=str(x): #if the client's response is wrong, we notify them and disqualify by giving them a DSQ, that is infinity thus they will automatically lose the round(highest RTT)
                    Wrong="Wrong input, you have been disqualified for this round! Careful"
                    Address[j][0].send(Wrong.encode())
                    RTTs[j][i]=n
                else: #if correct, just notify the client that their response is true
                    correct="Correct!" 
                    Address[j][0].send(correct.encode())
                    
            
            resultM=""
            results = [RTTs[j][i] for j in range(p)]       #RTTs[j][i]: j is the Player, i is the Round
            results_c = results.copy()  #we used the copy of the results to be able to delete from it afterwards (see line 86)
            results_s = results.copy()
            results_s.sort(reverse=1) #sort in decending order
            for j in range(p): #going from the slowest to the fastest player and displaying their player number and RTT
                ind = results_c.index(results_s[j]) 
                if results[ind]==n:
                    resultM += str(j+1)+". Player"+str(ind+1)+": DSQ\n"
                else:
                    resultM += str(j+1)+". Player"+str(ind+1)+": RTT = "+str(results_c[ind])+"\n"
                results_c[ind]=-1                  #so the same player doesn't appear twice in case of a tie
            
            if results_s[p-1]!=n: #if everyone is disqualified, no one gets a point
                score[results.index(min(results))]+=1
            
            
            
            scoreM="Scores: \n"
            score_c = score.copy()  #we used the copy of the scores to be able to delete from it afterwards (see line 100)
            score_s = score.copy()
            score_s.sort(reverse=1) #sort in decending order
            for j in range(p): ##going from the highest to the lowest score and displaying their player number and corresponding score
                ind = score_c.index(score_s[j])
                scoreM += str(j+1)+". Player"+str(ind+1)+": "+str(score_c[ind])+"\n"
                score_c[ind]=-1

            
            for j in range(p): #send all the results at once to all the players 
                Address[j][0].send((resultM+"\n\n"+scoreM).encode())
         
        
        
        tiewinners = []  #diplay many winners in case there was a tie in final scores
        maxscore = max(score) #detects the max score achieved 
        for i in range (len(score)): #we loop over the scores of the players, if they match the max score, we append them in the array "tiewinners"
            if score[i] == maxscore:
                tiewinners.append(i);
        if len(tiewinners) == 1: #if there's only 1 player in the array, then he's the only winner and there's no tie
                WinnerM="The winner is Player"+str(tiewinners[0]+1)+"\nThe game has ended."
        else: #if there's 2 or more players, then there's a tie, and we display them to all the players 
                WinnerM="It's a Tie! The winners are:\n"
                for i in range(len(tiewinners)):
                    WinnerM=WinnerM + "Player" + str(tiewinners[i]+1) + " \n"
                 
            
        #Rematch
        for i in range(p): #for each player we ask whether they want to rematch or not and we add their responses in an array 
            message="Do you wish to rematch?"
            Address[i][0].send((WinnerM+message).encode())
            response=Address[i][0].recv(4096).decode()
            Rematcharr.append(response)
        y=len(Rematcharr)      
        for i in range(y): #for the number of responses, if all of them were a 'yes',we rematch. If 1 "no" was there, we don't rematch
           if (Rematcharr[i]=="NO" or Rematcharr[i]=="No" or Rematcharr[i]=="no"): 
                Rematch="no" 
               
        if (Rematch=="yes"): # in case 1 of the players said no to rematch, then the rematch will become "NO" , so it skip this loop that is responsible for rematching
            for k in range(p):
                 endgame="Let's Play Again!"
                 Address[k][0].send(endgame.encode())
        else: # no rematch, then we close connections
            for k in range(p):
                 endgame="No rematch will happen. Have a nice day!"
                 Address[k][0].send(endgame.encode())
                 Address[k][0].close()
            Rematch="no" # again change the rematch to "no" so that the code exits the while loop 
            break
    
    
except socket.error or not Player1Ans: #in case 1 or more players are disconnected, we end the game for all and send the below message
    errormess="Game ended due to a player disconnecting"
    j=0
    try:
        while j<p:
            Address[j][0].send(errormess.encode())
            j=j+1
    except:
        j=j+1
        
               
         
        
          

Server.close()