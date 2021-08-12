
# """ Before running this, you need to install Ganache to run a local Blockchain. Otherwise, use infura to access a node. """
# Here, addresses match the local Ganache Blockchain.

from web3 import Web3

ganache_url = "HTTP://127.0.0.1:7545"

w3 = Web3(Web3.HTTPProvider(ganache_url))
print(w3.isConnected())
print(w3.eth.blockNumber)


account_1 = "0xD98676ad351E2E0e649a1225f0E2a3C9391Be8aF"
account_2 = "0xE35ae3bdA7a787EE2ac7f1c50C7483BB3418B9b2"
private_Key_1 = "27fb7dbfbf162bdf7d6f49828d7a79cc79a6ac8f4810030c31a3de611509b594"

nonce = w3.eth.getTransactionCount(account_1)

tx = {
        'nonce': nonce,
        'to': account_2,
        'value': w3.toWei(0.1,'ether'),
        'gas': 2000000,
        'gasPrice': w3.toWei('20','gwei'),
}
signed_tx = w3.eth.account.signTransaction(tx,private_Key_1)
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(w3.toHex(tx_hash))

Block1= w3.eth.getBlock(1)
print(Block1)
