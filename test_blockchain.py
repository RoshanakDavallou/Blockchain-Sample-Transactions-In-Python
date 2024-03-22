import unittest
from blockchain import SupplyChainBlockchain

class TestSupplyChainBlockchain(unittest.TestCase):

    def setUp(self):
        # Initialize the SupplyChainBlockchain before each test
        self.blockchain = SupplyChainBlockchain()

    def test_block_creation(self):
        # Test the creation of a new block
        block = self.blockchain.new_block(previous_hash='abc')
        self.assertTrue(isinstance(block, dict))
        self.assertEqual(block['index'], 2)
        self.assertEqual(block['previous_hash'], 'abc')

    def test_genesis_block(self):
        # Test the creation of the genesis block
        genesis_block = self.blockchain.chain[0]
        self.assertEqual(genesis_block['index'], 1)
        self.assertEqual(genesis_block['previous_hash'], '1')

    def test_new_transaction(self):
        # Test adding a new transaction
        self.blockchain.new_transaction("ORD123", "Order Placement", "Product ABC, Quantity: 100")
        self.assertEqual(len(self.blockchain.current_transactions), 1)

    def test_mining(self):
        # Test mining a new block with no transactions to ensure index increments
        last_block_index = self.blockchain.last_block['index']
        self.blockchain.new_block(previous_hash=self.blockchain.hash(self.blockchain.last_block))
        self.assertEqual(self.blockchain.last_block['index'], last_block_index + 1)

    def test_hash_static_method(self):
        # Test the static method hash
        new_block = self.blockchain.new_block(previous_hash='abc')
        block_hash = SupplyChainBlockchain.hash(new_block)
        self.assertEqual(block_hash, self.blockchain.hash(new_block))
        self.assertTrue(isinstance(block_hash, str))

if __name__ == '__main__':
    unittest.main()
