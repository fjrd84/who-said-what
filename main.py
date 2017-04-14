#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
main.py

NLP engine demo
"""

# Libraries
# import sys
import json
from datetime import datetime
from engines import user_analyzer
from engines import text_analyzer

# Initialization
DICTIONARY = user_analyzer.dictionary_parser('./language_data/user_dictionary.txt')
LEXICON = user_analyzer.lexicon_generator('./language_data/user_grammar.txt', DICTIONARY)

def demo(external_input):
    """
    Start the demo
    """
    # Language sources:

    language_data = text_analyzer.language_data_loader()

    input_data = json.loads(external_input)
    output_data = dict()
    # Get 'profile' and 'health_related'
    output_data['profile'] = user_analyzer.user_analyzer(
        input_data['user_description'], LEXICON)[1]
    if output_data['profile'] != '<unknown source>':
        output_data['health_related'] = True
    else:
        output_data['health_related'] = False
    # Get 'solution'
    output_data['solution'] = text_analyzer.analyzer(
        input_data['message'], language_data['start_words'],
        language_data['grammar'], language_data['stop_words'])[0]
    # Get 'problem'
    output_data['problem'] = text_analyzer.analyzer(
        input_data['message'], language_data['start_words'],
        language_data['grammar'], language_data['stop_words'])[1]
    # Get 'date'
    output_data['created_at'] = str(datetime.now())
    return json.dumps(output_data)


if __name__ == "__main__":
    # Testing demo in corpus:
    CORPUS = open(
        './corpus/heart_disease_cholesterol_hypertension_diabetes_obesity.json', 'r').readlines()
    for line in CORPUS:
        line = line.rstrip()
        print(demo(line))
