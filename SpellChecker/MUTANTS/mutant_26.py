"""Mutant 26: Check dictionary membership with wrong condition"""
from spellchecker import SpellChecker
import typing
from spellchecker.utils import KeyT, ensure_unicode

class MutantSpellChecker(SpellChecker):
    def known(self, words: typing.Iterable[KeyT]) -> typing.Set[str]:
        """The subset of `words` that appear in the dictionary of words"""
        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Check if word length is in dictionary instead of word itself
        return {w for w in tmp if len(w) in self._word_frequency.dictionary and self._check_if_should_check(w)}