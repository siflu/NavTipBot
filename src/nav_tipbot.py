from app import *

#test connection to NavCoin Core Node
ping()

a = Database()
print(a.GetUserBalance("testUser"))
