import requests
import json


def main():
    #replace the <rpcuser> and <rpcpassword> with the ones you put in navcoin.conf file
    url = "http://rpcuser:rpcpassword@127.0.0.1:44444"
    headers = {'content-type': 'application/json'}
    wallet_pass = ''

    payload = {
        "method": "getbalance",
        "jsonrpc": "2.0",
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()

    print(response)
'''

    payload = {
        "method": "walletpassphrase",
        "params": [wallet_pass, 60],
        "jsonrpc": "2.0",
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    # The 0.0001 is to cover transaction fee on network
    print(response)

    address = 'Ne8t9mSGu5JtLH8vtpc4JAfehyCA7SxVbg'
    payload = {
        "method": "sendtoaddress",
        "params": [address, 2.199-0.01],
        "jsonrpc": "2.0",
    }
    response2 = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response2['result'])
    return (response2['result'])
'''
if __name__ == "__main__":
    main()
