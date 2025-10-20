"""Mutant 21: Process only first half of words"""
from spellchecker import SpellChecker
import typing
from spellchecker.utils import KeyT, ensure_unicode

class MutantSpellChecker(SpellChecker):
    def known(self, words: typing.Iterable[KeyT]) -> typing.Set[str]:
        """The subset of `words` that appear in the dictionary of words"""
        # MUTATION: Only process first half
        tmp_words = [ensure_unicode(w) for w in words]
        half = len(tmp_words) // 2
        tmp_words = tmp_words[:half] if half > 0 else tmp_words
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}
