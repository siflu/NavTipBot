from app import *
import praw
import pdb
import re
import os
import sqlite3

#test connection to NavCoin Core Node
ping()

a = Database()
print(a.GetUserBalance("testUser"))

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='',
                     username='',
                     password='')

#check DB for comment ID
con = sqlite3.connect('navtipbot.db')
c = con.cursor()





#search all comments in submissions with the tip-text
#and reply to these comments
subreddit = reddit.subreddit('NavTipbot')


for submission in subreddit.hot(limit=10):
    for comment in submission.comments:
        #only reply, if not already replied to this comment
        dbCommentId = a.CheckCommentsRepliedTo(comment.id)
        try:
            #checks for matching commentIDs    
            if comment.id == dbCommentId[0][0]:
                print("Already commented!")
        except:
            if re.search("!tip x nav /u/NavTipBot", comment.body, re.IGNORECASE): #TODO: use regex for number
                #check if user is created already
                if a.GetUser(comment.author) is None:
                    #Create User
                    a.CreateUser(comment.author)
                    #generate Nav address and save to DB
                    navAddress = get_new_address()
                    a.SaveNavAddress(navAddress,comment.author)
                    #Reddit message to user asking for a deposit to Nav Address, amount is just a place holder value for now
                    #Doesn't seem to be a way to get the messageID from sent messages in Reddit that I can see. This seems wrong but will investigate
                    message = "To tip with NavCoin please send some NavCoins to the following address: " + navAddress
                    reddit.redditor(str(comment.author)).message('Deposit', str(message))
                    amount = 5
                    messageID = None
                    a.DepositRequest(messageID, navAddress, comment.author, amount)
                print("This is an automatic answer from NavTipBot!")  #comment.reply() replaces print
                a.AddCommentReplied(comment.id)





