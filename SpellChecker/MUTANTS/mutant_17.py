"""Mutant 17: Change AND to OR (variant)"""
from spellchecker import SpellChecker
import typing
from spellchecker.utils import KeyT, ensure_unicode

class MutantSpellChecker(SpellChecker):
    def known(self, words: typing.Iterable[KeyT]) -> typing.Set[str]:
        """The subset of `words` that appear in the dictionary of words"""
        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Changed to OR with negations
        return {w for w in tmp if w not in self._word_frequency.dictionary or not self._check_if_should_check(w)}
