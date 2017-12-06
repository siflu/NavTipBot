import requests
import json

#replace the <rpcusername> and <rpcpassword> with the ones you put in navcoin.conf file
url = "http://<rpcuser>:<rpcpassword>@localhost:44444"
headers = {'content-type': 'application/json'}
wallet_pass = "<wallet-pw-here>"

def ping():
    payload = {
        "method": "ping",
        "jsonrpc": "2.0",
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print(response)
    return(response['result'])


#generate a new Nav coin address- we should generate an address for each deposit and store in DB
def get_new_address():
    payload = {
        "method": "getnewaddress",
        "jsonrpc": "2.0",
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print(response['result'])
    return(response['result'])

#Withdraw Nav from main wallet, user address = destination outside of tipbot
def withdraw_nav(user_address, amount):
    payload = {
        "method": "walletpassphrase",
        "params":[wallet_pass, 60],
        "jsonrpc": "2.0",
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
#The 0.0001 is to cover transaction fee on network
    
    payload = {
        "method": "sendtoaddress",
        "params": [user_address, amount - 0.0001],
        "jsonrpc": "2.0",
    }
    response2 = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response2['result'])
    return(response2['result'])


def get_wallet_balance():
    #Use this to make sure SQL database over balance is never less than wallet
    payload = {
        "method": "getbalance",
        "jsonrpc": "2.0",
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response['result'])
    return(response['result'])

