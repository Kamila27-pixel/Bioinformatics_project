class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_pattern = False

class DNATrie:
   """
   A Trie specialized for genomic sequences (A, C, G, T).
   Provides O(m) search complexity where m is the length of the pattern.
   """
   def __init__(self):
       self.root = TrieNode()
       
   def insert(self, sequence):
       node = self.root
       for char in sequence.upper():
           if char not in node.children:
              node.children[char] = TrieNode()
           node = node.children[char]
       node.is_end_of_pattern = True

   def search(self, pattern):
       node = self.root
       for char in pattern.upper():
           if char not in node.children:
              return False
           node = node.children[char]
       return node.is_end_of_pattern
