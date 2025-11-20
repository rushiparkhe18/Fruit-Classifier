import hashlib
import json
from datetime import datetime
import os

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self):
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

class Blockchain:
    def __init__(self, storage_file='blockchain_data.json'):
        self.storage_file = storage_file
        self.chain = []
        self.load_chain()
        
        # Create genesis block if chain is empty
        if len(self.chain) == 0:
            self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, datetime.now().isoformat(), {
            'type': 'genesis',
            'message': 'Fruit Freshness Blockchain Initialized'
        }, '0')
        self.chain.append(genesis_block)
        self.save_chain()
    
    def get_latest_block(self):
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_block(self, data):
        """Add a new block to the chain"""
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=datetime.now().isoformat(),
            data=data,
            previous_hash=latest_block.hash
        )
        self.chain.append(new_block)
        self.save_chain()
        return new_block
    
    def is_chain_valid(self):
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def save_chain(self):
        """Save blockchain to file"""
        chain_data = [block.to_dict() for block in self.chain]
        with open(self.storage_file, 'w') as f:
            json.dump(chain_data, f, indent=2)
    
    def load_chain(self):
        """Load blockchain from file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    chain_data = json.load(f)
                    self.chain = []
                    for block_data in chain_data:
                        block = Block(
                            block_data['index'],
                            block_data['timestamp'],
                            block_data['data'],
                            block_data['previous_hash']
                        )
                        self.chain.append(block)
            except Exception as e:
                print(f"Error loading blockchain: {e}")
                self.chain = []
    
    def get_chain(self):
        """Get the entire blockchain as a list of dictionaries"""
        return [block.to_dict() for block in self.chain]
    
    def get_recent_records(self, limit=10):
        """Get the most recent records from the blockchain"""
        records = [block.to_dict() for block in self.chain if block.data.get('type') == 'freshness_check']
        return records[-limit:][::-1]  # Return last N records in reverse order
