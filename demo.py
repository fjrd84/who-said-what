#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Libraries
import sys
sys.path.insert(0, '/Users/DoraDorita/Desktop/NLP/engines')
import json
from datetime import datetime
from user_analyzer import *
from text_analyzer import *

# Language sources:
language_data = language_data_loader()
generated_lexicon = lexicon_generator()

def demo(external_input):
	input_data = json.loads(external_input)
	output_data = dict()
	# Get 'profile' and 'health_related'
	output_data['profile'] = user_analyzer(input_data['user_description'], generated_lexicon)[1]
	if output_data['profile'] != '<unknown source>':
		output_data['health_related'] = True
	else:
		output_data['health_related'] = False
	# Get 'solution'
	output_data['solution'] = analyzer(input_data['message'],language_data['start_words'],language_data['grammar'],language_data['stop_words'])[0]
	# Get 'problem'
	output_data['problem'] = analyzer(input_data['message'],language_data['start_words'],language_data['grammar'],language_data['stop_words'])[1]
	# Get 'date'
	output_data['created_at'] = str(datetime.now())
	return json.dumps(output_data)

# Testing demo in corpus:
corpusf_path = '/Users/DoraDorita/Desktop/NLP/corpus/'
corpus = open(corpusf_path+'heart_disease_cholesterol_hypertension_diabetes_obesity.json', 'r').readlines()
for line in corpus:
	line = line.rstrip()
	print demo(line)





 

