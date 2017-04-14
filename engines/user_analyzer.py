#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

###################
## User Analyzer ##
###################

This program receives a user description input, and extracts key information
from it to categorize the profile of the user (e.g. 'Proud husband. Radiologist
at Mayo clinic and Runner' --> 'Radiologist at Mayo Clinic')
user_analyzer consists of 2 functions: (1) lexicon_generator loads
linguistic knowledge to feed the analyzer (a simple NLP engine), (2)
user_analyzer uses information from the previous input to annotate the
key words or expression which best categorizes the profile of the user.

"""


# Pending screen user name analysis (e.g. @user, MD)
import re


def dictionary_parser(dictionary_file_path):
    """
    1) Create a dictionary of words (hospital, clinic) linked to nodes, e.g. <MEDICAL_PLACE>
    The input file 'user_dictionary.txt' should be as follows:
    (1 entry per line), e.g.
    <MEDICAL_PLACE> \t hospital
    <MEDICAL_PROFESSION> \t anesthesiologist
    """
    dictionary_f = open(dictionary_file_path, 'r')
    dictionary = dict()
    for l in dictionary_f:
        l = l.rstrip()
        entry_list = l.split('\t')
        if entry_list[0] not in dictionary.keys():
            dictionary[entry_list[0]] = []
            dictionary[entry_list[0]].append(entry_list[1])
        else:
            dictionary[entry_list[0]].append(entry_list[1])
    # The following loop reads dictionary's entries which have nodes inside,
    # e.g. <MEDICAL_JOB> \t <ADMINISTRATIVE_JOB>. It replaces the node for all
    # its words
    for entry in dictionary.items():
        for item in entry[1]:
            if item.startswith('<'):
                if '|' in item:
                    insidenode_l = item.split('|')
                    for insidenode in insidenode_l:
                        if insidenode in dictionary.keys():
                            for w in dictionary[insidenode]:
                                if w not in dictionary[entry[0]]:
                                    dictionary[entry[0]].append(w)
                        dictionary[entry[0]].remove(insidenode)
                else:
                    insidenode = item
                    if insidenode in dictionary.keys():
                        for w in dictionary[insidenode]:
                            if w not in dictionary[entry[0]]:
                                dictionary[entry[0]].append(w)
                    dictionary[entry[0]].remove(insidenode)
    dictionary_f.close()
    return dictionary


def lexicon_generator(grammar_file_path, dictionary):
    """
    2) Generate a lexicon from a set of simple grammar patterns and a dictionary:
    The file user_grammar.txt should be as follows:
    (1 entry per line), e.g.
    ¡<MEDICAL_PROFESSION> in <MEDICAL_PLACE>¡
    The symnol '¡' sets the text span to display as annotation
    """
    generated_lexicon = dict()
    user_grammar_f = open(grammar_file_path, 'r')
    pattern_list = user_grammar_f.readlines()
    for l in pattern_list[:len(pattern_list) - 2]:
        l = l.rstrip()
        full_pattern = l
        displaying_pattern = l.split('¡')[1]
        pattern = l.replace('¡', '')
        instance = pattern
        displaying_instance = displaying_pattern
        # generated_lexicon is as follows: {'full_pattern'}: [instance,
        # displaying_instance]
        generated_lexicon[full_pattern] = []
        # (a) 'instance' matches the whole pattern
        if re.search('<\S+?>', pattern):
            node_list = re.findall('<\S+?>', pattern)
            for node in node_list:
                if node in dictionary.keys():
                    instance = re.sub(
                        node, '(' + '|'.join(dictionary[node]) + ')', instance)
            generated_lexicon[full_pattern].append(instance)
        else:
            generated_lexicon[full_pattern].append(instance)
        # (b) 'displaying_instance' matches key words inside the pattern to better categorize the user's description
        if re.search('<\S+?>', displaying_pattern):
            node_list = re.findall('<\S+?>', displaying_pattern)
            for node in node_list:
                if node in dictionary.keys():
                    displaying_instance = re.sub(
                        node, '(' + '|'.join(dictionary[node]) + ')', displaying_instance)
            generated_lexicon[full_pattern].append(displaying_instance)
        else:
            generated_lexicon[full_pattern].append(displaying_instance)
    user_grammar_f.close()
    return generated_lexicon

# (2) Analyzer:


def user_analyzer(user_description, generated_lexicon):
    longest_match = ''
    # 'matching_pattern' and 'result' are only for annotation purposes (in userannotator)
    matching_pattern = ''
    result = []
    for full_pattern, instance_pair in generated_lexicon.items():
        if re.search(instance_pair[0], user_description):
            possible_match = user_description[re.search(instance_pair[0], user_description).start(
            ):re.search(instance_pair[0], user_description).end()]
            if len(possible_match) > len(longest_match):
                longest_match = possible_match
                matching_pattern = full_pattern
    if len(longest_match) > 0:
        displaying_instance = generated_lexicon[matching_pattern][1]
        displaying_match = user_description[re.search(displaying_instance, user_description).start(
        ):re.search(displaying_instance, user_description).end()]
        result.append(matching_pattern)
        result.append(displaying_match)
    else:
        result.append('<no pattern>')
        result.append('<unknown source>')
    return result
