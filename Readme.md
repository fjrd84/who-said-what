# Who said what

This repository is the first step towards an open-source project on health, social media and text mining. You can find here the code (currently being developed) of the NLP engine module. This module gets plain text as input, and returns a JSON file with an analysis that consists of:

1. A semantic analysis on the user profile (the sender of the message)
2. A semantic analysis on the message expressing a solution for a certain health problem.

The NLP module consists of two scritps (engines/text_analyzer.py, engines/user_analyzer.py), and language resources to perform the semantic parsing (language_resources).

You can also find here two simple annotators for populating the resources (semi-automatic annotation).

## Requirements

[Python 3](https://www.python.org/) is needed to run the demo. Scripts for setting it up and running it can be found into the [Makefile](https://en.wikipedia.org/wiki/Make_(software)).

## Install dependencies

`make init`

## Run the demo

`make`