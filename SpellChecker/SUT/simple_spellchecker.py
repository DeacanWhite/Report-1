"""
Simplified wrapper for testing the pyspellchecker known() method.
Original source: https://github.com/barrust/pyspellchecker
"""

from spellchecker import SpellChecker

class SimpleSpellChecker:
    """Wrapper class for testing known() method"""
    
    def __init__(self):
        """Initialize with English dictionary"""
        self.spell = SpellChecker(language='en')
    
    def known(self, words):
        """
        Return the subset of words that appear in the dictionary.
        
        Args:
            words (list): List of words to check
            
        Returns:
            set: Set of words that are in the dictionary
        """
        return self.spell.known(words)
    
    def get_dictionary_size(self):
        """Return number of words in dictionary"""
        return self.spell.word_frequency.unique_words


# Test the function manually
if __name__ == "__main__":
    checker = SimpleSpellChecker()
    
    # Test with some words
    test_words = ["hello", "world", "asdfgh", "python"]
    result = checker.known(test_words)
    
    print(f"Input: {test_words}")
    print(f"Known words: {result}")
    print(f"Dictionary size: {checker.get_dictionary_size()}")