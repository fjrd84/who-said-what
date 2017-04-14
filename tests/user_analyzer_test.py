"""
Test the user analyzer engine
"""
from engines import user_analyzer


def test_dictionary_parser():
    """
    Parse a demo dictionary
    """
    dictionary = user_analyzer.dictionary_parser('./tests/test_dictionary.txt')
    assert dictionary['<DISEASE>'] == ['liver cancer']
    assert dictionary['<MEDICAL_FIELD>'] == ['family medicine']
    assert dictionary['<MEDICAL_ATTRIBUTE>'] == ['family medicine']
    assert dictionary['<MEDICAL_JOB>'] == ['physicist', 'dermat(ó|o)log(o|a)']
