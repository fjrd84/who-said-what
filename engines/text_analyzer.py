# SpaCy is ON #

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Libraries:
# from __future__ import unicode_literals
import re
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
path_to_language_data = '/Users/DoraDorita/Desktop/NLP/language_data/'
from spacy.en import English
# Function for text processing with Spacy:
print 'Loading libraries...' 
nlp = English()


##############
## Analyzer ##
##############

# This program receives a text input (message), and extracts valuable information from it within the DISEASE-TREATMENT cognitive frame, i.e. a disease and a potential solution for it.

# The Analyzer consists of 3 functions: (1) language_data_loader loads linguistic knowledge to feed the Analyzer (a simple NLP engine), (2) start_word_match finds disease mentions in the incoming text message, (3) Analyzer uses information from previous inputs to extract entities (syntactically, noun phrases) that semantically express solutions for a mentioned disease. 

# (1) Language data loader:

def language_data_loader():
    language_data = dict()
    # Load grammar:
    grammar_file = open(path_to_language_data+'grammar.txt', 'r')
    grammar = []
    for l in grammar_file:
        l = l.strip()
        grammar.append(l)
    grammar_file.close()
    language_data['grammar'] = grammar
    # Load start words (a term list to recover messages on diseases):
    start_words_file = open(path_to_language_data+'start_words.txt', 'r')
    start_words = []
    for l in start_words_file:
        l = l.strip()
        l = l.lower()
        start_words.append(l)
    start_words_file.close()
    language_data['start_words'] = start_words
    # Load stop words (words tagged as noun phrases that cannot be extracted as entities (e.g. You, @username11):
    stop_words_file = open(path_to_language_data+'stop_words.txt', 'r')
    stop_words = []
    for l in stop_words_file:
        l = l.strip()
        l = l.lower()
        stop_words.append(l)
    stop_words_file.close()
    language_data['stop_words'] = stop_words
    return language_data

# (2) 'start word' finder:

def start_word_match(message,start_word_list):
    start_word = ''
    for w in start_word_list:
        if re.search(w,message):
            start_word_is_now = message[re.search(w,message).start():re.search(w,message).end()]
            if len(start_word_is_now) > len(start_word):
                start_word = start_word_is_now
    # we search for the longest match ('Mindfulness for anorexia nervosa' gets 'anorexia nervosa' but not 'anorexia', although both are disease terms)
    if len(start_word) > 0:
        return start_word
    elif len(start_word) == 0:
        return '<No start word in message>'

# (3) Analyzer (treatment-entity finder)
# The input grammar follows two basic syntactic schemes, where X = treatment/solution and Y = disease/problem: 
# (a) X to treat Y -> X comes first, (b) Y treated with X -> Y comes first.

def analyzer(message,start_words,grammar,stop_words):
    # Find the start word in message:
    start_word = start_word_match(message,start_words)
    twitter_start_word = '(' + '#' + start_word + '|' + start_word + ')'
    # Necessary variables:
    longest_match = ''
    matching_pattern = ''
    output = []
    NP_list = []
    # First, check if start_word is in message
    if start_word != '<No start word in message>':
        # For every stored grammar rule, generate its counterpart including the start word (e.g. '[s] for [p]' -> '[s] for anorexia')
        for pattern in grammar:
            instance = pattern.replace('[p]',twitter_start_word)
            instance = re.sub('\s*\[s\]\s*','',instance)
            # Test every rule against the message:
            if re.search(instance,message):
                found_instance = instance
                match = message[re.search(found_instance,message).start():re.search(found_instance,message).end()+1]
                # Find the rule with the longest match in the string:
                if len(match) > len(longest_match):
                    longest_match = match
                    matching_pattern = pattern
        # Rule matchs if 'longest_match' contains a string
        if len(longest_match) > 0:
            # The matching rule has the structure: S before P, where S is a string potentially including the treatment entity
            if matching_pattern.find('[s]') < matching_pattern.find('[p]'):
                target_match = message[:message.find(longest_match)]
                # target_match = unicode(target_match, "utf-8" )
                if len(target_match) >= 3:
                    # # Search NPs within target_match (target string):
                    for np in nlp(target_match.decode('utf-8')).noun_chunks:
                        NP_list.append(np)
                    if len(NP_list) > 0:
                        # Avoid the NP (noun phrase), if it's a stop word (e.g. You) 
                        forbidden_NP = False
                        for stop_word in stop_words:
                            if re.search(stop_word, str(NP_list[-1])):
                                forbidden_NP = True
                        if forbidden_NP is False:
                            # Include start_word and NP in a list named 'ouput'. Choose the latest NP from the target string (e.g. 'This treatment is a medicine...' gets 'medicine' but not 'treatment')
                            NP_outcome = str(NP_list[-1])
                            output.append(NP_outcome)
                            output.append(start_word)
                            output.append(matching_pattern)
                            return output
                    # output.append(target_match)
                    # output.append(start_word)
                    # output.append(matching_pattern)
                    # return output
            # The matching rule has the structure: P before S:
            elif matching_pattern.find('[s]') > matching_pattern.find('[p]'):
                target_match = message[message.find(longest_match)+len(longest_match):]
                if len(target_match) >= 3:
                    for np in nlp(target_match).noun_chunks:
                        NP_list.append(np)
                    if len(NP_list) > 0:
                        forbidden_NP = False
                        for stop_word in stop_words:
                            if re.search(stop_word,str(NP_list[0])):
                                forbidden_NP = True
                        if forbidden_NP is False:
                            # Choose the first NP from the target string (e.g. 'treated by a medicine from the shop', gets 'medicine' but not 'shop')
                            NP_outcome = str(NP_list[0])
                            output.append(NP_outcome)
                            output.append(start_word)
                            output.append(matching_pattern)
                            return output
                    # output.append(target_match)
                    # output.append(start_word)
                    # output.append(matching_pattern)
                    # return output
    if len(output) == 0:
        output.append('<nothing_found>')
        output.append(start_word)
        output.append('<no pattern found>')
        return output
        # return '<nothing found>'

# Use this to try text_analyzer on a corpus or a single sentence:

# s = str('new treatment for people with vasculopathy')
# language_data = language_data_loader()
# print analyzer(s,language_data['start_words'],language_data['grammar'],language_data['stop_words'])

# path_to_testing_corpus = '/Users/DoraDorita/Desktop/NLP/corpus/'
# corpus = open(path_to_testing_corpus+'all.txt', 'r').readlines()
# language_data = language_data_loader()
# for l in corpus:
#     l = l.rstrip()
#     l = l.split('  @@@  ')[0]
#     l = l.decode('utf-8')
#     result = analyzer(l,language_data['start_words'],language_data['grammar'],language_data['stop_words'])
#     print result[0], '-->', result[1]
 