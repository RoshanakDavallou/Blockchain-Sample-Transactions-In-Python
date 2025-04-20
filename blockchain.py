#creating a sample blockchain for 3 transactions (order placement, packing and transport) in supply chain. 
#Includes classes for Block, Blockchain, DigitalWallet, DigitalProductPassport, and TokenSmartContract.

import random
import hashlib
import time
import json
import rsa
import xml.etree.ElementTree as ET

class Block:
    """Represents a block in the blockchain."""
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        """Initialize a block with index, transactions, timestamp, previous hash, and nonce."""
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        """Computes the SHA-256 hash of the block's contents."""
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    """Implements a basic blockchain structure."""
    def __init__(self):
        """Initializes the blockchain with a genesis block."""
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Creates and appends the genesis block."""
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        """Returns the last block in the chain."""
        return self.chain[-1]

    def add_new_transaction(self, transaction):
        """Adds a new transaction to the unconfirmed list."""
        self.unconfirmed_transactions.append(transaction)

    def proof_of_work(self, block):
        """Performs proof of work algorithm for a given block."""
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0000'):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        """Validates and adds a block to the chain."""
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """Checks whether the proof of work is valid."""
        return (block_hash.startswith('0000') and block_hash == block.compute_hash())

    def mine(self):
        """Mines a new block with unconfirmed transactions."""
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

class DigitalWallet:
    """Represents a digital wallet with RSA key pair and balance."""
    def __init__(self, owner_name):
        """Initializes the wallet with a key pair and balance."""
        self.public_key, self.private_key = rsa.newkeys(2048)
        self.owner_name = owner_name
        self.balance = 0

    def get_address(self):
        """Returns the wallet's public key as address."""
        return self.public_key.save_pkcs1().decode()

    def add_tokens(self, amount):
        """Adds tokens to the wallet balance."""
        self.balance += amount

    def spend_tokens(self, amount):
        """Spends tokens from the wallet if balance is sufficient."""
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Insufficient balance")

class DigitalProductPassport:
    """Stores lifecycle data for a product."""
    def __init__(self, product_id, product_name):
        """Initializes product ID, name and data list."""
        self.product_id = product_id
        self.product_name = product_name
        self.lifecycle_data = []

    def add_data(self, stage, data):
        """Adds a lifecycle stage with data and timestamp."""
        self.lifecycle_data.append({
            "stage": stage,
            "data": data,
            "timestamp": time.time()
        })

    def get_passport(self):
        """Returns the full passport details."""
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "lifecycle_data": self.lifecycle_data
        }

    def to_json(self):
        """Returns a JSON string of the passport."""
        return json.dumps(self.get_passport(), indent=2)

    def __str__(self):
        return self.to_json()

class TokenSmartContract:
    """Handles token distribution and transfers."""
    def __init__(self, initial_supply):
        """Initializes total supply and wallet records."""
        self.total_supply = initial_supply
        self.wallets = {}

    def distribute_tokens(self, to, amount):
        """Distributes tokens to a wallet address."""
        if amount > self.total_supply:
            raise ValueError("Not enough tokens in supply")
        self.total_supply -= amount
        self.wallets[to] = self.wallets.get(to, 0) + amount

    def transfer_tokens(self, from_addr, to, amount):
        """Transfers tokens between wallets."""
        if self.wallets.get(from_addr, 0) < amount:
            raise ValueError("Not enough tokens")
        self.wallets[from_addr] -= amount
        self.wallets[to] = self.wallets.get(to, 0) + amount

    def get_balance(self, address):
        """Returns balance of the given wallet address."""
        return self.wallets.get(address, 0)

def simulate_iot_data():
    """Simulates IoT emissions data."""
    return {
        "carbonDioxide": f"{random.randint(20, 100)} kg",
        "nitrogenOxide": f"{random.randint(1, 5)} kg"
    }

def parse_xml_string(xml_string):
    """Parses XML string and returns root element."""
    return ET.fromstring(xml_string)

