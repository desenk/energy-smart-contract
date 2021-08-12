# """ Before running this, you need to install Ganache to run a local Blockchain. Otherwise, use infura to access a node. """
# Here, addresses match the local Ganache Blockchain.
# Then, You should (maybe) install solc (open a powershell terminal or a cmd, and run "pip install solc")
# Then, You should (definitely) install solcx (open a powershell terminal or a cmd, and run "pip install py-solc-x")  https://pypi.org/project/py-solc-x/
# Finally, you should change the paths that are listed below to locate the solidity SC (here, Greeting.sol).
# import json
import time
import pprint
from web3 import Web3
from solcx import compile_source, compile_files
from solcx import install_solc
install_solc('v0.5.3')

#Python methods for interactions with Contracts  : https://web3py.readthedocs.io/en/stable/contracts.html#contract-functions
# Interactions with Contracts example: https://web3py.readthedocs.io/en/stable/contracts.html
# Examples of Solidity contracts: https://solidity.readthedocs.io/en/v0.5.10/solidity-by-example.html 


def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def deploy_contract(w3, contract_interface):
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor().transact()
#functions.transact() executes the specified function by sending a new public transaction.
    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    return address


# Connection to he Local Ganache Blockchain
ganache_url = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(ganache_url))
print(w3.isConnected())
print(w3.eth.blockNumber)

w3.eth.defaultAccount = w3.eth.accounts[0]


#open('c:/Users/bc111/OneDrive - Heriot-Watt University/Smart-Grids/Blockchain/Smart_Contracts/SmartContracts_VSCode/Python_Main_files/Greeting.sol', 'r')


contract_source_path = 'c:/Users/bc111/OneDrive - Heriot-Watt University/Smart-Grids/Blockchain/Smart_Contracts/SmartContracts_VSCode/Python_Main_files/Greeting.sol'
compiled_sol = compile_source_file('c:/Users/bc111/OneDrive - Heriot-Watt University/Smart-Grids/Blockchain/Smart_Contracts/SmartContracts_VSCode/Python_Main_files/Greeting.sol')
contract_id, contract_interface = compiled_sol.popitem()

#print(contract_interface)
abi = contract_interface['abi']
bytecode = contract_interface['bin']
print(abi)
# Deployment of the contract
address = deploy_contract(w3, contract_interface)
""" GreeterSC = w3.eth.contract(abi = abi,bytecode=bytecode)
tx_hash = GreeterSC.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash) """
contract = w3.eth.contract(
    address = address,
    abi = abi
)
#Display the result
print(contract.functions.greet().call())
print("Deployed {0} to: {1}\n".format(contract_id, address))
gas_estimate = contract.functions.setGreeting("Bonjour !").estimateGas() #setGreeting is the function defined in the Greeting.sol smart contract
print("Gas estimate to transact with setGreeting: {0}\n".format(gas_estimate))

if gas_estimate < 100000:
  print("Sending transaction SetGreeting(Bonjour)\n")
  tx_hash = contract.functions.setGreeting("Bonjour !!").transact()
#functions.transact() executes the specified function by sending a new public transaction.
  receipt = w3.eth.waitForTransactionReceipt(tx_hash)
  print("Transaction receipt mined: \n")
  pprint.pprint(dict(receipt))
  print("Was transaction successful? \n")
  pprint.pprint(receipt['status'])
else:
  print("Gas cost exceeds 100000")

tx_hash = contract.functions.greet().transact()
#functions.transact() executes the specified function by sending a new public transaction.
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
# we check that the greeting has been updated ton "bonjour"
print(contract.functions.greet().call())
#functions.transact() calls a contract function, executing the transaction locally using the eth_call API. This will not create a new public transaction.




