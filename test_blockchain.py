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
        self.blockchain.add_new_transaction("<sample>XML transaction</sample>")
        initial_length = len(self.blockchain.chain)
        self.blockchain.mine()
        self.assertEqual(len(self.blockchain.chain), initial_length + 1)
        new_block = self.blockchain.last_block
        self.assertTrue(isinstance(new_block, Block))
        self.assertEqual(new_block.index, initial_length)

    def test_genesis_block(self):
        genesis_block = self.blockchain.chain[0]
        self.assertEqual(genesis_block.index, 0)
        self.assertEqual(genesis_block.previous_hash, '0')

    def test_new_transaction(self):
        initial_length = len(self.blockchain.unconfirmed_transactions)
        self.blockchain.add_new_transaction("<sample>XML transaction</sample>")
        self.assertEqual(len(self.blockchain.unconfirmed_transactions), initial_length + 1)

    def test_mining(self):
        self.blockchain.add_new_transaction("<sample>XML transaction</sample>")
        last_block_index = self.blockchain.last_block.index
        self.blockchain.mine()
        self.assertEqual(self.blockchain.last_block.index, last_block_index + 1)

    def test_proof_of_work(self):
        last_block = self.blockchain.last_block
        new_block = Block(
            index=last_block.index + 1,
            transactions=["<sample>XML transaction</sample>"],
            timestamp=time.time(),
            previous_hash=last_block.hash
        )
        proof = self.blockchain.proof_of_work(new_block)
        self.assertTrue(self.blockchain.is_valid_proof(new_block, proof))
        self.assertTrue(proof.startswith('0000'))

    def test_token_transfer(self):
        initial_balance_supplier = self.token_contract.get_balance(self.supplier_wallet.get_address())
        initial_balance_carrier = self.token_contract.get_balance(self.carrier_wallet.get_address())
        self.token_contract.transfer_tokens(
            from_addr=self.supplier_wallet.get_address(),
            to=self.carrier_wallet.get_address(),
            amount=50
        )
        self.assertEqual(self.token_contract.get_balance(self.supplier_wallet.get_address()), initial_balance_supplier - 50)
        self.assertEqual(self.token_contract.get_balance(self.carrier_wallet.get_address()), initial_balance_carrier + 50)

    def test_overspending_tokens(self):
        with self.assertRaises(ValueError):
            self.token_contract.transfer_tokens(
                from_addr=self.supplier_wallet.get_address(),
                to=self.carrier_wallet.get_address(),
                amount=10000  # exceeds balance
            )

    def test_invalid_block_hash(self):
        self.blockchain.add_new_transaction("<data>Test</data>")
        tampered_block = Block(
            index=self.blockchain.last_block.index + 1,
            transactions=["<data>Fake</data>"],
            timestamp=time.time(),
            previous_hash="wrong_hash"
        )
        fake_proof = tampered_block.compute_hash()
        result = self.blockchain.add_block(tampered_block, fake_proof)
        self.assertFalse(result)

    def test_invalid_xml_transaction(self):
        corrupt_xml = "<order><brokenTag>"
        self.blockchain.add_new_transaction(corrupt_xml)
        self.blockchain.mine()
        last_block = self.blockchain.last_block
        self.assertIn(corrupt_xml, last_block.transactions)

    def test_wallet_creation(self):
        wallet_1 = DigitalWallet("TestUser1")
        wallet_2 = DigitalWallet("TestUser2")
        self.assertNotEqual(wallet_1.get_address(), wallet_2.get_address())

if __name__ == '__main__':
    unittest.main()
