import re
import string
import urllib.request
import sqlite3
import praw

class Database:   
    def __init__(self, name='navtipbot.db'):
        print("in __init__ -> ", (name))
        self.connection = sqlite3.connect(name, check_same_thread=False)
        self.database = self.connection.cursor()
        self.CreateDatabase()
        self.addressIndex = len(self.database.execute("SELECT * FROM usedAdresses").fetchall())

    def CreateDatabase(self):
        print("in CreateDatabase")
        self.database.execute("CREATE TABLE IF NOT EXISTS Users (redditUsername TEXT PRIMARY KEY, balance INTEGER)")
        self.connection.commit()
        self.database.execute("CREATE TABLE IF NOT EXISTS CommentsRepliedTo (commentId TEXT PRIMARY KEY)")
        self.connection.commit()
        self.database.execute("CREATE TABLE IF NOT EXISTS UsedAdresses (adressIndex INTEGER PRIMARY KEY, adress TEXT)")
        self.connection.commit()
        self.database.execute("CREATE TABLE IF NOT EXISTS DepositRequests (messageId TEXT PRIMARY KEY, adress TEXT, amount INTEGER)")
        self.connection.commit()
    
    def CreateUser(self, redditUsername):
        user = self.GetUser(redditUsername)
        if not user:
            self.database.execute("INSERT INTO Users (redditUsername, balance) VALUES (?, ?)", (redditUsername, 0))
            self.connection.commit()

    def GetUserBalance(self, redditUsername):
        user = self.GetUser(redditUsername)
        if user:
            balance = user[1]
            return balance
        else:
            self.CreateUser(redditUsername)
            return self.GetUserBalance(redditUsername)

    def SetUserBalance(self, redditUsername, amount):
        user = self.GetUser(redditUsername)
        if user:
            self.database.execute("UPDATE Users SET balance=? WHERE redditUsername = ?", (amount, redditUsername))
            self.connection.commit()
        else:
            self.CreateUser(redditUsername)
            self.SetUserBalance(redditUsername,amount)

    def AddNavsToBalance(self, redditUsername, amount):
        user = self.GetUser(redditUsername)
        if user:
            balance = user[1]
            balance = balance + amount
            self.SetUserBalance(redditUsername, balance)

    def SubtractNavsFromBalance(self, redditUsername, amount):
        user = self.GetUser(redditUsername)
        if user:
            balance = user[1]
            balance = balance - amount
            self.SetUserBalance(redditUsername, balance)

    def DoesUserHaveEnoughNav(self, redditUsername, amount):
        user = self.GetUser(redditUsername)
        if user:
            balance = user[1]
            if amount > balance:
                return False
            else:
                return True
        else:
            return False

    def GetUser(self, redditUsername):
        user = self.database.execute("SELECT * FROM Users WHERE redditUsername = ?", (redditUsername,)).fetchone()
        return user



