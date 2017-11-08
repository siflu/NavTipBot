import pytest
from ..app.bot_api import Database

class TestBotApiTests(object):
    def test_GetUserBalance_WhenUserDoesNotExist_ThenReturn0(self):
        testDatabase = Database('testDb.db')
        userName = "testUserName"

        result = testDatabase.GetUserBalance(userName)
        assert result == 0
        