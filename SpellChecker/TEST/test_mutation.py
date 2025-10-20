"""
Mutation Testing for pyspellchecker
Tests each mutant against all metamorphic test groups (MR1, MR2, MR3, MR4)
"""

import sys
import importlib
import os

# Test cases from MR testing
MR1_TEST_CASES = [
    (['cat', 'dog', 'bird'], ['dog', 'bird', 'cat']),
    (['hello', 'world'], ['world', 'hello']),
    (['test', 'python', 'code'], ['code', 'test', 'python']),
    (['apple', 'banana'], ['banana', 'apple']),
    (['one', 'two', 'three', 'four'], ['three', 'one', 'four', 'two']),
    (['a', 'I', 'to'], ['to', 'I', 'a']),
]

MR2_TEST_CASES = [
    (['hello', 'world', 'test'], ['hello', 'world', 'test', 'asdfgh']),
    (['cat', 'dog'], ['cat', 'dog', 'xyz123']),
    (['python', 'java'], ['python', 'java', 'qqqq']),
    (['apple'], ['apple', 'zzzzz']),
    (['the', 'quick', 'brown'], ['the', 'quick', 'brown', 'xjkdf']),
    (['I', 'a', 'to'], ['I', 'a', 'to', 'xyz']),
]

MR3_TEST_CASES = [
    (['Hello', 'World'], ['hello', 'world']),
    (['PYTHON', 'java'], ['python', 'JAVA']),
    (['Test', 'CODE'], ['test', 'code']),
    (['Apple', 'BANANA'], ['APPLE', 'banana']),
    (['The', 'QUICK', 'brown'], ['THE', 'quick', 'BROWN']),
    (['A', 'I'], ['a', 'i']),
]

MR4_TEST_CASES = [
    ['hello', 'xyzabc'],
    ['xyzabc', 'world'],
    ['qqqq', 'test', 'zzzzz'],
    ['python'], 
    ['asdfgh', 'the', 'jklqw'],
    ['a', 'xyzabc'],
    ['I', 'qqqq'],
]

def test_mutant(mutant_num):
    """Test a single mutant against all MRs"""
    mutant_module = f"mutant_{mutant_num:02d}"
    
    try:
        # Import the mutant
        sys.path.insert(0, '../MUTANTS')
        module = importlib.import_module(mutant_module)
        MutantChecker = module.MutantSpellChecker
        
        checker = MutantChecker(language='en')
        killed = False
        violations = []
        
        # Test MR1: Permutation Invariance
        for i, (si, fi) in enumerate(MR1_TEST_CASES, 1):
            try:
                so = checker.known(si)
                fo = checker.known(fi)
                
                if so != fo:
                    killed = True
                    violations.append(f"MR1_MG{i}")
            except Exception as e:
                killed = True
                violations.append(f"MR1_MG{i} (Error: {str(e)})")
        
        # Test MR2: Unknown Addition
        for i, (si, fi) in enumerate(MR2_TEST_CASES, 1):
            try:
                so = checker.known(si)
                fo = checker.known(fi)
                
                if fo != so:
                    killed = True
                    violations.append(f"MR2_MG{i}")
            except Exception as e:
                killed = True
                violations.append(f"MR2_MG{i} (Error: {str(e)})")
        
        # Test MR3: Case Invariance
        for i, (si, fi) in enumerate(MR3_TEST_CASES, 1):
            try:
                so = checker.known(si)
                fo = checker.known(fi)
                
                # Normalize to lowercase for comparison
                so_norm = {w.lower() for w in so}
                fo_norm = {w.lower() for w in fo}
                
                if so_norm != fo_norm:
                    killed = True
                    violations.append(f"MR3_MG{i}")
            except Exception as e:
                killed = True
                violations.append(f"MR3_MG{i} (Error: {str(e)})")
        
        # Test MR4: Non-Empty Property
        for i, words in enumerate(MR4_TEST_CASES, 1):
            try:
                output = checker.known(words)
                
                # Output should be non-empty AND should not contain invalid content
                if len(output) == 0 or '' in output:
                    killed = True
                    violations.append(f"MR4_MG{i}")
            except Exception as e:
                killed = True
                violations.append(f"MR4_MG{i} (Error: {str(e)})")
        
        # Clean up
        sys.path.remove('../MUTANTS')
        del sys.modules[mutant_module]
        
        return killed, violations
        
    except Exception as e:
        print(f"  Error loading mutant: {e}")
        return False, []

def run_mutation_testing():
    """Run mutation testing on all 30 mutants"""
    print("=" * 70)
    print("MUTATION TESTING - pyspellchecker known() method")
    print("Testing with MR1, MR2, MR3, MR4")
    print("=" * 70)
    
    results = {}
    killed_count = 0
    
    for i in range(1, 31):
        print(f"\nTesting Mutant {i:02d}...", end=" ")
        killed, violations = test_mutant(i)
        
        results[i] = {
            'killed': killed,
            'violations': violations
        }
        
        if killed:
            print(f"✗ KILLED by {len(violations)} test(s): {', '.join(violations[:3])}")
            killed_count += 1
        else:
            print("✓ SURVIVED")
    
    # Calculate mutation score
    mutation_score = killed_count / 30
    
    print("\n" + "=" * 70)
    print("MUTATION TESTING RESULTS")
    print("=" * 70)
    print(f"Total Mutants: 30")
    print(f"Killed: {killed_count}")
    print(f"Survived: {30 - killed_count}")
    print(f"Mutation Score: {mutation_score:.2%}")
    print("=" * 70)
    
    # Detailed results
    print("\nDETAILED RESULTS:")
    for i in range(1, 31):
        status = "KILLED" if results[i]['killed'] else "SURVIVED"
        violations_str = ', '.join(results[i]['violations'][:3]) if results[i]['violations'] else 'None'
        print(f"Mutant {i:02d}: {status:10s} - Violations: {len(results[i]['violations'])} ({violations_str})")
    
    return results, mutation_score

if __name__ == "__main__":
    results, score = run_mutation_testing()