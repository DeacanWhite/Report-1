# debug.py
import sys
sys.path.insert(0, '../SUT')
from simple_spellchecker import SimpleSpellChecker

checker = SimpleSpellChecker()

# Check what the actual behavior is
print("Test 1:", checker.known(['Hello', 'World']))
print("Test 2:", checker.known(['hello', 'world']))
print("Test 3:", checker.known(['hello', 'xyzabc']))