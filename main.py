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

## Initialization ##

# User analysis
DICTIONARY = user_analyzer.dictionary_parser(
    './language_data/user_dictionary.txt')

LEXICON = user_analyzer.lexicon_generator(
    './language_data/user_grammar.txt', DICTIONARY)
# Text analysis
LANGUAGE_DATA = text_analyzer.language_data_loader()


def job_analyzer(job_json):
    """
    It takes a job as an input and returns an analysis.
    """
    analysis = dict()
    # Get 'profile' and 'health_related'
    analysis['profile'] = user_analyzer.user_analyzer(job_json['user_description'],
                                                      LEXICON)[1]

    # Identified medical sources will be tagged as health related
    analysis['health_related'] = analysis['profile'] != '<unknown source>'

    # Get a 'solution'
    analysis['solution'] = text_analyzer.analyzer(job_json['message'],
                                                  LANGUAGE_DATA['start_words'],
                                                  LANGUAGE_DATA['grammar'],
                                                  LANGUAGE_DATA['stop_words'])[0]
    # Get a 'problem'
    analysis['problem'] = text_analyzer.analyzer(job_json['message'],
                                                 LANGUAGE_DATA['start_words'],
                                                 LANGUAGE_DATA['grammar'],
                                                 LANGUAGE_DATA['stop_words'])[1]

    # Save the analysis timestamp
    analysis['created_at'] = datetime.now().isoformat()
    return json.dumps(analysis)


if __name__ == "__main__":
    # Test the job_analyzer using corpus data
    CORPUS = open(
        './corpus/heart_disease_cholesterol_hypertension_diabetes_obesity.json', 'r').readlines()

    for line in CORPUS:
        print(job_analyzer(json.loads(line.rstrip())))
