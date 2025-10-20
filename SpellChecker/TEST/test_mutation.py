"""
Mutation Testing for pyspellchecker
Tests each mutant against all metamorphic test groups (MR1, MR2, MR3, MR4)
WITH INDIVIDUAL MR ANALYSIS
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
    (['apple', 'apple', 'banana'], ['banana', 'apple', 'apple'])
]

MR2_TEST_CASES = [
    (['hello', 'world', 'test'], ['hello', 'world', 'test', 'asdfgh']),
    (['cat', 'dog'], ['cat', 'dog', 'xyz123']),
    (['python', 'java'], ['python', 'java', 'qqqq']),
    (['apple'], ['apple', 'zzzzz']),
    (['the', 'quick', 'brown'], ['the', 'quick', 'brown', 'xjkdf']),
    (['I', 'a', 'to'], ['I', 'a', 'to', 'xyz']),
    (['hello', 'world'], ['hello', 'world', 'xyzabc', 'qwerty', 'asdfzxcv'])
]

MR3_TEST_CASES = [
    (['Hello', 'World'], ['hello', 'world']),
    (['PYTHON', 'java'], ['python', 'JAVA']),
    (['Test', 'CODE'], ['test', 'code']),
    (['Apple', 'BANANA'], ['APPLE', 'banana']),
    (['The', 'QUICK', 'brown'], ['THE', 'quick', 'BROWN']),
    (['A', 'I'], ['a', 'i']),
    (['THE', 'and'], ['the', 'AND'])
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

def test_mutant_with_mr(mutant_num, mr_name):
    """Test a single mutant against a specific MR"""
    mutant_module = f"mutant_{mutant_num:02d}"
    
    try:
        # Import the mutant
        sys.path.insert(0, '../MUTANTS')
        module = importlib.import_module(mutant_module)
        MutantChecker = module.MutantSpellChecker
        
        checker = MutantChecker(language='en')
        violations = []
        
        if mr_name == 'MR1':
            # Test MR1: Permutation Invariance
            for i, (si, fi) in enumerate(MR1_TEST_CASES, 1):
                try:
                    so = checker.known(si)
                    fo = checker.known(fi)
                    
                    if so != fo:
                        violations.append(f"MG{i}")
                except Exception as e:
                    violations.append(f"MG{i} (Error)")
        
        elif mr_name == 'MR2':
            # Test MR2: Unknown Addition
            for i, (si, fi) in enumerate(MR2_TEST_CASES, 1):
                try:
                    so = checker.known(si)
                    fo = checker.known(fi)
                    
                    if fo != so:
                        violations.append(f"MG{i}")
                except Exception as e:
                    violations.append(f"MG{i} (Error)")
        
        elif mr_name == 'MR3':
            # Test MR3: Case Invariance
            for i, (si, fi) in enumerate(MR3_TEST_CASES, 1):
                try:
                    so = checker.known(si)
                    fo = checker.known(fi)
                    
                    # Normalize to lowercase for comparison
                    so_norm = {w.lower() for w in so}
                    fo_norm = {w.lower() for w in fo}
                    
                    if so_norm != fo_norm:
                        violations.append(f"MG{i}")
                except Exception as e:
                    violations.append(f"MG{i} (Error)")
        
        elif mr_name == 'MR4':
            # Test MR4: Non-Empty Property
            for i, words in enumerate(MR4_TEST_CASES, 1):
                try:
                    output = checker.known(words)
                    
                    # Output should be non-empty AND should not contain invalid content
                    if len(output) == 0 or '' in output:
                        violations.append(f"MG{i}")
                except Exception as e:
                    violations.append(f"MG{i} (Error)")
        
        # Clean up
        if '../MUTANTS' in sys.path:
            sys.path.remove('../MUTANTS')
        if mutant_module in sys.modules:
            del sys.modules[mutant_module]
        
        killed = len(violations) > 0
        return killed, violations
        
    except Exception as e:
        print(f"  Error loading mutant: {e}")
        if '../MUTANTS' in sys.path:
            sys.path.remove('../MUTANTS')
        return False, []

def run_mutation_testing():
    """Run mutation testing on all 30 mutants with MR-specific analysis"""
    print("=" * 80)
    print("MUTATION TESTING WITH METAMORPHIC RELATIONS")
    print("=" * 80)
    print(f"Testing 30 mutants against MR1, MR2, MR3, MR4")
    print(f"Test groups per MR: {len(MR1_TEST_CASES)} (MR1), {len(MR2_TEST_CASES)} (MR2), {len(MR3_TEST_CASES)} (MR3), {len(MR4_TEST_CASES)} (MR4)")
    print()
    
    # Store results by MR
    mr_results = {
        'MR1': {'killed': [], 'survived': [], 'violations': {}},
        'MR2': {'killed': [], 'survived': [], 'violations': {}},
        'MR3': {'killed': [], 'survived': [], 'violations': {}},
        'MR4': {'killed': [], 'survived': [], 'violations': {}}
    }
    
    # Test each mutant against each MR
    print("-" * 80)
    print("TESTING MUTANTS AGAINST EACH MR")
    print("-" * 80)
    
    for i in range(1, 31):
        print(f"\n[Mutant {i:02d}]")
        
        for mr_name in ['MR1', 'MR2', 'MR3', 'MR4']:
            killed, violations = test_mutant_with_mr(i, mr_name)
            
            mutant_id = f"mutant_{i:02d}"
            
            if killed:
                mr_results[mr_name]['killed'].append(mutant_id)
                status = "KILLED"
                symbol = "✗"
            else:
                mr_results[mr_name]['survived'].append(mutant_id)
                status = "SURVIVED"
                symbol = "○"
            
            mr_results[mr_name]['violations'][mutant_id] = violations
            
            total_tests = len(MR1_TEST_CASES) if mr_name == 'MR1' else len(MR2_TEST_CASES) if mr_name == 'MR2' else len(MR3_TEST_CASES) if mr_name == 'MR3' else len(MR4_TEST_CASES)
            violation_rate = (len(violations) / total_tests * 100) if total_tests > 0 else 0
            
            print(f"  {symbol} {mr_name}: {status:8s} ({len(violations)}/{total_tests} violations, {violation_rate:.1f}%)")
    
    # Print summary results
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    
    print("\n1. MUTATION SCORES BY METAMORPHIC RELATION")
    print("-" * 80)
    
    for mr_name in ['MR1', 'MR2', 'MR3', 'MR4']:
        killed_count = len(mr_results[mr_name]['killed'])
        survived_count = len(mr_results[mr_name]['survived'])
        mutation_score = (killed_count / 30) * 100
        
        # Calculate average violation rate
        total_violations = sum(len(v) for v in mr_results[mr_name]['violations'].values())
        total_tests = len(MR1_TEST_CASES) if mr_name == 'MR1' else len(MR2_TEST_CASES) if mr_name == 'MR2' else len(MR3_TEST_CASES) if mr_name == 'MR3' else len(MR4_TEST_CASES)
        avg_violation_rate = (total_violations / (30 * total_tests)) * 100
        
        print(f"\n{mr_name} (Permutation Invariance):" if mr_name == 'MR1' else 
              f"\n{mr_name} (Unknown Addition):" if mr_name == 'MR2' else
              f"\n{mr_name} (Case Invariance):" if mr_name == 'MR3' else
              f"\n{mr_name} (Non-Empty Property):")
        print(f"  Killed:              {killed_count}/30 ({mutation_score:.2f}%)")
        print(f"  Survived:            {survived_count}/30 ({100-mutation_score:.2f}%)")
        print(f"  Avg Violation Rate:  {avg_violation_rate:.2f}%")
        print(f"  Mutation Score:      {mutation_score:.2f}%")
    
    # Combined effectiveness
    print("\n2. COMBINED EFFECTIVENESS")
    print("-" * 80)
    
    all_killed = set()
    for mr_name in mr_results:
        all_killed.update(mr_results[mr_name]['killed'])
    
    combined_killed = len(all_killed)
    combined_score = (combined_killed / 30) * 100
    
    print(f"\nMutants killed by AT LEAST ONE MR: {combined_killed}/30 ({combined_score:.2f}%)")
    
    # Find mutants that survived all MRs
    all_mutants = set(f"mutant_{i:02d}" for i in range(1, 31))
    survived_all = all_mutants - all_killed
    
    print(f"Mutants that SURVIVED ALL MRs:     {len(survived_all)}/30 ({(len(survived_all)/30)*100:.2f}%)")
    if survived_all:
        survived_ids = ', '.join([m.split('_')[1] for m in sorted(survived_all)])
        print(f"  IDs: {survived_ids}")
    
    # Detailed analysis
    print("\n3. DETAILED MUTANT ANALYSIS")
    print("-" * 80)
    
    # Find mutants killed by all MRs
    killed_by_all = set(mr_results['MR1']['killed'])
    for mr_name in ['MR2', 'MR3', 'MR4']:
        killed_by_all &= set(mr_results[mr_name]['killed'])
    
    print(f"\nMutants killed by ALL MRs: {len(killed_by_all)}/30")
    if killed_by_all:
        killed_ids = ', '.join([m.split('_')[1] for m in sorted(killed_by_all)])
        print(f"  IDs: {killed_ids}")
    
    # Find mutants killed by only one MR
    print()
    for mr_name in ['MR1', 'MR2', 'MR3', 'MR4']:
        only_this_mr = set(mr_results[mr_name]['killed'])
        for other_mr in ['MR1', 'MR2', 'MR3', 'MR4']:
            if other_mr != mr_name:
                only_this_mr -= set(mr_results[other_mr]['killed'])
        
        if only_this_mr:
            only_ids = ', '.join([m.split('_')[1] for m in sorted(only_this_mr)])
            print(f"Mutants killed ONLY by {mr_name}: {len(only_this_mr)}")
            print(f"  IDs: {only_ids}")
    
    # Generate comparison table
    print("\n4. COMPARISON TABLE")
    print("-" * 80)
    print(f"\n{'MR':<10} {'Killed':<15} {'Survived':<15} {'Mutation Score':<20}")
    print("-" * 80)
    
    for mr_name in ['MR1', 'MR2', 'MR3', 'MR4']:
        killed_count = len(mr_results[mr_name]['killed'])
        survived_count = len(mr_results[mr_name]['survived'])
        mutation_score = (killed_count / 30) * 100
        print(f"{mr_name:<10} {f'{killed_count}/30':<15} {f'{survived_count}/30':<15} {mutation_score:.2f}%")
    
    print("-" * 80)
    print(f"{'COMBINED':<10} {f'{combined_killed}/30':<15} {f'{len(survived_all)}/30':<15} {combined_score:.2f}%")
    print("=" * 80)
    
    # Save detailed results to file
    with open('mutation_test_results.txt', 'w') as f:
        f.write("MUTATION TESTING RESULTS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("INDIVIDUAL MR RESULTS:\n")
        f.write("-" * 80 + "\n")
        for mr_name in ['MR1', 'MR2', 'MR3', 'MR4']:
            f.write(f"\n{mr_name}:\n")
            f.write(f"  Mutation Score: {(len(mr_results[mr_name]['killed'])/30)*100:.2f}%\n")
            f.write(f"  Killed ({len(mr_results[mr_name]['killed'])}): ")
            f.write(', '.join([m.split('_')[1] for m in sorted(mr_results[mr_name]['killed'])]) + "\n")
            f.write(f"  Survived ({len(mr_results[mr_name]['survived'])}): ")
            f.write(', '.join([m.split('_')[1] for m in sorted(mr_results[mr_name]['survived'])]) + "\n")
        
        f.write(f"\nCOMBINED RESULTS:\n")
        f.write(f"  Mutation Score: {combined_score:.2f}%\n")
        f.write(f"  Killed by at least one MR: {combined_killed}/30\n")
        f.write(f"  Survived all MRs: {len(survived_all)}/30\n")
        if survived_all:
            f.write(f"    IDs: {', '.join([m.split('_')[1] for m in sorted(survived_all)])}\n")
        
        f.write("\nDETAILED MUTANT RESULTS:\n")
        f.write("-" * 80 + "\n")
        for i in range(1, 31):
            mutant_id = f"mutant_{i:02d}"
            f.write(f"\nMutant {i:02d}:\n")
            for mr_name in ['MR1', 'MR2', 'MR3', 'MR4']:
                status = "KILLED" if mutant_id in mr_results[mr_name]['killed'] else "SURVIVED"
                violations = mr_results[mr_name]['violations'].get(mutant_id, [])
                f.write(f"  {mr_name}: {status:8s} - Violations: {len(violations)} {violations}\n")
    
    print("\nResults saved to 'mutation_test_results.txt'")
    
    return mr_results, combined_score

if __name__ == "__main__":
    results, score = run_mutation_testing()