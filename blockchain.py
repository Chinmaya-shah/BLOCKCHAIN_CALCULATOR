import hashlib
import time
import json

class Transaction:
    """
    Represents a mathematical operation (transaction) on the blockchain.
    Supported operations: 'ADD', 'SUBTRACT', 'MULTIPLY', 'DIVIDE', 'SET'
    """
    def __init__(self, operation, operand, description=""):
        self.operation = operation.upper()
        self.operand = float(operand)
        self.description = description
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "operation": self.operation,
            "operand": self.operand,
            "description": self.description,
            "timestamp": self.timestamp
        }

    def __str__(self):
        op_symbols = {"ADD": "+", "SUBTRACT": "-", "MULTIPLY": "*", "DIVIDE": "/", "SET": "="}
        symbol = op_symbols.get(self.operation, "?")
        return f"{symbol} {self.operand} ({self.description})"


class Block:
    """
    Represents a single block in the blockchain.
    Contains transaction list, index, proof (nonce), previous hash, and state.
    """
    def __init__(self, index, transactions, previous_hash, state_value):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.state_value = state_value  # Running total/result at this block
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Convert block data to a serialized JSON string for hashing
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "state_value": self.state_value
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined successfully! Nonce: {self.nonce}, Hash: {self.hash}")


class BlockchainCalculator:
    """
    The main Blockchain Calculator class.
    Manages the chain, transaction pool, difficulty, and running state.
    """
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
        self.state_value = 0.0  # The initial calculator total
        
        # Create the genesis block
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_tx = Transaction("SET", 0.0, "Genesis initialization")
        genesis_block = Block(
            index=0,
            transactions=[genesis_tx],
            previous_hash="0",
            state_value=0.0
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, operation, operand, description=""):
        if operation.upper() not in ["ADD", "SUBTRACT", "MULTIPLY", "DIVIDE", "SET"]:
            raise ValueError(f"Invalid operation: {operation}")
        
        tx = Transaction(operation, operand, description)
        self.pending_transactions.append(tx)
        print(f"Added pending transaction: {tx}")
        return tx

    def calculate_next_state(self, current_state, transactions):
        state = current_state
        for tx in transactions:
            if tx.operation == "ADD":
                state += tx.operand
            elif tx.operation == "SUBTRACT":
                state -= tx.operand
            elif tx.operation == "MULTIPLY":
                state *= tx.operand
            elif tx.operation == "DIVIDE":
                if tx.operand == 0:
                    print("Warning: Division by zero attempted! Value remains unchanged.")
                else:
                    state /= tx.operand
            elif tx.operation == "SET":
                state = tx.operand
        return state

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            print("No pending transactions to mine.")
            return False

        latest_block = self.get_latest_block()
        
        # Calculate new state value based on the pending operations
        new_state = self.calculate_next_state(latest_block.state_value, self.pending_transactions)
        
        new_block = Block(
            index=latest_block.index + 1,
            transactions=self.pending_transactions,
            previous_hash=latest_block.hash,
            state_value=new_state
        )
        
        print(f"Mining block {new_block.index} with {len(self.pending_transactions)} transactions...")
        new_block.mine_block(self.difficulty)
        
        self.chain.append(new_block)
        self.state_value = new_state
        self.pending_transactions = []  # Clear pending transaction pool
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # 1. Check if hash matches block data recalculation
            if current_block.hash != current_block.calculate_hash():
                print(f"Validation Error: Block {i} data has been mutated!")
                return False

            # 2. Check if block links correctly to previous hash
            if current_block.previous_hash != previous_block.hash:
                print(f"Validation Error: Block {i} previous hash link is broken!")
                return False

            # 3. Check if Proof of Work target is satisfied
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"Validation Error: Block {i} proof of work is invalid!")
                return False

            # 4. Validate that states match transactions step-by-step
            recalculated_state = self.calculate_next_state(previous_block.state_value, current_block.transactions)
            if abs(current_block.state_value - recalculated_state) > 1e-9:
                print(f"Validation Error: State value mismatch at Block {i}! Expected {recalculated_state}, found {current_block.state_value}")
                return False

        return True
