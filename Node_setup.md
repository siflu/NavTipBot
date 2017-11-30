# How to set up a NavCoin Node for NavTipBot

1. Download Navcoin Core Wallet for host OS: https://navcoin.org/downloads/    
      *-We will want to figure out how to just use CLI/daemon in production I think*
2. Open Navcoin Core wallet to download blockchain(this could take some time). I recommend downloading blockchain bootstap here: https://navcoin.org/advanced-downloads/
3. If you downloaded blockchain bootstrap, unzip and copy and paste folders into Navcoin4 directory. You will end up replace the blockchain and chainstate folders. The location will vary by OS. On Windows it was located here: C:\Users\<windows_user_name>\AppData\Roaming\NavCoin4   
4. In the same folder, create a navcoin.conf file (see example file I added). Include an rpcusername and rpcpassword. These can be any values for testing I believe.
5. Start the Navcoin Daemon. It takes at least a few minutes to make it usable(just let it run) and probably longer if it is the first time.  On Windows you can find it here: C:\Program Files\NavCoin\daemon\navcoind.exe
6. Input the rpcusername and rpcpassword values you created into navJSONRPC.py file. When you run the python script you should get some JSON values back.    
