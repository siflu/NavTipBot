import requests
import json


def main():
    #replace the <rpcusername> and <rpcpassword> with the ones you put in navcoin.conf file
    url = "http://sloth:sloth@localhost:44444"
    headers = {'content-type': 'application/json'}

    payload = {
        "method": "ping",
        "jsonrpc": "2.0",
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response)
    '''
    payload = {
        "method": "getbalance",
        "jsonrpc": "2.0",
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    print(response)
    '''
    
if __name__ == "__main__":
    main()
