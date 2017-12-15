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
my_inbox = reddit.inbox

while True:
    #tip logic branch
    for submission in subreddit.hot(limit=10):
        for comment in submission.comments:
            #only reply, if not already replied to this comment
            dbCommentId = a.CheckCommentsRepliedTo(comment.id)
            try:
                #checks for matching commentIDs    
                if comment.id == dbCommentId[0][0]:
                    print("Already commented!")
            except:
                amount = re.search("!tip\s(\d*)\snav /u/NavTipBot", comment.body, re.IGNORECASE)
                if amount is not None:
                    #check if user is created already and if user has a zero balance
                    if a.GetUser(comment.author) is None:
                        #Create User
                        a.CreateUser(comment.author)
                        #generate Nav address and save to DB
                        navAddress = get_new_address()
                        a.SaveNavAddress(navAddress,comment.author)
                        #Reddit message to user asking for a deposit to Nav Address, amount is just a place holder value for now
                        #Doesn't seem to be a way to get the messageID from sent messages in Reddit that I can see. This seems wrong but will investigate
                        message = "No account. To tip with NavCoin please send some NavCoins to the following address: " + navAddress  
                        reddit.redditor(str(comment.author)).message('Deposit', str(message))
                        a.DepositRequest(navAddress, comment.author, amount.group(1),0, False)
                    elif a.GetUserBalance(comment.author) < int(amount.group(1)):
                        navAddress = get_new_address()
                        a.SaveNavAddress(navAddress,comment.author)
                        #Reddit message to user asking for a deposit to Nav Address, amount is just a place holder value for now
                        #Doesn't seem to be a way to get the messageID from sent messages in Reddit that I can see. This seems wrong but will investigate
                        message = "Low balance. To tip with NavCoin please send some NavCoins to the following address: " + navAddress
                        reddit.redditor(str(comment.author)).message('Deposit', str(message))
                        a.DepositRequest(navAddress, comment.author, amount.group(1),0, False)
                    elif a.GetUser(submission.author) is None:
                        a.CreateUser(submission.author)
                        if a.GetUserBalance(comment.author) >= int(amount.group(1)):
                            a.SubtractNavsFromBalance(comment.author, int(amount.group(1)))
                            a.AddNavsToBalance(submission.author, int(amount.group(1)))
                            comment.reply("Your Navcoin tip was sent to "+submission.author)
                            #Reddit message to user informing them of Nav sent.
                            message = "You have been sent " + amount.group(1) +" Nav coins. To withdraw, reply with !withdraw followed by your Navcoin Wallet Address"
                            reddit.redditor(str(submission.author)).message("You've got Nav!", str(message))
                    elif a.GetUser(submission.author) is not None:
                        if a.GetUserBalance(comment.author) >= int(amount.group(1)):
                            a.SubtractNavsFromBalance(comment.author, int(amount.group(1)))
                            a.AddNavsToBalance(submission.author, int(amount.group(1)))
                            comment.reply("Your Navcoin tip was sent to "+submission.author)
                            #Reddit message to user informing them of Nav sent.
                            message = "You have been sent " + amount.group(1) +" Nav coins. To withdraw, reply with !withdraw followed by your Navcoin Wallet Address"
                            reddit.redditor(str(submission.author)).message("You've got Nav!", str(message))
                a.AddCommentReplied(comment.id)

    #withdraw/deposit logic branch
    for item in my_inbox.unread():
        if item.subject.lower() == '!createaccount':
            if a.GetUser(item.author) is None:
                a.CreateUser(item.author)
                #Reddit message to user asking for a deposit to Nav Address, amount is just a place holder value for now
                #Doesn't seem to be a way to get the messageID from sent messages in Reddit that I can see. This seems wrong but will investigate
                message = "Welcome! To tip with Navcoin send a private message with the subject '!deposit' with an amount in the message body. You will receive a message with a Navcoin Wallet address. Send Navcoins equal to your deposit request. Once confirmed, you can top Reddit Submission authors with the comamnd '!tip X nav /u/NavTipBot' where X equals the number of Nav to tip."  
                reddit.redditor(str(item.author)).message('Welcome', str(message))              
        if item.subject.lower() == '!withdraw':
            withdraw_account = int(item.body)
            withdraw_amount = a.GetUserBalance(item.author)
            if withdraw_amount >= 1:
                a.SubtractNavsFromBalance(item.author, withdraw_amount)
                withdraw_nav(withdraw_account, withdraw_amount)
                my_inbox.mark_read(item) 
            else:
                message = "You don't have enough Nav to withdraw."
                reddit.redditor(str(item.author)).message("No balance", str(message))
                my_inbox.mark_read(item) 
        elif item.subject.lower() == '!deposit':
            if a.GetUser(item.author) is None:
                deposit_amount = int(item.body)
                #Create User
                a.CreateUser(item.author)
                #message author has account created 
                navAddress = get_new_address()
                a.SaveNavAddress(navAddress,item.author)
                #Reddit message to user asking for a deposit to Nav Address
                message = "To tip with NavCoin please send "+ deposit_amount + " NavCoins to the following address: " + navAddress
                reddit.redditor(str(item.author)).message('Deposit', str(message))
                a.DepositRequest(navAddress, comment.author, deposit_amount,0, False)
                my_inbox.mark_read(item)
        else:
            my_inbox.mark_read(item)

    #Deposit confirmation branch

    to_be_confirmed = a.CheckNavConfirmation()
    for item in to_be_confirmed:
        address = item[0]
        reddit_name = item[1]
        print(address)
        print(reddit_name)
        confirmed_deposit_amount = NavDepositConfirmed(address)
        print(confirmed_deposit_amount)
        if int(confirmed_deposit_amount) > 0:
            a.AddNavsToBalance(reddit_name, confirmed_deposit_amount)
            ConfirmDeposit(address,int(confirmed_deposit_amount))
            message = "Your Navcoin deposit of " + confirmed_deposit_amount +" has been confirmed." 
            reddit.redditor(str(reddit_name)).message('Deposit', str(message))





