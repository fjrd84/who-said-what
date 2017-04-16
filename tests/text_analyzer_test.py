#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Text analyzer tests.
"""
from engines import text_analyzer

START_WORDS_PATH = './tests/demo_start_words.txt'
STOP_WORDS_PATH = './tests/demo_stop_words.txt'
GRAMMAR_PATH = './tests/demo_grammar.txt'


def test_file_parser():
    """
    File parser tests.
    """
    start_words = text_analyzer.file_parser(START_WORDS_PATH, True)
    assert 'negativity' in start_words
    assert 'pci' in start_words
    assert r'acute \w+' in start_words
    assert 'eczema' in start_words
    assert 'wrinkles' in start_words
    assert 'yeast infections' in start_words
    assert 'wrinkless' not in start_words
    assert 'invented_word' not in start_words


def test_language_data_loader():
    """
    Language data loader tests
    """
    language_data = text_analyzer.language_data_loader(
        GRAMMAR_PATH,
        START_WORDS_PATH,
        STOP_WORDS_PATH)
    assert 'eczema' in language_data['start_words']
    assert '^@\\w+$' in language_data['stop_words']
    assert '[s] \\w+ed to (healthier|better)( \\S+){0,7} [p]' in language_data['grammar']
    assert r'[s] effective( \w+){0,2} (in|for|to)( \w+){0,5} [p]' in language_data['grammar']
