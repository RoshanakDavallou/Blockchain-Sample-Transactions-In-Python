#creating a sample blockchain for 3 transactions (order placement, packing and transport) in supply chain. 
#Includes classes for Block, Blockchain, DigitalWallet, DigitalProductPassport, and TokenSmartContract.

import random
import hashlib
import time
import json
import rsa
import xml.etree.ElementTree as ET

# Define the structure of a block in the blockchain
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0): # Constructor for a new block
        self.index = index # The position of the block in the chain
        self.transactions = transactions # Data (transactions) stored in the block
        self.timestamp = timestamp # Time of block creation
        self.previous_hash = previous_hash # Hash of the previous block in the chain
        self.nonce = nonce # A variable used in the proof-of-work process

    def compute_hash(self): # Computes and returns the hash of the block
        block_string = json.dumps(self.__dict__, sort_keys=True) # Convert the block's contents to a string
        return hashlib.sha256(block_string.encode()).hexdigest() # Return the SHA-256 hash of the string
    
# Define the blockchain structure
class Blockchain:
    def __init__(self):
        # Constructor for the blockchain
        self.unconfirmed_transactions = [] # Transactions yet to be added to the blockchain
        self.chain = [] # The blockchain itself
        self.create_genesis_block() # Create the first block in the chain

    def create_genesis_block(self):
        # Creates the first block (genesis block) in the blockchain
        genesis_block = Block(0, [], time.time(), "0") # Genesis block has index 0, no transactions, current time, and previous_hash "0"
        genesis_block.hash = genesis_block.compute_hash() # Compute the hash of the genesis block
        self.chain.append(genesis_block) # Add the genesis block to the chain

    @property
    def last_block(self):
        # Returns the last block in the blockchain
        return self.chain[-1]

    def add_new_transaction(self, xml_transaction):
        # Adds a new transaction to the list of unconfirmed transactions
        self.unconfirmed_transactions.append(xml_transaction)

    def proof_of_work(self, block): # Proof of work algorithm: find a nonce that results in a hash with a specific number of leading zeroes
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0000'):
            block.nonce += 1 # Increment the nonce until the hash has the desired properties
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof): # Adds a block to the chain after validating it
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False # Block is invalid if it doesn't correctly reference the hash of the previous block
        if not self.is_valid_proof(block, proof): 
            return False # Block is invalid if the proof of work is not correct
        block.hash = proof # Set the block's hash to the proof
        self.chain.append(block) # Add the block to the chain
        return True

    def is_valid_proof(self, block, block_hash): # Checks if the block's hash is valid (has the required number of leading zeroes)
        return (block_hash.startswith('0000') and block_hash == block.compute_hash())

    def mine(self): # Mines a new block with the unconfirmed transactions
        if not self.unconfirmed_transactions:
            return False # No block is mined if there are no unconfirmed transactions
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash) # Create a new block
        proof = self.proof_of_work(new_block) # Perform the proof of work
        self.add_block(new_block, proof) # Add the new block to the chain
        self.unconfirmed_transactions = [] # Clear the list of unconfirmed transactions
        return new_block.index # Return the index of the new block

class DigitalWallet: # Digital Wallet for managing tokens
    def __init__(self, owner_name):
        # Generate public and private keys for the wallet
        self.public_key, self.private_key = rsa.newkeys(2048)
        self.owner_name = owner_name
        self.balance = 0  # Initial balance

    def get_address(self):
        return self.public_key.save_pkcs1().decode()  # Returns the wallet's public key (used as an address)

    def add_tokens(self, amount): # Add tokens to the wallet
        self.balance += amount

    def spend_tokens(self, amount): # Spend tokens if sufficient balance exists
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Insufficient balance")

class DigitalProductPassport:
    def __init__(self, product_id, product_name):
        self.product_id = product_id
        self.product_name = product_name
        self.lifecycle_data = []

    def add_data(self, stage, data):
        self.lifecycle_data.append({
            "stage": stage,
            "data": data,
            "timestamp": time.time()
        })

    def get_passport(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "lifecycle_data": self.lifecycle_data
        }

# IoT devices data simulation
def simulate_iot_data():
    return {
        "carbonDioxide": f"{random.randint(20, 100)} kg",
        "nitrogenOxide": f"{random.randint(1, 5)} kg"
    }

# Token Smart Contract definition
class TokenSmartContract:
    def __init__(self, initial_supply):
        self.total_supply = initial_supply
        self.wallets = {}  # Stores wallet balances by wallet address

    def distribute_tokens(self, to, amount):
        if amount > self.total_supply:
            raise ValueError("Not enough tokens in supply")
        self.total_supply -= amount
        self.wallets[to] = self.wallets.get(to, 0) + amount

    def transfer_tokens(self, from_addr, to, amount):
        if self.wallets.get(from_addr, 0) < amount:
            raise ValueError("Not enough tokens")
        self.wallets[from_addr] -= amount
        self.wallets[to] = self.wallets.get(to, 0) + amount

    def get_balance(self, address):
        return self.wallets.get(address, 0)
    
def validate_and_parse_xml(xml_string):  # XML validation function
      try:
        root = ET.fromstring(xml_string)
        return root
      except ET.ParseError as e:
        print(f"Invalid XML format: {e}")
        return None
      
# Generate a short wallet address from public key
def get_wallet_address(public_key):
    return hashlib.sha256(public_key.save_pkcs1()).hexdigest()[:16]
          
# Creating an instance of the blockchain
blockchain = Blockchain()
# Create a token contract with 1000 tokens
token_contract = TokenSmartContract(1000)

