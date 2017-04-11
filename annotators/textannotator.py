#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The following program is for populating language resources based on a corpus annotation iterative process.
# The program annotate text messages about diseases, for feeding the following resources:
# (1) grammar.txt, (2) stop_words.txt, (3) start_words.txt

# Load text_analyzer module
import sys
from text_analyzer import *

# Load corpus to annotate
corpusf_path = './corpus/'
corpusf_name = raw_input('\nCorpus file name: ')

# The corpus is stored in a list (lowercase)
corpusf = open(corpusf_path + corpusf_name, 'r')
corpus = []
for l in corpusf:
    l = l.rstrip()
    l = l.lower()
    if l not in corpus:
        corpus.append(l)
corpusf.close()

# Function to annotate loaded corpus. It returns a dictionary with
# positive (annotated) and negative (non-annotated) messages


def create_annotated_corpus(corpus):
    # language_data stores language resources to analyze text messages
    language_data = language_data_loader()
    annotated_corpus = dict()
    annotated_corpus['positive'] = []
    annotated_corpus['negative'] = []
    cnt = 0
    print '\nAnnotating ', len(corpus), ' left...', '\n'
    for l in corpus:
        cnt = cnt + 1
        analysis_result = analyzer(
            l, language_data['start_words'], language_data['grammar'], language_data['stop_words'])
        if analysis_result != '<nothing found>':
            positive_analysis = []
            positive_analysis.append(analysis_result[0])
            positive_analysis.append(analysis_result[1])
            positive_analysis.append(analysis_result[2])
            positive_analysis.append(l)
            annotated_corpus['positive'].append(positive_analysis)
        else:
            annotated_corpus['negative'].append(l)
    return annotated_corpus

# The annotation process consists of steps. In each step we can pass over
# the message (and delete it from corpus), or try modifications on it if
# we do not agree with the resulting analysis


def annotation_step(message):
    try_or_go = raw_input('(t)ry / (g)o ? ')
    launch_create_annotated_corpus = False
    while try_or_go == 't':
        language_data = language_data_loader()
        analysis_result = analyzer(
            message, language_data['start_words'], language_data['grammar'], language_data['stop_words'])
        if analysis_result != '<nothing found>':
            testing_message = message.replace(
                analysis_result[0], ' [ ' + analysis_result[0] + ' ] ')
            testing_message = testing_message.replace(
                analysis_result[1], '< ' + analysis_result[1] + ' >')
            print '\n'
            print testing_message, ' | ', analysis_result[2]
            print '\n'
            launch_create_annotated_corpus = True
            try_or_go = raw_input('(t)ry / (g)o ? ')
        else:
            print '\n'
            print message, ' | ', '<no annotations>'
            print '\n'
            launch_create_annotated_corpus = True
            try_or_go = raw_input('(t)ry / (g)o ? ')
    else:
        corpus.remove(message)
    return launch_create_annotated_corpus

# This function starts the whole annotation process, and calls the latter
# on each step


def annotation_process():
    annotated_corpus = create_annotated_corpus(corpus)
    while len(corpus) > 0:
        while len(annotated_corpus['negative']) > 0:
            for message in annotated_corpus['negative']:
                print '\n'
                print message
                print '\n'
                if annotation_step(message) is True:
                    annotated_corpus = create_annotated_corpus(corpus)
                    break
                else:
                    if annotated_corpus['negative'].index(message) != -1:
                        annotated_corpus['negative'].remove(message)
                        continue
                    else:
                        annotated_corpus['negative'].remove(message)
                        break
        else:
            for positive_item in annotated_corpus['positive']:
                testing_message = positive_item[3].replace(
                    positive_item[0], ' [ ' + positive_item[0] + ' ] ')
                testing_message = testing_message.replace(
                    positive_item[1], '< ' + positive_item[1] + ' >')
                print '\n'
                print testing_message, ' | ', positive_item[2]
                print '\n'
                if annotation_step(positive_item[3]) is True:
                    annotated_corpus = create_annotated_corpus(corpus)
                    break
                else:
                    if annotated_corpus['positive'].index(positive_item) != -1:
                        annotated_corpus['positive'].remove(positive_item)
                        continue
                    else:
                        annotated_corpus['positive'].remove(positive_item)
                        break
    else:
        print '\n' + '*** No more messages ***' + '\n'
        quit()


annotation_process()
