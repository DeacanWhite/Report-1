"""Mutant 26: Use words directly"""
from spellchecker import SpellChecker
import typing
from spellchecker.utils import KeyT, ensure_unicode

class MutantSpellChecker(SpellChecker):
    def known(self, words: typing.Iterable[KeyT]) -> typing.Set[str]:
        """The subset of `words` that appear in the dictionary of words"""
        # MUTATION: Skip tmp_words creation
        tmp = [w if self._case_sensitive else ensure_unicode(w).lower() for w in words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}
