from app import *
import praw
import re
import sqlite3
'''
import logging

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger = logging.getLogger('prawcore')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
'''

#test connection to NavCoin Core Node
ping()

a = Database()
print(a.GetUserBalance("testUser"))

reddit = praw.Reddit()

#check DB for comment ID
con = sqlite3.connect('navtipbot.db')
c = con.cursor()

#search all comments in submissions with the tip-text
#and reply to these comments
my_inbox = reddit.inbox

'''
# 
'''
while True:
    #withdraw/deposit logic branch
    for item in my_inbox.unread():
        if item.subject.lower() == '!createaccount':
            if a.GetUser(item.author) is None:
                a.CreateUser(item.author)
                #Reddit message to user asking for a deposit to Nav Address, amount is just a place holder value for now
                #Doesn't seem to be a way to get the messageID from sent messages in Reddit that I can see. This seems wrong but will investigate
                message = "Welcome! To tip with Navcoin send a private message with the subject '!deposit' with an amount in the message body. You will receive a message with a Navcoin Wallet address. Send Navcoins equal to your deposit request. Once confirmed, you can top Reddit Submission authors with the comamnd '!tip X nav /u/NavTipBot' where X equals the number of Nav to tip."  
                reddit.redditor(str(item.author)).message('Welcome', str(message))
        elif item.subject.lower() == '!balance':
            if a.GetUser(item.author) is None:
                a.CreateUser(item.author)
                #Reddit message to user asking for a deposit to Nav Address, amount is just a place holder value for now
                #Doesn't seem to be a way to get the messageID from sent messages in Reddit that I can see. This seems wrong but will investigate
                message = "Welcome! To tip with Navcoin send a private message with the subject '!deposit' with an amount in the message body. You will receive a message with a Navcoin Wallet address. Send Navcoins equal to your deposit request. Once confirmed, you can top Reddit Submission authors with the comamnd '!tip X nav /u/NavTipBot' where X equals the number of Nav to tip."
                print(message)
                reddit.redditor(str(item.author)).message('Welcome', str(message))
            else:
                balance = float(a.GetUserBalance(item.author))
                print(balance)
                message = "Your Nav balance is: " +str(balance)
                print(message)
                reddit.redditor(str(item.author)).message('Nav Balance', str(message))
                item.mark_read()
        elif item.subject.lower() == '!withdraw':
            withdraw_account = item.body
            withdraw_amount = float(a.GetUserBalance(item.author))
            if float(withdraw_amount) >= 1:
                a.SubtractNavsFromBalance(item.author, float(withdraw_amount))
                txid = withdraw_nav(withdraw_account, float(withdraw_amount))
                message = "We have processed your withdrawal. TxID: " + str(txid)
                reddit.redditor(str(item.author)).message("Withdrawal", str(message))
                item.mark_read()
            else:
                message = "You don't have enough Nav to withdraw."
                reddit.redditor(str(item.author)).message("No balance", str(message))
                item.mark_read()
        elif item.subject.lower() == '!deposit':
            if a.GetUser(item.author) is None:
                deposit_amount = float(item.body)
                #Create User
                a.CreateUser(item.author)
                #message author has account created 
                navAddress = get_new_address()
                a.SaveNavAddress(navAddress,item.author)
                #Reddit message to user asking for a deposit to Nav Address
                message = "To tip with NavCoin please send "+ deposit_amount + " NavCoins to the following address: " + navAddress
                reddit.redditor(str(item.author)).message('Deposit', str(message))
                a.DepositRequest(navAddress, comment.author, float(deposit_amount),0, False)
                item.mark_read()
            else:
                deposit_amount = float(item.body)
                #Create User
                #message author has account created
                navAddress = get_new_address()
                a.SaveNavAddress(navAddress,item.author)
                #Reddit message to user asking for a deposit to Nav Address
                message = "To tip with NavCoin please send "+ deposit_amount + " NavCoins to the following address: " + navAddress
                reddit.redditor(str(item.author)).message('Deposit', str(message))
                a.DepositRequest(navAddress, item.author, float(deposit_amount),0, False)
                item.mark_read()
        else:
            try:
                print(item.id)
                print(item.author)
                print(item.body)
                print(item.submission.author)
                amount = re.search("!tipnav\s(\d\D*\d*)\s/u/NavTipBot", item.body, re.IGNORECASE)
                print(amount)
                if amount is not None:
                    # check if user is created already and if user has a zero balance
                    if a.GetUserBalance(item.author) < float(amount.group(1)):
                        navAddress = get_new_address()
                        a.SaveNavAddress(navAddress, item.author)
                        # Reddit message to user asking for a deposit to Nav Address, amount is just a place holder value for now
                        # Doesn't seem to be a way to get the messageID from sent messages in Reddit that I can see. This seems wrong but will investigate
                        message = "Low balance. To tip with NavCoin please send some NavCoins to the following address: " + navAddress
                        reddit.redditor(str(item.author)).message('Deposit', str(message))
                        a.DepositRequest(navAddress, item.author, float(amount.group(1)), 0, False)
                    elif a.GetUser(item.submission.author) is None:
                        a.CreateUser(item.submission.author)
                        if a.GetUserBalance(item.author) >= float(amount.group(1)):
                            a.SubtractNavsFromBalance(item.author, float(amount.group(1)))
                            a.AddNavsToBalance(item.submission.author, float(amount.group(1)))
                            comment.reply("Your Navcoin tip was sent to " + item.submission.author)
                            # Reddit message to user informing them of Nav sent.
                            message = "You have been sent " + str(amount.group(
                                1)) + " Nav coins. To withdraw, reply with !withdraw followed by your Navcoin Wallet Address"
                            reddit.redditor(str(item.submission.author)).message("You've got Nav!", str(message))
                    elif a.GetUser(item.submission.author) is not None:
                        if a.GetUserBalance(item.author) >= float(amount.group(1)):
                            a.SubtractNavsFromBalance(item.author, float(amount.group(1)))
                            a.AddNavsToBalance(item.submission.author, float(amount.group(1)))
                            comment.reply("Your Navcoin tip was sent to " + item.submission.author)
                            # Reddit message to user informing them of Nav sent.
                            message = "You have been sent " + amount.group(1) + " Nav coins. To withdraw, reply with !withdraw followed by your Navcoin Wallet Address"
                            reddit.redditor(str(item.submission.author)).message("You've got Nav!", str(message))
                    elif a.GetUser(item.author) is None:
                        # Create User
                        a.CreateUser(item.author)
                        # generate Nav address and save to DB
                        navAddress = get_new_address()
                        a.SaveNavAddress(navAddress, item.author)
                        # Reddit message to user asking for a deposit to Nav Address, amount is just a place holder value for now
                        # Doesn't seem to be a way to get the messageID from sent messages in Reddit that I can see. This seems wrong but will investigate
                        message = "No account. To tip with NavCoin please send some NavCoins to the following address: " + navAddress
                        reddit.redditor(str(item.author)).message('Deposit', str(message))
                        a.DepositRequest(navAddress, item.author, float(amount.group(1)), 0, False)
                    print(item.id)
                try:
                    a.AddCommentReplied(item.id)
                except:
                    print('Comment ID already exists '+ item.id)
            except:
                print('Could not process message.')
            item.mark_read()

    #Deposit confirmation branch

    to_be_confirmed = a.CheckNavConfirmation()
    for item in to_be_confirmed:
        address = item[0]
        reddit_name = item[1]
        print(address)
        print(reddit_name)
        confirmed_deposit_amount = NavDepositConfirmed(address)
        print(confirmed_deposit_amount)
        if float(confirmed_deposit_amount) > 0:
            a.AddNavsToBalance(reddit_name, float(confirmed_deposit_amount))
            a.ConfirmDeposit(address, float(confirmed_deposit_amount))
            message = "Your Navcoin deposit of " + str(confirmed_deposit_amount) +" has been confirmed."
            reddit.redditor(str(reddit_name)).message('Deposit', str(message))





