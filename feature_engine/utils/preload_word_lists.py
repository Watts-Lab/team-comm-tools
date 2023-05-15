import os
'''
Several functions involve comparing text against a specific lexicon.
In order to prevent repeated re-loading of the lexicon, we pre-load them here.
'''

"""
Returns the list of easy words according to Dale-Chall readability.
"""
def get_dale_chall_easy_words():
    #get the list of dale-chall words
    with open('./features/lexicons/dale_chall.txt', 'r') as file:
        easy_word_list = [line.strip() for line in file]
    return easy_word_list

"""
Returns the list of function words, according to Ranganath, Jurafsky, and McFarland (2013).
https://web.stanford.edu/~jurafsky/pubs/ranganath2013.pdf
"""
def get_function_words():
    #get the list of dale-chall words
    with open('./features/lexicons/function_words.txt', 'r') as file:
        function_word_list = [line.strip() for line in file]
    return function_word_list

"""
Returns a list of question words.
"""
def get_question_words():
    #get the list of dale-chall words
    with open('./features/lexicons/question_words.txt', 'r') as file:
        question_word_list = [line.strip() for line in file]
    return question_word_list