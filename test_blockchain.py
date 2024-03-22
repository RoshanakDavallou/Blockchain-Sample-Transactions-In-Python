import unittest
import time
from blockchain import Block, Blockchain, DigitalWallet, TokenSmartContract

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        # Initialize the Blockchain and TokenSmartContract before each test
        self.blockchain = Blockchain()
        self.token_contract = TokenSmartContract(1000)
        self.supplier_wallet = DigitalWallet("Supplier")
        self.carrier_wallet = DigitalWallet("Carrier")
        self.retailer_wallet = DigitalWallet("Retailer")
        
        # Distribute tokens to wallets
        self.token_contract.distribute_tokens(self.supplier_wallet.get_address(), 500)
        self.token_contract.distribute_tokens(self.carrier_wallet.get_address(), 300)
        self.token_contract.distribute_tokens(self.retailer_wallet.get_address(), 200)

    def test_block_creation(self):
        # Test the addition and validation of a new block
        self.blockchain.add_new_transaction("<sample>XML transaction</sample>")
        initial_length = len(self.blockchain.chain)
        self.blockchain.mine()
        self.assertEqual(len(self.blockchain.chain), initial_length + 1)
        new_block = self.blockchain.last_block
        self.assertTrue(isinstance(new_block, Block))
        self.assertEqual(new_block.index, initial_length)

    def test_genesis_block(self):
        # Test the creation of the genesis block
        genesis_block = self.blockchain.chain[0]
        self.assertEqual(genesis_block.index, 0)
        self.assertEqual(genesis_block.previous_hash, '0')

    def test_new_transaction(self):
        # Test adding a new transaction
        initial_length = len(self.blockchain.unconfirmed_transactions)
        self.blockchain.add_new_transaction("<sample>XML transaction</sample>")
        self.assertEqual(len(self.blockchain.unconfirmed_transactions), initial_length + 1)

    def test_mining(self):
        # Test mining a new block with transactions
        self.blockchain.add_new_transaction("<sample>XML transaction</sample>")
        last_block_index = self.blockchain.last_block.index
        self.blockchain.mine()
        self.assertEqual(self.blockchain.last_block.index, last_block_index + 1)

    def test_proof_of_work(self):
        # Test the proof of work algorithm
        last_block = self.blockchain.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=["<sample>XML transaction</sample>"],
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.blockchain.proof_of_work(new_block)
        self.assertTrue(self.blockchain.is_valid_proof(new_block, proof))
        self.assertTrue(proof.startswith('0000'))

    def test_token_transfer(self):
        # Test token transfer between wallets
        initial_balance_supplier = self.token_contract.get_balance(self.supplier_wallet.get_address())
        initial_balance_carrier = self.token_contract.get_balance(self.carrier_wallet.get_address())
        self.token_contract.transfer_tokens(
            from_addr=self.supplier_wallet.get_address(),
            to=self.carrier_wallet.get_address(),
            amount=50
        )
        self.assertEqual(self.token_contract.get_balance(self.supplier_wallet.get_address()), initial_balance_supplier - 50)
        self.assertEqual(self.token_contract.get_balance(self.carrier_wallet.get_address()), initial_balance_carrier + 50)

    def test_wallet_creation(self):
        # Test wallet creation and address uniqueness
        wallet_1 = DigitalWallet("TestUser1")
        wallet_2 = DigitalWallet("TestUser2")
        self.assertNotEqual(wallet_1.get_address(), wallet_2.get_address())

if __name__ == '__main__':
    unittest.main()
