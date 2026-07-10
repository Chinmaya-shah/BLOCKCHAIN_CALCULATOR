# 🧮 Blockchain Calculator

An educational, proof-of-concept blockchain implementation where blocks record mathematical operations (transactions) rather than financial transfers. It maintains a running state (the "accumulator" total) across blocks, securing transactions using cryptographic hashing, Proof of Work (PoW) consensus, and full state verification.

---

## 🚀 Features

-   **Cryptographic Ledger**: Uses SHA-256 to hash block contents and verify integrity.
-   **Immutable Chain Links**: Blocks reference the previous block's hash, forming an unbreakable cryptographic chain.
-   **Proof of Work Consensus**: Mining uses variable difficulty matching prefix-zeros in the mined block's hash.
-   **State Machine Accumulator**: Each block evaluates mathematical operations (`ADD`, `SUBTRACT`, `MULTIPLY`, `DIVIDE`, `SET`) to update the running state total securely.
-   **Tamper Resistance Demonstration**: Built-in verification logic simulates block modification and proves how the network immediately detects and rejects corrupted blocks.

---

## 📁 Repository Structure

```
├── blockchain.py      # Core block, transaction, and chain class definitions
├── main.py            # CLI entry point demonstrating execution & tampering detection
└── requirements.txt   # Project dependency file (uses Python standard libraries)
```

---

## 🛠️ Getting Started

### Prerequisites

-   **Python 3.6+** (no external packages required, uses standard libraries only).

### Running the Project

1. Clone this repository to your local machine (if not already cloned).
2. Run the main demonstration file:
   ```bash
   python main.py
   ```

---

## 🧬 How It Works

### Mathematical Transactions
Each transaction is an operations packet. For example:
- `ADD 50`
- `SUBTRACT 15`
- `MULTIPLY 2`

### Mining & Block Linking
When pending operations are mined:
1. The new accumulator state is calculated starting from the previous block's final state value.
2. The block computes its cryptographic hash using its contents (index, previous hash, timestamp, transaction logs, current state, and nonce).
3. The mining algorithm increments the nonce until a hash with `difficulty` number of leading zeros is found:
   $$\text{Hash} = \text{SHA256}(\text{Index} \parallel \text{Prev\_Hash} \parallel \text{Transactions} \parallel \text{State} \parallel \text{Nonce}) < \text{Target}$$
4. The block is appended to the chain.

### Integrity & Validation Loop
The integrity function checks the entire chain sequentially:
- Recalculates block hashes to check for data mutations.
- Confirms the `previous_hash` pointers match.
- Verifies that block states accurately match the mathematical operations sequence starting from the genesis block.
