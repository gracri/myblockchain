import hashlib
import json
from time import time

class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.currentTransactions = []
        self.nodes = set()

        #create genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.currentTransactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.currentTransactions = []
        self.chain.append(block)

        return block

    # Adds a new transaction to the list of transactions
    def new_transaction(self, sender, recipient, amount):
        """

        Creates a new transaction to go into the next mined block.

        :param sender: <str> Address of the sender

        :param recipient: <str> Address of the recipient

        :param amount: <int> amount

        :return: <int> index of the block that holds the transaction

        """

        self.currentTransactions.append({

            'sender': sender,

            'recipient': recipient,

            'amount': amount,

        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        # Returns the last block in the chain.

        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block.

        :param block: <dict> block
        :return: <str> hash of the block.
        """

        # Make sure the dictionary is Ordered, otherwise we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple proof of work algorithm
        - find a number 'p' such that hash(pp') contains last 4 leading zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        :param last_block: last block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)
        proof = 0

        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof