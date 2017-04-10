#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The following program is for populating language resources based on a corpus annotation iterative process.
# The program annotate user description's texts, for feeding the following resources:
# (1) user_dictionary, (2) user_grammar

# Load user_analyzer module
import sys
sys.path.insert(0, '/Users/DoraDorita/Desktop/NLP/engines')
from user_analyzer import *

# Load corpus to annotate
corpusf_path = '/Users/DoraDorita/Desktop/NLP/corpus/'
corpusf_name = raw_input('\nCorpus file name: ')

# The corpus is stored in a list (lowercase)
corpusf = open(corpusf_path+corpusf_name, 'r')
corpus = []
for l in corpusf:
    l = l.rstrip()
    l = l.lower()
    if l not in corpus:
        corpus.append(l)
corpusf.close()

# Function to annotate loaded corpus. It returns a dictionary with positive (annotated) and negative (non-annotated) messages
def create_annotated_corpus(corpus):
    # language_data stores language resources to analyze users' descriptions
    generated_lexicon = lexicon_generator()
    annotated_corpus = dict()
    annotated_corpus['positive'] = []
    annotated_corpus['negative'] = []
    cnt = 0
    print '\nAnnotating ', len(corpus), ' left...', '\n'
    for l in corpus:
        cnt = cnt +1
        analysis_result = user_analyzer(l,generated_lexicon)
        if analysis_result[1] != '<unknown source>':
            positive_analysis = []
            positive_analysis.append(analysis_result[0])
            positive_analysis.append(analysis_result[1])
            positive_analysis.append(l)
            annotated_corpus['positive'].append(positive_analysis)
        else:
            annotated_corpus['negative'].append(l)
    return annotated_corpus

# The annotation process consists of steps. In each step we can pass over the message (and delete it from corpus), or try modifications on it if we do not agree with the resulting analysis
def annotation_step(user_description):
    try_or_go = raw_input('(t)ry / (g)o ? ')
    launch_create_annotated_corpus = False
    while try_or_go == 't':
        generated_lexicon = lexicon_generator()
        analysis_result = user_analyzer(user_description,generated_lexicon)
        if analysis_result != '<unknown source>':
            testing_user_description = user_description.replace(analysis_result[1], ' [ '+analysis_result[1]+' ] ')
            print '\n'
            print testing_user_description, ' | ', analysis_result[0]
            print '\n'
            launch_create_annotated_corpus = True
            try_or_go = raw_input('(t)ry / (g)o ? ')
        else:
            print '\n'
            print user_description, ' | ', '<no annotations>'
            print '\n'
            launch_create_annotated_corpus = True
            try_or_go = raw_input('(t)ry / (g)o ? ')
    else:
        corpus.remove(user_description)
    return launch_create_annotated_corpus

# This function starts the whole annotation process, and calls the latter on each step
def annotation_process():
    annotated_corpus = create_annotated_corpus(corpus)
    while len(corpus) > 0:
        while len(annotated_corpus['negative']) > 0:
            for user_description in annotated_corpus['negative']:
                print '\n'
                print user_description
                print '\n'
                if annotation_step(user_description) is True:
                    annotated_corpus = create_annotated_corpus(corpus)
                    break                 
                else:
                    if annotated_corpus['negative'].index(user_description) != -1:
                        annotated_corpus['negative'].remove(user_description)
                        continue
                    else:
                        annotated_corpus['negative'].remove(user_description)
                        break
        else:
            for positive_item in annotated_corpus['positive']:
                testing_user_description = positive_item[2].replace(positive_item[1], ' [ '+positive_item[1]+' ] ')
                print '\n'
                print testing_user_description, ' | ', positive_item[0]
                print '\n'
                if annotation_step(positive_item[2]) is True:
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
        print '\n' + '*** No more user_descriptions ***' + '\n'
        quit()

annotation_process()