# Create wallets for participants
supplier_wallet = DigitalWallet("Supplier")
carrier_wallet = DigitalWallet("Carrier")
retailer_wallet = DigitalWallet("Retailer")

# Distribute tokens to the wallets
token_contract.distribute_tokens(supplier_wallet.get_address(), 500)
token_contract.distribute_tokens(carrier_wallet.get_address(), 300)
token_contract.distribute_tokens(retailer_wallet.get_address(), 200)

# Print initial balances
print("Initial Balances:")
print(f"Supplier: {token_contract.get_balance(supplier_wallet.get_address())}")
print(f"Carrier: {token_contract.get_balance(carrier_wallet.get_address())}")
print(f"Retailer: {token_contract.get_balance(retailer_wallet.get_address())}")

# XML data for Order Placement
order_placement_xml = f"""
<order>
  <orderId>123456</orderId>
  <customer>
    <firstName>John</firstName>
    <lastName>Doe</lastName>
    <contactNo>9876543210</contactNo>
    <email>john.doe@example.com</email>
  </customer>
  <address>
    <city>New York</city>
    <state>New York</state>
    <zip>10001</zip>
  </address>
  <product>
    <productId>789</productId>
    <productName>Laptop</productName>
    <quantity>10</quantity>
  </product>
  <walletAddress>{get_wallet_address(supplier_wallet.public_key)}</walletAddress>
  <emissionsData>
    <carbonDioxide>50 kg</carbonDioxide>
    <nitrogenOxide>2 kg</nitrogenOxide>
  </emissionsData>
</order>
"""

# XML data for Packing
packing_xml = f"""
<shipment>
  <order>
    <orderId>123456</orderId>
    <customer>
      <firstName>John</firstName>
      <lastName>Doe</lastName>
      <contactNo>9876543210</contactNo>
      <email>john.doe@example.com</email>
    </customer>
    <address>
      <city>New York</city>
      <state>New York</state>
      <zip>10001</zip>
    </address>
    <product>
      <productId>789</productId>
      <productName>Laptop</productName>
      <quantity>10</quantity>
    </product>
    <walletAddress>{get_wallet_address(carrier_wallet.public_key)}</walletAddress>
    <routeOptimization>
      <optimalRoute>Route ABC</optimalRoute>
      <estimatedArrival>2023-12-31 12:00 PM</estimatedArrival>
    </routeOptimization>
    <energyConsumption>
      <vehicle>Transporter X</vehicle>
      <consumption>120 kWh</consumption>
    </energyConsumption>
    <emissionsData>
      <carbonDioxide>50 kg</carbonDioxide>
      <nitrogenOxide>2 kg</nitrogenOxide>
    </emissionsData>
  </order>
</shipment>
"""

# XML data for Transport
transport_xml = f"""
<transport>
  <orderId>123456</orderId>
  <carrier>
    <carrierName>XYZ Logistics</carrierName>
    <contactNo>123-456-7890</contactNo>
    <driver>
      <driverName>Mike Johnson</driverName>
      <contactNo>987-654-3210</contactNo>
    </driver>
  </carrier>
  <walletAddress>{get_wallet_address(retailer_wallet.public_key)}</walletAddress>
  <route>
    <origin>New York, NY</origin>
    <destination>Los Angeles, CA</destination>
    <estimatedArrival>2023-12-31 15:00</estimatedArrival>
  </route>
  <co2Consumption>
    <emissionsDuringTransport>25 kg</emissionsDuringTransport>
  </co2Consumption>
</transport>
"""
# Create a dynamic wallet list for easy management
wallets = [
    (supplier_wallet, "Supplier"),
    (carrier_wallet, "Carrier"),
    (retailer_wallet, "Retailer"),
]

# Token transfer during each stage
print("\nToken Transfers:")
try:
    # Supplier pays the carrier for transport
    token_contract.transfer_tokens(
        from_addr=supplier_wallet.get_address(),
        to=carrier_wallet.get_address(),
        amount=50
    )
    print("Supplier paid Carrier 50 tokens for transport services.")

    # Carrier pays the retailer
    token_contract.transfer_tokens(
        from_addr=carrier_wallet.get_address(),
        to=retailer_wallet.get_address(),
        amount=30
    )
    print("Carrier paid Retailer 30 tokens for delivery.")
except ValueError as e:
    print(f"Error during token transfer: {e}")
    
# Adding the XML transactions to the blockchain after validation
if validate_and_parse_xml(order_placement_xml):
    blockchain.add_new_transaction(order_placement_xml)
else:
    print("Order Placement XML is invalid.")

if validate_and_parse_xml(packing_xml):
    blockchain.add_new_transaction(packing_xml)
else:
    print("Packing XML is invalid.")

if validate_and_parse_xml(transport_xml):
    blockchain.add_new_transaction(transport_xml)
else:
    print("Transport XML is invalid.")


# Simulate IoT data for emissions
iot_data = simulate_iot_data()
blockchain.add_new_transaction(iot_data)

# Mining a block to include the transactions
blockchain.mine()

# Function to display transactions from the blockchain
def display_transactions(blockchain, token_contract=None, wallets=None):
    for block_index, block in enumerate(blockchain.chain):
        print(f"Block {block_index}:")
        for transaction_index, transaction in enumerate(block.transactions):
            print(f"  Transaction {transaction_index + 1}:\n{transaction}")
    if token_contract and wallets:
        print("\nFinal Wallet Balances:")
        for wallet, owner in wallets:
            print(f"{owner}: {token_contract.get_balance(wallet.get_address())} tokens")

# Calling the function to display the transactions
display_transactions(blockchain, token_contract, wallets)
