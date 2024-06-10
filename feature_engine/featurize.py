"""
file: featurize.py
---
This file is the main driver of the feature generating pipeline. 
It instantiates and calls the FeatureBuilder class which defines the logic used for feature creation.
"""

# Importing the Feature Generating Class
from feature_builder import FeatureBuilder
import pandas as pd
import chardet

# Main Function
if __name__ == "__main__":

	# detects CSV encoding of our datasets
	with open("../feature_engine/testing/data/cleaned_data/test_chat_level.csv", 'rb') as file:
		chat_encoding = chardet.detect(file.read())

	with open("../feature_engine/testing/data/cleaned_data/test_conv_level.csv", 'rb') as file:
		conv_encoding = chardet.detect(file.read())

	chat_df = pd.read_csv("../feature_engine/testing/data/cleaned_data/test_chat_level.csv", encoding=chat_encoding['encoding'])
	chat_complex_df = pd.read_csv("../feature_engine/testing/data/cleaned_data/test_chat_level_complex.csv", encoding=chat_encoding['encoding'])
	conv_df = pd.read_csv("../feature_engine/testing/data/cleaned_data/test_conv_level.csv", encoding=conv_encoding['encoding'])
	tiny_juries_df = pd.read_csv("../feature_engine/tpm-data/cleaned_data/test_data/juries_tiny_for_testing.csv", encoding='utf-8')
	tiny_multi_task_df = pd.read_csv("../feature_engine/tpm-data/cleaned_data/test_data/multi_task_TINY.csv", encoding='utf-8')
	juries_df = pd.read_csv("../feature_engine/tpm-data/cleaned_data/jury_conversations_with_outcome_var.csv", encoding='utf-8')
	csop_df = pd.read_csv("../feature_engine/tpm-data/cleaned_data/csop_conversations_withblanks.csv", encoding='utf-8')
	csopII_df = pd.read_csv("../feature_engine/tpm-data/cleaned_data/csopII_conversations_withblanks.csv", encoding='utf-8')
	test_ner_df = pd.read_csv("../feature_engine/testing/data/cleaned_data/test_named_entity.csv", encoding='utf-8')
	test_ner_training_df = pd.read_csv("../feature_engine/testing/data/cleaned_data/train_named_entity.csv")
	
	# TINY / TEST DATASETS -------------------------------#
	
	# # Tiny Juries
	# tiny_juries_feature_builder = FeatureBuilder(
	# 	input_df = tiny_juries_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/jury_TINY_output_chat_level.csv",
	# 	output_file_path_user_level = "../feature_engine/output/user/jury_TINY_output_user_level.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/jury_TINY_output_conversation_level.csv",
	# 	turns = False,
	# )
	# feature_builder.featurize(col="message")

	# test_turn_taking_feature_builder = FeatureBuilder(
	# 	input_file_path = "../feature_engine/tpm-data/cleaned_data/test_data/test_turn_taking.csv",
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/test_turn_taking_chat_level.csv",
	# 	output_file_path_user_level = "../feature_engine/output/user/test_turn_taking_user_level.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/test_turn_taking_conversation_level.csv",
	# 	turns = False,
	# )
	# test_turn_taking_feature_builder.featurize(col="message")
    
	test_ner_feature_builder = FeatureBuilder(
		input_df = test_ner_df,
		ner_training_df = test_ner_training_df,
		vector_directory = "../feature_engine/tpm-data/vector_data/",
		output_file_path_chat_level = "../feature_engine/output/chat/test_named_entity_chat_level.csv",
		output_file_path_user_level = "../feature_engine/output/user/test_named_entity_user_level.csv",
		output_file_path_conv_level = "../feature_engine/output/conv/test_named_entity_conversation_level.csv",
		turns = False,
		conversation_id = "stageId",
		cumulative_grouping = True
	)
	test_ner_feature_builder.featurize(col="message")

	# # Tiny multi-task
	# tiny_multi_task_feature_builder = FeatureBuilder(
	# 	input_df = tiny_multi_task_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/multi_task_TINY_output_chat_level_stageId_cumulative.csv",
	# 	output_file_path_user_level = "../feature_engine/output/user/multi_task_TINY_output_user_level_stageId_cumulative.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/multi_task_TINY_output_conversation_level_stageId_cumulative.csv",
	# 	turns = False,
	# 	conversation_id = "stageId",
	# 	cumulative_grouping = True
	# )
	# tiny_multi_task_feature_builder.featurize(col="message")

	# testing chat features
	testing_chat = FeatureBuilder(
		input_df = chat_df,
		ner_training_df = test_ner_training_df,
		vector_directory = "../feature_engine/tpm-data/vector_data/",
		output_file_path_chat_level = "../feature_engine/output/chat/test_chat_level_chat.csv",
		output_file_path_user_level = "../feature_engine/output/user/test_chat_level_user.csv",
		output_file_path_conv_level = "../feature_engine/output/conv/test_chat_level_conv.csv",
		turns = False,
	)
	testing_chat.featurize(col="message")

	# testing perturbed chat level features
	testing_chat_complex = FeatureBuilder(
		input_df = chat_complex_df,
		vector_directory = "../feature_engine/tpm-data/vector_data/",
		output_file_path_chat_level = "../feature_engine/output/chat/test_chat_level_chat_complex.csv",
		output_file_path_user_level = "../feature_engine/output/user/test_chat_level_user_complex.csv",
		output_file_path_conv_level = "../feature_engine/output/conv/test_chat_level_conv_complex.csv",
		turns = False,
	)
	testing_chat_complex.featurize(col="message")

	# testing conv features
	testing_conv = FeatureBuilder(
		input_df = conv_df,
		vector_directory = "../feature_engine/tpm-data/vector_data/",
		output_file_path_chat_level = "../feature_engine/output/chat/test_conv_level_chat.csv",
		output_file_path_user_level = "../feature_engine/output/user/test_conv_level_user.csv",
		output_file_path_conv_level = "../feature_engine/output/conv/test_conv_level_conv.csv",
		turns = False,
	)
	testing_conv.featurize(col="message")

	# FULL DATASETS BELOW ------------------------------------- #
	
	# Juries
	# jury_feature_builder = FeatureBuilder(
	# 	input_df = juries_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/jury_output_chat_level.csv",
	# 	# output_file_path_chat_level = "",
	# 	output_file_path_user_level = "../feature_engine/output/user/jury_output_user_level.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/jury_output_conversation_level.csv",
	# 	turns = True
	# )
	# jury_feature_builder.featurize(col="message")

	# # CSOP (Abdullah)
	# csop_feature_builder = FeatureBuilder(
	# 	input_df = csop_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/csop_output_chat_level.csv",
	# 	output_file_path_user_level = "../feature_engine/output/user/csop_output_user_level.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/csop_output_conversation_level.csv",
	# 	turns = True
	# )
	# csop_feature_builder.featurize(col="message")


	# # CSOP II (Nak Won Rim)
	# csopII_feature_builder = FeatureBuilder(
	# 	input_df = csopII_df,
	# 	vector_directory = "../feature_engine/tpm-data/vector_data/",
	# 	output_file_path_chat_level = "../feature_engine/output/chat/csopII_output_chat_level.csv",
	# 	output_file_path_user_level = "../feature_engine/output/user/csopII_output_user_level.csv",
	# 	output_file_path_conv_level = "../feature_engine/output/conv/csopII_output_conversation_level.csv",
	# 	turns = True
	# )
	# csopII_feature_builder.featurize(col="message")
