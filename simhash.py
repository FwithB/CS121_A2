import os
import string
import hashlib

def tokenize(text):
    """
    Tokenize the given text by splitting on whitespace and punctuation.
    """
    return [word.strip(string.punctuation) for word in text.lower().split()]

def shingle(text, k):
    """
    Create k-shingles from the given text.
    """
    tokens = tokenize(text)
    return set(' '.join(tokens[i:i+k]) for i in range(len(tokens)-k+1))

def hash_shingles(shingles):
    """
    Hash each shingle to a 64-bit integer.
    """
    hashes = []
    for shingle in shingles:
        # Use MD5 to generate a hash value for the shingle
        hash_value = int(hashlib.md5(shingle.encode('utf-8')).hexdigest(), 16)
        
        # Split the 128-bit hash value into two 64-bit values
        hash1 = hash_value >> 64
        hash2 = hash_value & (2**64-1)
        
        hashes.append((hash1, hash2))
    
    return hashes

def simhash(shingles, hash_bits=64):
    """
    Compute the SimHash of the given set of shingles.
    """
    # Initialize the hash counts to 0
    hash_counts = [0] * hash_bits
    
    # Hash each shingle to a 64-bit integer
    hashes = hash_shingles(shingles)
    
    # Compute the hash count for each bit in the hash values
    for hash1, hash2 in hashes:
        for i in range(hash_bits):
            if (hash1 >> i) & 1:
                hash_counts[i] += 1
            else:
                hash_counts[i] -= 1
            if (hash2 >> i) & 1:
                hash_counts[i] += 1
            else:
                hash_counts[i] -= 1
    
    # Convert the hash counts to a bit vector
    simhash = 0
    for i in range(hash_bits):
        if hash_counts[i] >= 0:
            simhash |= 1 << i
    
    return simhash

def hamming_distance(simhash1, simhash2):
    """
    Compute the Hamming distance between two SimHash values.
    """
    return bin(simhash1 ^ simhash2).count('1')

def process_hash(text,k):
    """
    Compare the similarity between two files using SimHashing.
    """
    
    # Create k-shingles from the texts
    shingles = shingle(text, k)
    
    # Compute the SimHash values for each set of shingles
    simhash1 = simhash(shingles)

    return simhash1

def compare(simhash1,simhash2,threshold):
    # Compute the Hamming distance between the SimHash values
    distance = hamming_distance(simhash1, simhash2)
    
    # Normalize the distance to be between 0 and 1
    similarity = 1 - distance / 64
    
    # Return True if the similarity is above the threshold, False otherwise
    return similarity>=threshold

# Example usage

#k = 5 # Use 5-shingles
#threshold = 0.5 #
