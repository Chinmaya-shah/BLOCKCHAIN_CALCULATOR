import sys
from blockchain import BlockchainCalculator, Transaction

def print_blockchain(calculator):
    print("\n" + "="*50)
    print("                CURRENT BLOCKCHAIN STATE               ")
    print("="*50)
    for block in calculator.chain:
        print(f"\n[Block {block.index}]")
        print(f"  Timestamp : {block.timestamp}")
        print(f"  Prev Hash : {block.previous_hash}")
        print(f"  Hash      : {block.hash}")
        print(f"  Nonce     : {block.nonce}")
        print(f"  Calculated Value: {block.state_value}")
        print("  Transactions:")
        for tx in block.transactions:
            print(f"    - {tx}")
    print("="*50 + "\n")

def main():
    print("Initializing Blockchain Calculator (Difficulty = 4)...")
    calc = BlockchainCalculator(difficulty=4)
    
    # Check initial status
    print(f"Initial State Value: {calc.state_value}")
    
    # Block 1 transactions: basic arithmetic
    print("\n--- Queueing Block 1 Transactions ---")
    calc.add_transaction("ADD", 50, "Initial deposit/seed")
    calc.add_transaction("SUBTRACT", 15, "Purchase hardware")
    calc.add_transaction("MULTIPLY", 2, "Double investments")
    
    # Mine Block 1
    calc.mine_pending_transactions()
    
    # Block 2 transactions: advanced math & division
    print("\n--- Queueing Block 2 Transactions ---")
    calc.add_transaction("DIVIDE", 5, "Distribute shares")
    calc.add_transaction("ADD", 2.5, "Interest earned")
    
    # Mine Block 2
    calc.mine_pending_transactions()

    # Print the current chain structure
    print_blockchain(calc)

    # Validate the blockchain integrity
    print(f"Is Blockchain Valid? {calc.is_chain_valid()}")
    
    # Demonstration of Tampering / Mutation detection
    print("\n--- Simulating Malicious Data Mutation (Tampering) ---")
    # A hacker tries to change the operand of the transaction in Block 1
    # Change "Purchase hardware (-15)" to "Purchase hardware (-5)" to steal 10 units
    hacked_block = calc.chain[1]
    original_operand = hacked_block.transactions[1].operand
    hacked_block.transactions[1].operand = 5.0
    print(f"Altered Block 1 transaction to SUBTRACT 5 instead of {original_operand}")
    
    # Re-validate chain
    valid = calc.is_chain_valid()
    print(f"Is Blockchain Valid after tampering? {valid}")
    
    if not valid:
        print("SUCCESS: Blockchain integrity check detected data tampering!")
        
        # Restore to original value
        hacked_block.transactions[1].operand = original_operand
        print("Restored original block transactions.")
        print(f"Is Blockchain Valid after restoration? {calc.is_chain_valid()}")
    else:
        print("WARNING: Tampering went undetected! (This shouldn't happen)")

if __name__ == "__main__":
    main()
