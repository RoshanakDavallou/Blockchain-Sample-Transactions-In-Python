# Creating Supply Chain Blockchain

This thesis project explores the application of blockchain technology to create a transparent and secure record of transactions within a supply chain.
The custom `SupplyChainBlockchain` class, implemented in Python, facilitates the tracking of goods from order placement through to delivery.

# Objectives
- To demonstrate how blockchain can improve transparency in supply chain management.
- To provide a proof-of-concept for tracking items through various stages of a supply chain.

# Implementation
The project includes a Python-based blockchain that allows for:
- Creation of blocks to represent transactions.
- Addition of transactions with timestamps and relevant supply chain data.
- A proof-of-work algorithm to validate new blocks.

# Features
- `new_block()`: Method to create a new block in the chain.
- `new_transaction()`: Method to add a new transaction to the list of transactions to be included in the next mined block.
- `hash()`: Static method to create a SHA-256 hash of a block.
- `proof_of_work()`: Method that implements the proof-of-work algorithm to validate the mining of a new block.

How to Use
To interact with the blockchain, instantiate the SupplyChainBlockchain class and use its methods to add transactions and mine new blocks.

Adding a Transaction
blockchain.new_transaction(order_id="ORD123", action="Order Placement", details="Product ABC, Quantity: 100")

Mining a Block
blockchain.new_block(previous_hash=blockchain.hash(blockchain.last_block))

Running the Tests
Ensuring the integrity of the blockchain functionality by running the unit tests provided in the test_blockchain.py file.

python -m unittest test_blockchain.py


License
This project is licensed under the MIT License - see the LICENSE file for details.


Project developed by Roshanak Davallou as part of the thesis work for Supply chain management and Logistics at Jacobs University Bremen.
