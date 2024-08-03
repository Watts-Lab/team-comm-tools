import pytest
import pandas as pd
import numpy as np
from numpy import nan
import logging
import itertools

# Import Test Outputs
input_data = pd.read_csv("data/cleaned_data/multi_task_TINY_cols_renamed.csv", encoding='utf-8')
case1_chatdf = None # starts out as None as reading this file in is a test unto itself!
case2_chatdf = pd.read_csv("./output/chat/tiny_multi_task_case2_level_chat.csv")
case3a_chatdf = pd.read_csv("./output/chat/tiny_multi_task_case3a_level_chat.csv")
case3b_chatdf = pd.read_csv("./output/chat/tiny_multi_task_case3b_level_chat.csv")
case3c_chatdf = pd.read_csv("./output/chat/tiny_multi_task_case3c_level_chat.csv")
impropercase_chatdf = pd.read_csv("./output/chat/tiny_multi_task_improper_level_chat.csv")

# Import the Feature Dictionary
from team_comm_tools.feature_dict import feature_dict

def test_path_robustness():
    # case 1 was specified without the necessary 'output/', 'chat/', and '.csv' in its path. Ensure it works!
    try:
        case1_chatdf = pd.read_csv("./output/chat/tiny_multi_task_PT1_level_chat.csv")
    except:
        with open('test.log', 'a') as file:
            file.write("\n")
            file.write("------TEST FAILED------\n")
            file.write(f"Case 1 file (./output/chat/tiny_multi_task_PT1_level_chat.csv) not found: Path robustness test failed.\n")
        raise

def test_case_1():

    try:
        case1_chatdf = pd.read_csv("./output/chat/tiny_multi_task_PT1_level_chat.csv")
        # Case 1 should have the same number of rows as the input df
        assert(input_data.shape[0] == case1_chatdf.shape[0])
    except AssertionError:
        with open('test.log', 'a') as file:
            file.write("\n")
            file.write("------TEST FAILED------\n")
            file.write(f"Case 1: Testing whether processed chat data has the same number of rows (chats) as input data.\n")
            file.write(f"Expected value: {input_data.shape[0]}\n")
            file.write(f"Actual value: {case1_chatdf.shape[0]}\n")

        raise  # Re-raise the AssertionError to mark the test as failed

def test_case_2():
    try:
        # Case 2 should have the same number of unique items between "conversation_num" and "stageId"
        num_case2_conversationnums = len(case2_chatdf["conversation_num"].drop_duplicates())
        num_case2_stageIds = len(case2_chatdf["stageId"].drop_duplicates())

        assert(num_case2_conversationnums == num_case2_stageIds)
    except AssertionError:
        with open('test.log', 'a') as file:
            file.write("\n")
            file.write("------TEST FAILED------\n")
            file.write(f"Case 2: Testing whether grouped data has the correct number of unique items.\n")
            file.write(f"Expected value: {num_case2_conversationnums}\n")
            file.write(f"Actual value: {num_case2_stageIds}\n")

        raise  

def test_case_3ab():
    # 3a
    case_3a_rowcounts = pd.DataFrame(case3a_chatdf.groupby("conversation_num")["speakerId"].count()).reset_index()
    case_3a_rowcounts = case_3a_rowcounts.rename(columns={"conversation_num": "stageId"})
    input_data_rowcounts = pd.DataFrame(input_data.groupby("stageId")["speakerId"].count()).reset_index()

    # 3b
    case_3b_rowcounts = pd.DataFrame(case3b_chatdf.groupby("conversation_num")["speakerId"].count()).reset_index()
    case_3b_rowcounts = case_3b_rowcounts.rename(columns={"conversation_num": "stageId"})

    case3a_orig_comparison = case_3a_rowcounts.merge(input_data_rowcounts, how = "inner", on = "stageId").rename(columns={"speakerId_x": "3a", "speakerId_y": "orig"})
    case3ab_orig_comparison = case_3b_rowcounts.merge(case3a_orig_comparison, how = "inner", on = "stageId").rename(columns={"speakerId": "3b"})


    try:
        # assert that conversations can only get longer if we group cumulatively
        orig_longer_than_3a = len(case3ab_orig_comparison[case3ab_orig_comparison["3a"] < case3ab_orig_comparison["orig"]])
        assert(orig_longer_than_3a == 0)
        origi_longer_than_3b = len(case3ab_orig_comparison[case3ab_orig_comparison["3b"] < case3ab_orig_comparison["orig"]])
        assert(origi_longer_than_3b == 0)

        # assert that we can only get more rows if we don't do within_task
        b_longer_than_a = len(case3ab_orig_comparison[case3ab_orig_comparison["3b"] > case3ab_orig_comparison["3a"]])
        assert(b_longer_than_a == 0)

    except AssertionError:
        with open('test.log', 'a') as file:
            file.write("\n")
            file.write("------TEST FAILED------\n")
            file.write(f"Case 3a and 3b: Testing whether cumulative conversations have the proper number of rows.\n")
            file.write(f"Expected: conversations only get longer when we we don't do within_task, and when we group cumulatively.\n")
            file.write(f"Number of Rows in which original is longer than 3a (should be 0): {orig_longer_than_3a}\n")
            file.write(f"Number of Rows in which original is longer than 3b (should be 0): {origi_longer_than_3b}\n")
            file.write(f"Number of Rows in which 3b is longer than 3a (should be 0): {b_longer_than_a}\n")

        raise  

