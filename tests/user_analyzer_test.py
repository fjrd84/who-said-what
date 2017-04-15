"""
Test the user analyzer engine
"""
from engines import user_analyzer


def test_is_tag():
    """
    Test tag identification
    """
    # Valid tags
    assert user_analyzer.is_tag('<THIS_IS_A_TAG>')
    assert user_analyzer.is_tag('<TAG>')
    # Invalid tags
    assert not user_analyzer.is_tag('<THIS_I _A_TAG>')
    assert not user_analyzer.is_tag('<this is no tag>')
    assert not user_analyzer.is_tag('<SOME_INVALID_TAG')


def test_dictionary_parser():
    """
    Parse a demo dictionary
    """
    dictionary = user_analyzer.dictionary_parser(
        './tests/demo_user_dictionary.txt')
    assert dictionary['<DISEASE>'] == ['liver cancer']
    assert dictionary['<MEDICAL_FIELD>'] == ['family medicine', 'biotech']
    assert dictionary['<MEDICAL_ATTRIBUTE>'] == ['family medicine', 'biotech']
    assert dictionary['<MEDICAL_JOB>'] == ['physicist', 'dermat(ó|o)log(o|a)']


def test_lexicon_generator():
    """
    Generate a demo lexicon from a demo grammar file
    """

    dictionary = user_analyzer.dictionary_parser(
        './tests/demo_user_dictionary.txt')
    lexicon = user_analyzer.lexicon_generator('./tests/demo_user_grammar.txt',
                                              dictionary)
    assert lexicon == {'¡working for <MEDICAL_ATTRIBUTE>¡': [
        'working for (family medicine|biotech)',
        'working for (family medicine|biotech)']}
