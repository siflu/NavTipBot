import requests
import json


def main():
    #replace the <rpcusername> and <rpcpassword> with the ones you put in navcoin.conf file
    url = "http://<rpcusername>:<rpcpassword>@localhost:44444"
    headers = {'content-type': 'application/json'}

    payload = {
        "method": "getaccountaddress",
        "params": ["account=sloths"],
        "jsonrpc": "2.0",
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response)

    payload = {
        "method": "getbalance",
        "params": ["account=sloths"],
        "jsonrpc": "2.0",
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response)

    payload = {
        "method": "help",
        "jsonrpc": "2.0",
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response)
    
if __name__ == "__main__":
    main()
