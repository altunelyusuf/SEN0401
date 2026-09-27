import hashlib
import time

class Block:
    """
    Represents a single block in our blockchain.
    """
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculates the hash of the block using its contents.
        The hash is a unique fingerprint of the block's data.
        """
        block_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the Block.
        """
        return f"Block(#{self.index}, Data: '{self.data}', Hash: {self.hash[:10]}..., Prev_Hash: {self.previous_hash[:10]}...)"


class Blockchain:
    """
    Manages the chain of blocks, including adding new blocks and validating integrity.
    """
    def __init__(self):
        # The chain is initialized with a "Genesis Block"
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """
        Creates the very first block in the chain, manually.
        This block has no previous hash.
        """
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        """
        Returns the most recent block in the chain.
        """
        return self.chain[-1]

    def add_block(self, new_block_data):
        """
        Creates and adds a new block to the chain.
        """
        latest_block = self.get_latest_block()
        new_block = Block(index=latest_block.index + 1,
                          data=new_block_data,
                          previous_hash=latest_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self, chain_to_validate):
        """
        Validates the integrity of the blockchain.
        Returns a tuple: (is_valid, index_of_break)
        """
        # 1. Check if the Genesis Block is correct
        if chain_to_validate[0].index != 0 or \
           chain_to_validate[0].data != "Genesis Block" or \
           chain_to_validate[0].previous_hash != "0":
            return (False, 0)
        
        # 2. Iterate through the rest of the chain
        for i in range(1, len(chain_to_validate)):
            current_block = chain_to_validate[i]
            previous_block = chain_to_validate[i - 1]

            # 2a. Check if the block's hash is still valid for its content
            if current_block.hash != current_block.calculate_hash():
                print(f"\n[!] Tampering detected in Block #{current_block.index}. Data doesn't match hash.")
                return (False, current_block.index)

            # 2b. Check if the block points correctly to the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                print(f"\n[!] Chain link broken at Block #{current_block.index}.")
                print(f"    Block #{previous_block.index}'s hash is {previous_block.hash[:10]}...")
                print(f"    But Block #{current_block.index} points to {current_block.previous_hash[:10]}...")
                return (False, current_block.index)
        
        return (True, None)


def print_chain(blockchain):
    """
    Prints the blockchain in a visually appealing way.
    """
    print("." * 80)
    for i, block in enumerate(blockchain.chain):
        is_genesis = "(Genesis Block)" if i == 0 else ""
        print(f"Block #{block.index} {is_genesis}")
        print(f"  ├─ Data: '{block.data}'")
        print(f"  ├─ Hash: {block.hash}")
        if i > 0:
            print(f"  └─ Previous Hash: {block.previous_hash}")
        else:
             print(f"  └─ Previous Hash: {block.previous_hash}")

        if i < len(blockchain.chain) - 1:
            print("         ^")
            print("         |  <-- Cryptographic Link")
            print("         |")
    print("." * 80)


def run_game():
    """
    Main function to run the "Break the Chain" game.
    """
    # 1. Setup the blockchain with some initial transactions
    my_chain = Blockchain()
    my_chain.add_block("Alice pays Bob 1 coin")
    my_chain.add_block("Bob pays Carol 2 coins")
    my_chain.add_block("Carol pays Dave 0.5 coins")

    print("=" * 80)
    print("      🔗 WELCOME TO THE 'BREAK THE CHAIN' CHALLENGE! 🔗")
    print("=" * 80)
    print("Here is the current, valid blockchain. Notice how each block's 'Previous Hash'")
    print("matches the 'Hash' of the block before it, creating a secure chain.")

    print_chain(my_chain)

    # 2. The Challenge: Ask the user to tamper with the chain
    print("\nNow, it's your turn to be the hacker! Let's try to alter a transaction.")
    
    while True:
        try:
            block_to_edit = int(input(f"Which block number would you like to tamper with? (1-{len(my_chain.chain) - 1}): "))
            if 1 <= block_to_edit < len(my_chain.chain):
                break
            else:
                print("Invalid block number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

    new_data = input(f"Enter the new transaction data for Block #{block_to_edit}: ")

    # 3. The Consequence: Alter the block's data
    print("\n[!] Tampering with the block...")
    my_chain.chain[block_to_edit].data = new_data
    print(f"    Success! Block #{block_to_edit}'s data has been changed to '{new_data}'.")
    print("    But wait... did that break the chain? Let's re-validate everything.")
    time.sleep(2)

    # 4. Visual Feedback: Re-validate the chain and show the result
    print("\n🔍 Re-validating the entire blockchain from scratch...")
    print("-" * 80)
    time.sleep(1)
    
    is_valid, break_point = my_chain.is_chain_valid(my_chain.chain)
    
    if is_valid:
        print("\n✅ Hmm, surprisingly the chain is still valid. This shouldn't happen in this demo.")
    else:
        print("\n" + "=" * 80)
        print("      ❌ CHAIN INVALID! YOU'VE BEEN CAUGHT! ❌")
        print("=" * 80)
        print("The cryptographic links are broken. Here's what happened:")
        print(f"1. You changed the data in Block #{break_point-1 if my_chain.chain[break_point].previous_hash != my_chain.chain[break_point-1].calculate_hash() else break_point}.")
        print(f"2. This changed its calculated hash.")
        print(f"3. The 'Previous Hash' stored in Block #{break_point} no longer matches the new, altered hash of Block #{break_point - 1}.")
        print("\nThis simple check proves the tampering. To make the chain valid again, you would")
        print("have to recalculate the hashes for ALL subsequent blocks... an impossible task")
        print("on a real, global network!")

    print("\nHere is the broken chain for you to inspect:")
    print_chain(my_chain)


if __name__ == '__main__':
    run_game()
