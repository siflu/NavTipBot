import pytest
import os
from ..app.bot_api import Database

class TestBotApiTests(object):
    def test_GetUserBalance_WhenUserDoesNotExist_ThenReturn0(self):
        self.CleanUp()
        testDatabase = Database('testDb.db')
        userName = "testUserName"

        result = testDatabase.GetUserBalance(userName)
        assert result == 0
        
    def test_CreateUser_WhenUserIsCreated_ThenUserIsSavedToDatabase(self):
        self.CleanUp()
        userName = "createUserTest"
        testDatabase = Database('testDb.db')
        testDatabase.CreateUser(userName)

        result = testDatabase.GetUserBalance(userName)
        assert result == 0

    def test_SetUserBalance_WhenUserExistsAndHasNavs_ThenCorrectBalanceIsReturned(self):
        self.CleanUp()
        userName = "testUserName"
        expectedBalance = 100
        testDatabase = Database('testDb.db')
        testDatabase.CreateUser(userName)
        testDatabase.SetUserBalance(userName, expectedBalance)

        result = testDatabase.GetUserBalance(userName)
        assert result == expectedBalance

    def CleanUp(self):
        os.remove('testDb.db')
