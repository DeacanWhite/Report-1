"""Mutant 16: Use upper() instead of lower()"""
from spellchecker import SpellChecker
import typing
from spellchecker.utils import KeyT, ensure_unicode

class MutantSpellChecker(SpellChecker):
    def known(self, words: typing.Iterable[KeyT]) -> typing.Set[str]:
        """The subset of `words` that appear in the dictionary of words"""
        tmp_words = [ensure_unicode(w) for w in words]
        # MUTATION: Changed .lower() to .upper()
        tmp = [w if self._case_sensitive else w.upper() for w in tmp_words]
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}
