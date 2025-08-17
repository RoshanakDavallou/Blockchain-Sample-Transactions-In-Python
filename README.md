# A Demo case of Supply Chain Blockchain in Python

This project demonstrates how blockchain technology can be applied to improve transparency, traceability, and accountability across supply chain processes. Implemented in Python, the system models transaction tracking from order placement to final delivery, integrating concepts such as Digital Product Passports (DPP), IoT-based emissions monitoring, and tokenized incentive mechanisms.

# Objectives
- Improve supply chain **visibility and trust** using blockchain.
- Enable secure tracking of goods across all process stages.
- Simulate **real-time environmental data** via IoT sensors.
- Demonstrate token-driven incentives for supply chain actors.


## Key Components
<img width="600" height="500" alt="435461738-2c4c633b-cda8-4b55-89fb-22da007f8352" src="https://github.com/user-attachments/assets/dd36e9d8-5c67-484a-8f02-9252b9cc88b8" />


### Blockchain Logic

- `add_new_transaction(xml_transaction)`: Adds an XML-formatted transaction to the queue.
- `mine()`: Mines a new block containing unconfirmed transactions.
- `compute_hash()`: Generates a SHA-256 hash for a block.
- `proof_of_work(block)`: Validates block creation via a proof-of-work algorithm (4 leading zeroes).

### Digital Wallets

- Each participant (e.g., Supplier, Carrier, Retailer) receives a unique wallet.
- Tokens are used to reward or pay for services, managed by a smart contract.

### IoT Emissions Data

- Simulated **IoT devices** generate CO₂ and NOₓ emissions data.
- Environmental data is permanently recorded in the blockchain.

### Digital Product Passport (DPP)

- Tracks the full lifecycle of a product.
- Stores manufacturing, transportation, and emissions data.
- Ensures accountability at every stage.

## Use Cases

| Use Case                  | Description |
|---------------------------|-------------|
| **Raw Material Tracking** | Monitor emissions during sourcing. |
| **Packaging & Transport** | Log CO₂/NOₓ data during shipment. |
| **Smart Incentives**      | Trigger tokens for eco-compliance. |
| **End-of-Life**           | Enable recycling and transparency. |    
---

## Security & Interoperability

- Ensures **data immutability** and **blockchain validation**.
- Encourages **interoperability** with other platforms and devices.
- Includes unit tests to validate core blockchain and token logic.


## Advanced Concepts (Optional for Expansion)

- Predictive analytics using AI/ML on emissions data.
- Front-end integration for user-friendly blockchain access.
- External hardware integration (e.g., RFID, real-time sensors).


## How to Use

### 1. Add a Transaction
```python
blockchain.add_new_transaction(xml_transaction_data)
```
### 2. Mine a Block
```python
blockchain.mine()
```
### 3. Run Unit Tests
```python
python -m unittest test_blockchain.py
```
**Note:** You can replace `xml_transaction` with your actual XML string, or link it with real-time sensor data (e.g., RFID). This project is structured to support autonomous and transparent interactions between IoT devices and a secure blockchain ledger.

## Testing & Validation
Unit tests are included in test_blockchain.py to validate:

Token transactions

Block mining

XML storage

Tamper protection


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

The Project is developed by Roshanak Davallou as part of the thesis work for Smart Supply Chain Management and Logistics at Constructor University Bremen.
