import pytest
import pandas as pd
import numpy as np
from numpy import nan
import logging
import itertools

test_chat_df =  pd.read_csv("./output/chat/test_chat_level_chat.csv")
test_conv_df =  pd.read_csv("./output/conv/test_conv_level_conv.csv")

# Import the Feature Dictionary
import sys
import os

# Add the parent directory to the sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/team_comm_tools/')))
# from feature_dict import feature_dict
from team_comm_tools.feature_dict import feature_dict

chat_features = [feature_dict[feature]["columns"] for feature in feature_dict.keys() if feature_dict[feature]["level"] == "Chat"]
conversation_features = [feature_dict[feature]["columns"] for feature in feature_dict.keys() if feature_dict[feature]["level"] == "Conversation"]

num_features_chat = len(list(itertools.chain(*chat_features)))
num_features_conv = len(list(itertools.chain(*conversation_features)))

num_tested_chat = test_chat_df['expected_column'].nunique()
num_tested_conv = test_conv_df['expected_column'].nunique()

with open('test.log', 'w') as f:
    f.write(f'Tested {num_tested_chat} features out of {num_features_chat} chat level features: {num_tested_chat/num_features_chat * 100:.2f}% Coverage!\n')
    f.write(f'Tested {num_tested_conv} features out of {num_features_conv} conv level features: {num_tested_conv/num_features_conv * 100:.2f}% Coverage!\n')
    pass

# generate coverage for tests
@pytest.mark.parametrize("row", test_chat_df.iterrows())
def test_chat_unit_equality(row):
    actual = row[1][row[1]['expected_column']]
    expected = row[1]['expected_value']
    
    try:
        assert round(float(actual), 3) == round(float(expected), 3)
    except AssertionError:

        with open('test.log', 'a') as file:
            file.write("\n")
            file.write("------TEST FAILED------\n")
            file.write(f"Testing {row[1]['expected_column']} for message: {row[1]['message_original']}\n")
            file.write(f"Expected value: {expected}\n")
            file.write(f"Actual value: {actual}\n")

        raise  # Re-raise the AssertionError to mark the test as failed


@pytest.mark.parametrize("conversation_num, conversation_rows", test_conv_df.groupby('conversation_num'))
def test_conv_unit_equality(conversation_num, conversation_rows):
    test_failed = False
    expected_out = ""
    actual_out = ""

    for _, row in conversation_rows.iterrows():
        actual = row[row['expected_column']]
        expected = row['expected_value']
    
    try:
        assert round(actual, 3) == round(expected, 3)
    except AssertionError:
        expected_out = expected
        actual_out = actual
        test_failed = True

    if test_failed:
        with open('test.log', 'a') as file:
            file.write("\n")
            file.write("------TEST FAILED------\n")
            file.write(f"Testing {row['expected_column']} for conversation_num: {conversation_num}\n")
            file.write(f"Expected value: {expected_out}\n")
            file.write(f"Actual value: {actual_out}\n")

        raise