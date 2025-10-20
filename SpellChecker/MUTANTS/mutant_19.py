"""Mutant 19: Remove list comprehension result"""
from spellchecker import SpellChecker
import typing
from spellchecker.utils import KeyT, ensure_unicode

class MutantSpellChecker(SpellChecker):
    def known(self, words: typing.Iterable[KeyT]) -> typing.Set[str]:
        """The subset of `words` that appear in the dictionary of words"""
        tmp_words = [ensure_unicode(w) for w in words]
        # MUTATION: Use tmp_words directly
        tmp = tmp_words
        return {w for w in tmp if w in self._word_frequency.dictionary and self._check_if_should_check(w)}