def test_within_task_flag():
    try:
        # assert that the within_task flag is working
        for conversation_id in case3b_chatdf["conversation_num"].unique():
            # get all chats with this id
            conversation = case3b_chatdf[case3b_chatdf["conversation_num"] == conversation_id]
            assert(len(conversation["task"].unique())==1)

    except AssertionError:
        with open('test.log', 'a') as file:
            file.write("\n")
            file.write("------TEST FAILED------\n")
            file.write(f"Within-Task Flag Check Failed.\n")
        raise


def test_case_3c():
    # 3c
    case_3c_rowcounts = pd.DataFrame(case3c_chatdf.groupby("conversation_num")["speakerId"].count()).reset_index()
    case_3c_rowcounts = case_3c_rowcounts.rename(columns={"conversation_num": "roundId"})
    input_data_rowcounts_by_roundId = pd.DataFrame(input_data.groupby("roundId")["speakerId"].count()).reset_index()

    case3c_orig_comparison = case_3c_rowcounts.merge(input_data_rowcounts_by_roundId, how = "inner", on = "roundId").rename(columns={"speakerId_x": "3c", "speakerId_y": "orig"})

    try:
        # First assert that we properly grouped by the roundId (Mid-level grouper)
        case3c_roundids = len(case_3c_rowcounts["roundId"].unique())
        inputdata_roundids = len(input_data["roundId"].unique())
        assert(case3c_roundids == inputdata_roundids)
    except AssertionError:
        with open('test.log', 'a') as file:
            file.write("\n")
            file.write("------TEST FAILED------\n")
            file.write(f"Case 2c: Testing whether grouped data has the correct number of unique items.\n")
            file.write(f"Expected value: {case3c_roundids}\n")
            file.write(f"Actual value: {inputdata_roundids}\n")

        raise  
    try:
        # assert that conversations can only get longer if we group cumulatively
        orig_longer_than_3c = len(case3c_orig_comparison[case3c_orig_comparison["3c"] < case3c_orig_comparison["orig"]])
        assert(orig_longer_than_3c == 0)
    except AssertionError:
        with open('test.log', 'a') as file:
            file.write("\n")
            file.write("------TEST FAILED------\n")
            file.write(f"Case 3c: Testing whether cumulative conversations have the proper number of rows.\n")
            file.write(f"Expected: conversations only get longer when we group cumulatively.\n")
            file.write(f"Number of Rows in which original is longer than 3c (should be 0): {orig_longer_than_3c}\n")

        raise  

def test_improper_case():
    try:
        # assert that we treat the improper case the exact same as case 2
        assert(impropercase_chatdf.shape == case2_chatdf.shape)
        assert(impropercase_chatdf["conversation_num"].equals(case2_chatdf["conversation_num"]))

    except AssertionError:
        improper_ids = len(impropercase_chatdf["conversation_num"].unique())
        case_2_ids = len(case2_chatdf["conversation_num"].unique())

        with open('test.log', 'a') as file:
            file.write("\n")
            file.write("------TEST FAILED------\n")
            file.write(f"Improper Case: Testing whether we treat the Improper Case the same as Case 2.\n")
            file.write(f"Number of unique conversation identifiers in improper case: {improper_ids}\n")
            file.write(f"Number of unique conversation identifiers in Case 2: {case_2_ids}\n")

def test_robustness_to_existing_column_names():
    try:
        chat_df_orig = pd.read_csv("./output/chat/test_chat_level_chat.csv") # original output
        chat_df_existing = pd.read_csv("./output/chat/test_chat_level_existing_chat.csv") # output for dataframe that had existing cols

        # filter down to the feature columns of interest
        chat_features = list(itertools.chain(*[feature_dict[feature]["columns"] for feature in feature_dict.keys() if feature_dict[feature]["level"] == "Chat"]))
        chat_feature_cols = [col for col in chat_df_orig.columns if col in chat_features]
        chat_df_orig = chat_df_orig[chat_feature_cols].reset_index(drop=True)
        chat_df_existing = chat_df_existing[chat_feature_cols].reset_index(drop=True)

        # assert that we have the right dimensions for both
        assert(chat_df_orig.shape == chat_df_existing.shape)

    except AssertionError:
        with open('test.log', 'a') as file:
            file.write("\n")
            file.write("------TEST FAILED------\n")
            file.write(f"Robustness check for passing in chat dataframe with feature columns failed.\n")

        raise 