#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Text analyzer tests.
"""
from engines import text_analyzer


def test_file_parser():
    """
    File parser tests.
    """
    start_words = text_analyzer.file_parser('./tests/demo_start_words.txt', True)
    assert 'negativity' in start_words
    assert 'pci' in start_words
    assert r'acute \w+' in start_words
    assert 'eczema' in start_words
    assert 'wrinkles' in start_words
    assert 'yeast infections' in start_words
    assert 'wrinkless' not in start_words
    assert 'invented_word' not in start_words
