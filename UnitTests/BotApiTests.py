import unittest
from ..src import bot_api

class BotApiTests(unittest.TestCase):
    def test_GetUserBalance_WhenUserDoesNotExist_ThenReturn0(self):
        testDatabase = Database('testDb.db')
        userName = "testUserName"

        result = testDatabase.GetUserBalance(userName)
        self.assertEqual(result, 0)


unittest.main()
