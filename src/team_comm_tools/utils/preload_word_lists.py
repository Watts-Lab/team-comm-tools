import os
'''
Several functions involve comparing text against a specific lexicon.
In order to prevent repeated re-loading of the lexicon, we pre-load them here.
'''

def get_dale_chall_easy_words():
    """
    Returns the list of easy words according to the Dale-Chall readability formula.

    Reference: https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula

    :return: A list of easy words as defined by the Dale-Chall readability formula.
    :rtype: list
    """
    current_dir = os.path.dirname(__file__)
    dale_chall_file_path = os.path.join(current_dir, '../features/lexicons/dale_chall.txt')
    dale_chall_file_path = os.path.abspath(dale_chall_file_path)

    with open(dale_chall_file_path, 'r') as file:
        easy_word_list = [line.strip() for line in file]
    return easy_word_list

def get_function_words():
    """
    Returns the list of function words according to Ranganath, Jurafsky, and McFarland (2013).

    Reference: https://web.stanford.edu/~jurafsky/pubs/ranganath2013.pdf

    :return: A list of function words.
    :rtype: list
    """
    current_dir = os.path.dirname(__file__)
    function_word_file_path = os.path.join(current_dir, '../features/lexicons/function_words.txt')
    function_word_file_path = os.path.abspath(function_word_file_path)

    with open(function_word_file_path, 'r') as file:
        function_word_list = [line.strip() for line in file]
    return function_word_list

def get_question_words():
    """
    Returns a list of question words.

    :return: A list of question words.
    :rtype: list
    """
    current_dir = os.path.dirname(__file__)
    question_word_file_path = os.path.join(current_dir, '../features/lexicons/question_words.txt')
    question_word_file_path = os.path.abspath(question_word_file_path)

    with open(question_word_file_path, 'r') as file:
        question_word_list = [line.strip() for line in file]
    return question_word_list

def get_first_person_words():
    """
    Returns a list of first-person pronouns.

    :return: A list of first-person pronouns.
    :rtype: list
    """
    # current_script_directory = Path(__file__).resolve().parent
    # first_person_word_file_path = current_script_directory / "../features/lexicons/other_lexicons/first_person.txt"
    # with open(first_person_word_file_path, 'r') as file:
    #     first_person_word_list = [line.strip() for line in file]
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '../features/lexicons/other_lexicons/first_person.txt')
    file_path = os.path.abspath(file_path)
    with open(file_path, 'r') as file:
        first_person_word_list = [line.strip() for line in file]
    return first_person_word_list