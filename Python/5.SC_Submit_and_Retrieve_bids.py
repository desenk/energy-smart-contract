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


#########################  To Run the interaction with Matlab ############################
# First, follow the instructions below: https://uk.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html 
# 1. Make sure you have Python in your PATH.
# 2. Find the Matlab root folder. You can use the matlabroot command within Matlab to find it.
# 3. In the windows Command line ("cmd" opened with admin rights) Go to the Matlab root folder in the command line by typing cd "matlabroot\extern\engines\python" (In Windows)
# 4. Type in python setup.py install 
# 6. In matlab (opened with admin rights ) type in :cd (fullfile(matlabroot,'extern','engines','python'))
#                                                      system('python setup.py install')
# Then, uncomment the 2 following lines:
""" import matlab.engine
matlab_eng = matlab.engine.start_matlab() """

# This Smart Contract aims to:
# 1. Open a Market Place as defined in SC_1_Bid_and_Payment.sol
# 2. Submit bids from 2 agents (1 seller 1 buyer)
# 3. retrieve the bids (by the DSO/operator) 


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

# We define the agent's accounts
# The operator/DSO:
w3.eth.defaultAccount = w3.eth.accounts[0]
# The Seller:
SellerAgentAccount = w3.eth.accounts[1]
# The Buyer:
BuyerAgentAccount = w3.eth.accounts[2]



# Compile the contract
contract_source_path = 'c:/Users/bc111/OneDrive - Heriot-Watt University/Smart-Grids/Blockchain/Smart_Contracts/SmartContracts_VSCode/Python_Main_files/SC_0_Bid_and_Retrieve.sol'
compiled_sol = compile_source_file('c:/Users/bc111/OneDrive - Heriot-Watt University/Smart-Grids/Blockchain/Smart_Contracts/SmartContracts_VSCode/Python_Main_files/SC_0_Bid_and_Retrieve.sol')
contract_id, contract_interface = compiled_sol.popitem()

# retrieve the compilation results (abi and bytecode)
abi = contract_interface['abi']
bytecode = contract_interface['bin']
# print(abi)
# Deployment of the contract
address = deploy_contract(w3, contract_interface)
contract = w3.eth.contract(
    address = address,
    abi = abi
)

print("Deployed {0} to: {1}\n".format(contract_id, address))
gas_estimate = contract.functions.submitBid(10, 10, 1, 0).estimateGas() #submitbid the function defined in the SC_1_Bid_and_Payment.sol smart contract - 
# arg(1) =10 is the bid price
# arg(2) =10 is the bidQuantity
# arg(3) =1 is the bidWeight
# arg(4) =0 is the agent type (0 for seller, 1 for buyer)
print("Gas estimate to transact with submitBid: {0}\n".format(gas_estimate))

if gas_estimate < 200000:
    # The seller submits his offer:
  print("Submitting Offer from Seller\n")
  tx_hash = contract.functions.submitBid(10, 10, 1, 0).transact({'from': SellerAgentAccount}) # the 
  #functions.transact() executes the specified function by sending a new public transaction.
  receipt = w3.eth.waitForTransactionReceipt(tx_hash)
# arg(1) =10 is the bid price
# arg(2) =10 is the bidQuantity
# arg(3) =1 is the bidWeight
# arg(4) =0 is the agent type  (0 for seller, 1 for buyer)
  # The buyer submits his bid
  tx_hash = contract.functions.submitBid(1, 5, 1, 1).transact({'from': BuyerAgentAccount})
  receipt = w3.eth.waitForTransactionReceipt(tx_hash)
  """   print("Transaction receipt mined: \n")
  pprint.pprint(dict(receipt))
  print("Was transaction successful? \n")
  pprint.pprint(receipt['status']) """
else:
  print("Gas cost exceeds 200000")

# Now the Operator/DSO retrieves the bids
# First retrieves the seller's bid
tx_hash = contract.functions.retrievebid(SellerAgentAccount).transact()
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
sellerData = contract.functions.retrievebid(SellerAgentAccount).call()
# Then retrieves the Buyer's bid
tx_hash = contract.functions.retrievebid(BuyerAgentAccount).transact()
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
buyerData = contract.functions.retrievebid(BuyerAgentAccount).call()

# we check that the DSO retrieve the buyer's
print(contract.functions.retrievebid(BuyerAgentAccount).call())

# Then, the DSO/Operator realizes the negotiations and validation of the grid offline (Matlab code)
# We send the values to Matlab, and retrieve the price to pay. 
Price_to_pay = 19
# #If using Matlab, please uncomment the following line
""" Price_to_pay = matlab_eng.Compute_Price_to_Pay(buyerData,sellerData)"""
print(Price_to_pay)

# Then, we will proceed to the payment using the Smart Contract



