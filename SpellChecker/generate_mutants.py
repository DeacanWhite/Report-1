"""
Generate 30 mutants for the known() method
"""

mutant_template = '''"""Mutant {num:02d}: {description}"""
from spellchecker import SpellChecker
import typing
from spellchecker.utils import KeyT, ensure_unicode

class MutantSpellChecker(SpellChecker):
    def known(self, words: typing.Iterable[KeyT]) -> typing.Set[str]:
        """The subset of `words` that appear in the dictionary of words"""
{code}
'''

mutations = [
    # (mutant_num, description, code)
    (1, "Change AND to OR", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Changed 'and' to 'or'
        return {w for w in tmp if w in self._word_frequency.dictionary or self._check_if_should_check(w)}"""),
    
    (2, "Remove .lower()", """        tmp_words = [ensure_unicode(w) for w in words]
        # MUTATION: Removed .lower()
        tmp = [w if self._case_sensitive else w for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (3, "Remove check_if_should_check", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Removed self._check_if_should_check(w)
        return {w for w in tmp if w in self._word_frequency.dictionary}"""),
    
    (4, "Change 'in' to 'not in'", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Changed 'w in' to 'w not in'
        return {w for w in tmp if w not in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (5, "Negate case_sensitive", """        tmp_words = [ensure_unicode(w) for w in words]
        # MUTATION: Added 'not' before self._case_sensitive
        tmp = [w if not self._case_sensitive else w.lower() for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (6, "Remove ensure_unicode from comprehension", """        # MUTATION: Removed ensure_unicode
        tmp_words = [w for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (7, "Return empty set", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Always return empty set
        return set()"""),
    
    (8, "Return all words", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Return all input words
        return set(tmp)"""),
    
    (9, "Flip case branches", """        tmp_words = [ensure_unicode(w) for w in words]
        # MUTATION: Swapped if/else branches
        tmp = [w.lower() if self._case_sensitive else w for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (10, "Remove dictionary check", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Removed dictionary check
        return {w for w in tmp if self._check_if_should_check(w)}"""),
    
    (11, "Empty tmp_words", """        # MUTATION: Set to empty list
        tmp_words = []
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (12, "Empty tmp", """        tmp_words = [ensure_unicode(w) for w in words]
        # MUTATION: Set to empty list
        tmp = []
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (13, "Return first valid word", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Return only first valid word (deterministic)
        result = {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}
        for w in tmp:  # Check in original order
            if w in result:
                return {w}
        return set()"""),
    
    (14, "Return input without dictionary check", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Return all tmp without checking dictionary
        return set(tmp) if self._check_if_should_check(list(tmp)[0] if tmp else '') else set()"""),
    
    (15, "Reverse all conditions", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Reversed conditions
        return {w for w in tmp if w not in self._word_frequency.dictionary and not self._check_if_should_check(w)}"""),
    
    (16, "Use upper() instead of lower()", """        tmp_words = [ensure_unicode(w) for w in words]
        # MUTATION: Changed .lower() to .upper()
        tmp = [w if self._case_sensitive else w.upper() for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (17, "Change AND to OR (variant)", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Changed to OR with negations
        return {w for w in tmp if w not in self._word_frequency.dictionary or not self._check_if_should_check(w)}"""),
    
    (18, "Skip first word", """        # MUTATION: Skip first word
        tmp_words = [ensure_unicode(w) for w in words][1:]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (19, "Remove list comprehension result", """        tmp_words = [ensure_unicode(w) for w in words]
        # MUTATION: Use tmp_words directly
        tmp = tmp_words
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (20, "Add length check", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Added len(w) > 0 check
        return {w for w in tmp if len(w) > 0 and w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (21, "Process only first half of words", """        # MUTATION: Only process first half
        tmp_words = [ensure_unicode(w) for w in words]
        half = len(tmp_words) // 2
        tmp_words = tmp_words[:half] if half > 0 else tmp_words
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (22, "Always use lower", """        tmp_words = [ensure_unicode(w) for w in words]
        # MUTATION: Always use .lower() regardless of case_sensitive
        tmp = [w.lower() for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (23, "Return list instead of set", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Return list instead of set (will cause error)
        return [w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)]"""),
    
    (24, "Add extra length condition", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Added len(w) > 2 condition
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w) and len(w) > 2}"""),
    
    (25, "Filter in comprehension", """        # MUTATION: Added filter
        tmp_words = [ensure_unicode(w) for w in words if w]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (26, "Check dictionary membership with wrong condition", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Check if word length is in dictionary instead of word itself
        return {w for w in tmp if len(w) in self._word_frequency.dictionary and self._check_if_should_check(w)}"""),
    
    (27, "Add empty string to result", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Add empty string
        result = {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}
        result.add('')
        return result"""),
    
    (28, "Change to False", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Added 'and False'
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w) and False}"""),
    
    (29, "Return tmp as set", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Ignore dictionary check, return all
        return set(tmp)"""),
    
    (30, "Check opposite", """        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Return words NOT in dictionary
        return {w for w in tmp if w not in self._word_frequency.dictionary}"""),
]

# Generate all mutant files
for num, description, code in mutations:
    filename = f"MUTANTS/mutant_{num:02d}.py"
    content = mutant_template.format(num=num, description=description, code=code)
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"Created {filename}")

print("\n✓ All 30 mutants generated successfully!")