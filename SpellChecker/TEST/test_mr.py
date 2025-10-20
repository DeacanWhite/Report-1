"""
Metamorphic Testing for pyspellchecker known() method
"""

import sys
sys.path.insert(0, '../SUT')
from simple_spellchecker import SimpleSpellChecker

def test_mr1_permutation():
    """MR1: Permutation Invariance - Order doesn't matter"""
    checker = SimpleSpellChecker()
    
    test_cases = [
        (['cat', 'dog', 'bird'], ['dog', 'bird', 'cat']),
        (['hello', 'world'], ['world', 'hello']),
        (['test', 'python', 'code'], ['code', 'test', 'python']),
        (['apple', 'banana'], ['banana', 'apple']),
        (['one', 'two', 'three', 'four'], ['three', 'one', 'four', 'two']),
        (['a', 'I', 'to'], ['to', 'I', 'a']),
        (['apple', 'apple', 'banana'], ['banana', 'apple', 'apple'])
    ]
    
    print("\n=== MR1: Permutation Invariance Testing ===")
    passed = 0
    total = len(test_cases)
    
    for i, (si, fi) in enumerate(test_cases, 1):
        so = checker.known(si)
        fo = checker.known(fi)
        
        if so == fo:
            print(f"✓ MG1_{i}: PASS - SO == FO")
            passed += 1
        else:
            print(f"✗ MG1_{i}: FAIL - SO != FO")
            print(f"  SI: {si}, SO: {so}")
            print(f"  FI: {fi}, FO: {fo}")
    
    print(f"\nMR1 Results: {passed}/{total} passed")
    print(f"Violation Rate: {(total - passed) / total:.2%}")
    return passed == total

def test_mr2_unknown_addition():
    """MR2: Adding unknown word doesn't change known words"""
    checker = SimpleSpellChecker()
    
    test_cases = [
        (['hello', 'world', 'test'], ['hello', 'world', 'test', 'asdfgh']),
        (['cat', 'dog'], ['cat', 'dog', 'xyz123']),
        (['python', 'java'], ['python', 'java', 'qqqq']),
        (['apple'], ['apple', 'zzzzz']),
        (['the', 'quick', 'brown'], ['the', 'quick', 'brown', 'xjkdf']),
        (['I', 'a', 'to'], ['I', 'a', 'to', 'xyz']),
        (['hello', 'world'], ['hello', 'world', 'xyzabc', 'qwerty', 'asdfzxcv'])
    ]
    
    print("\n=== MR2: Unknown Word Addition Testing ===")
    passed = 0
    total = len(test_cases)
    
    for i, (si, fi) in enumerate(test_cases, 1):
        so = checker.known(si)
        fo = checker.known(fi)
        
        if fo == so:
            print(f"✓ MG2_{i}: PASS - FO == SO")
            passed += 1
        else:
            print(f"✗ MG2_{i}: FAIL - FO != SO")
            print(f"  SI: {si}, SO: {so}")
            print(f"  FI: {fi}, FO: {fo}")
    
    print(f"\nMR2 Results: {passed}/{total} passed")
    print(f"Violation Rate: {(total - passed) / total:.2%}")
    return passed == total

def test_mr3_case_invariance():
    """MR3: Case Invariance - Outputs normalized to lowercase should match"""
    checker = SimpleSpellChecker()
    
    test_cases = [
        (['Hello', 'World'], ['hello', 'world']),
        (['PYTHON', 'java'], ['python', 'JAVA']),
        (['Test', 'CODE'], ['test', 'code']),
        (['Apple', 'BANANA'], ['APPLE', 'banana']),
        (['The', 'QUICK', 'brown'], ['THE', 'quick', 'BROWN']),
        (['A', 'I'], ['a', 'i']),
        (['THE', 'and'], ['the', 'AND'])
    ]
    
    print("\n=== MR3: Case Invariance Testing ===")
    passed = 0
    total = len(test_cases)
    
    for i, (si, fi) in enumerate(test_cases, 1):
        so = checker.known(si)
        fo = checker.known(fi)
        
        # Both should return same result (program normalizes to lowercase)
        so_norm = {w.lower() for w in so}
        fo_norm = {w.lower() for w in fo}
        
        if so_norm == fo_norm:
            print(f"✓ MG3_{i}: PASS - SO == FO (normalized)")
            passed += 1
        else:
            print(f"✗ MG3_{i}: FAIL - SO != FO")
            print(f"  SI: {si}, SO: {so}")
            print(f"  FI: {fi}, FO: {fo}")
    
    print(f"\nMR3 Results: {passed}/{total} passed")
    print(f"Violation Rate: {(total - passed) / total:.2%}")
    return passed == total

def test_mr4_non_empty_property():
    """MR4: Non-Empty Property - Valid words must produce output"""
    checker = SimpleSpellChecker()
    
    test_cases = [
        ['hello', 'xyzabc'],
        ['xyzabc', 'world'],
        ['qqqq', 'test', 'zzzzz'],
        ['python'], 
        ['asdfgh', 'the', 'jklqw'],
        ['a', 'xyzabc'],
        ['I', 'qqqq'],
    ]
    
    print("\n=== MR4: Non-Empty Property Testing ===")
    passed = 0
    total = len(test_cases)
    
    for i, words in enumerate(test_cases, 1):
        output = checker.known(words)
        
        if len(output) > 0:
            print(f"✓ MG4_{i}: PASS - Output non-empty: {output}")
            passed += 1
        else:
            print(f"✗ MG4_{i}: FAIL - Output empty for {words}")
    
    print(f"\nMR4 Results: {passed}/{total} passed")
    print(f"Violation Rate: {(total - passed) / total:.2%}")
    return passed == total

if __name__ == "__main__":
    print("=" * 70)
    print("METAMORPHIC TESTING - pyspellchecker known() method")
    print("=" * 70)
    
    mr1_pass = test_mr1_permutation()
    mr2_pass = test_mr2_unknown_addition()
    mr3_pass = test_mr3_case_invariance()
    mr4_pass = test_mr4_non_empty_property()
    
    print("\n" + "=" * 70)
    print("OVERALL RESULTS:")
    print(f"MR1 (Permutation): {'PASS ✓' if mr1_pass else 'FAIL ✗'}")
    print(f"MR2 (Addition): {'PASS ✓' if mr2_pass else 'FAIL ✗'}")
    print(f"MR3 (Case Invariance): {'PASS ✓' if mr3_pass else 'FAIL ✗'}")
    print(f"MR4 (Non-Empty Property): {'PASS ✓' if mr4_pass else 'FAIL ✗'}")
    print("=" * 70)