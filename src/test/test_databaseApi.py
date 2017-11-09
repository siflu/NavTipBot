import pytest
import os
from ..app.databaseApi import Database

class TestDatabaseApiTests(object):
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

    def test_AddNavsToBalance_WhenUserHas10NavsAndWantsToAdd40MoreNavs_ThenTheBalanceIs50Navs(self):
        self.CleanUp()
        userName = "testUserName"
        expectedBalance = 50
        testDatabase = Database('testDb.db')
        testDatabase.CreateUser(userName)
        testDatabase.SetUserBalance(userName, 10)
        testDatabase.AddNavsToBalance(userName, 40)

        result = testDatabase.GetUserBalance(userName)
        assert result == expectedBalance

    def test_SubtractNavsFromBalance_WhenUserHas50NavsAndWantsToSubtract20Navs_ThenTheBalanceIs30(self):
        self.CleanUp()
        userName = "testUserName"
        expectedBalance = 30
        testDatabase = Database('testDb.db')
        testDatabase.CreateUser(userName)
        testDatabase.SetUserBalance(userName, 50)
        testDatabase.SubtractNavsFromBalance(userName, 20)

        result = testDatabase.GetUserBalance(userName)
        assert result == expectedBalance

    def test_DoesUserHaveEnoughNav_WhenUserDoesNotExist_ThenReturnFalse(self):
        self.CleanUp()
        userName = "testUserName"
        testDatabase = Database('testDb.db')

        result = testDatabase.DoesUserHaveEnoughNav(userName, 10)
        assert result is False

    def test_DoesUserHaveEnoughNav_WhenTheBalanceOfTheUserIsSmallerThanTheAmount_ThenReturnFalse(self):
        self.CleanUp()
        userName = "testUserName"
        testDatabase = Database('testDb.db')
        testDatabase.CreateUser(userName)
        testDatabase.SetUserBalance(userName, 10)

        result = testDatabase.DoesUserHaveEnoughNav(userName, 50)
        assert result is False

    def test_DoesUserHaveEnoughNav_WhenTheBalanceOfTheUserIsBiggerThanTheAmount_ThenReturnTrue(self):
        self.CleanUp()
        userName = "testUserName"
        testDatabase = Database('testDb.db')
        testDatabase.CreateUser(userName)
        testDatabase.SetUserBalance(userName, 100)

        result = testDatabase.DoesUserHaveEnoughNav(userName, 50)
        assert result is True

    def CleanUp(self):
        os.remove('testDb.db')
