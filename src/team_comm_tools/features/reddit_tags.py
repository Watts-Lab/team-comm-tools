import numpy as np
import string
import re


def count_all_caps(text):
    """
    The number of all-caps words in the input text.

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of all-caps words in the input text.
    """
    words = text.split()
    # Check if the word is all uppercase, is alphabetical, and has more than one letter. Differentiating all caps vs acronyms?
    all_caps_count = sum(
        1 for word in words 
        if word.strip(string.punctuation).isupper()  
        and word.strip(string.punctuation).isalpha() 
        and len(word.strip(string.punctuation)) > 1 
        or (word.strip(string.punctuation) != "I" and len(word.strip(string.punctuation)) == 1)
    ) 
    return all_caps_count

def count_links(text):

    """
    Returns the number of links in a message.

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of links in the input text.
    """
    link_pattern = r'http[s]?://[^\s]+|\b\S+?\.(com|org|net|edu|gov|io)\b'
    links = re.findall(link_pattern, text)
    return len(links)


def count_user_references(text):

    """
    Returns the number of user references in a message, indicated by format u/username.

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of user references in the input text.
    """

    user_refs = re.findall(r'\bu/[^\s]+', text)
    return len(user_refs)

def count_emphasis(text):
    """
    Returns the number of **bolded**, *italicized*, or ***bolded and italicized*** words in a message.

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of emphasized words in the input text.
    """
    formatted_texts = re.findall(r'\*{1,3}(.*?)\*{1,3}', text)
    return len(formatted_texts)

def count_bullet_points(text):
    """
    Returns the number of bullet points in a message starting with asterisks or dashes.

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of bullet points in the input text.
    """
    normalized_text = text.replace('\\n', '\n')
    bullet_points = re.findall(r'^[\*\-] .+', normalized_text, flags=re.MULTILINE)
    return len(bullet_points)


def count_numbering(text):
    """
    Returns the number of numberings in a message, indicated by a format like "1. ".

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of numbered lists in the input text.
    """
    normalized_text = text.replace('\\n', '\n')
    numberings = re.findall(r'^\d+\. .+', normalized_text, flags=re.MULTILINE)
    return len(numberings)


def count_line_breaks(text):
    """
    Returns the number of paragraphs / line breaks in a message.

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of line breaks in the input text.
    """
    normalized_text = text.replace('\\n', '\n').replace('\\r', '\n').replace('\r\n', '\n').replace('\r', '\n')
    text_single_breaks = re.sub(r'\n+', '\n', normalized_text)
    line_break_count = text_single_breaks.count('\n') + 1  
    return line_break_count


def count_quotes(text):
    """
    Returns the number instances of text enclosed in quotation marks in a message.

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of quoted texts in the input text.
    """
    double_quoted_texts = re.findall(r'"[^"\\]*(?:\\.[^"\\]*)*"', text)
    single_quoted_texts = re.findall(r"'[^'\\]*(?:\\.[^'\\]*)*'", text)    
    return len(double_quoted_texts) + len(single_quoted_texts)


def count_responding_to_someone(text):
    """
    Returns the number of block quote responses, indicating if the message is quoting someone else by ">" or "&gt;".

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of block quote responses in the input text.
    """
    normalized_text = text.replace('&gt;', '>')
    pattern = r'^>.*'
    responses = re.findall(pattern, normalized_text, re.M)
    return len(responses)


def count_ellipses(text):
    """
    Returns the number of ellipses (three or more consecutive dots) in a message.

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of ellipses in the input text.
    """
    ellipses = re.findall(r'\.{3,}', text)
    return len(ellipses)


def count_parentheses(text):
    """
    Returns the number of instances of text enclosed in parentheses in a message (includes nested parentheses).

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of parenthetical texts in the input text.
    """
    count = 0
    stack = []

    for char in text:
        if char == '(':
            stack.append(char)
        elif char == ')' and stack:
            stack.pop()
            count += 1

    return count


def count_emojis(text):
    """
    Returns the number of instances of emojis in a message.

    Args:
        text (str): The input text to be analyzed.

    Returns:
        int: The number of emojis in the input text.
    """
    emoji_pattern = r'[:;]-?\)+'
    emojis = re.findall(emoji_pattern, text)
    return len(emojis)
