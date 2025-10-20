"""Mutant 14: Return input without dictionary check"""
from spellchecker import SpellChecker
import typing
from spellchecker.utils import KeyT, ensure_unicode

class MutantSpellChecker(SpellChecker):
    def known(self, words: typing.Iterable[KeyT]) -> typing.Set[str]:
        """The subset of `words` that appear in the dictionary of words"""
        tmp_words = [ensure_unicode(w) for w in words]
        tmp = [w if self._case_sensitive else w.lower() for w in tmp_words]
        # MUTATION: Return all tmp without checking dictionary
        return set(tmp) if self._check_if_should_check(list(tmp)[0] if tmp else '') else set()
