"""
file: run_tests.py
---
This file runs the feature builder pipeline on our custom testing datasets.
"""

# Importing the Feature Generating Class
from team_comm_tools import FeatureBuilder
import pandas as pd
import chardet

# Main Function
if __name__ == "__main__":

	# detects CSV encoding of our datasets
	with open("data/cleaned_data/test_chat_level.csv", 'rb') as file:
		chat_encoding = chardet.detect(file.read())

	with open("data/cleaned_data/test_conv_level.csv", 'rb') as file:
		conv_encoding = chardet.detect(file.read())

	chat_df = pd.read_csv("data/cleaned_data/test_chat_level.csv", encoding=chat_encoding['encoding'])
	conv_df = pd.read_csv("data/cleaned_data/test_conv_level.csv", encoding=conv_encoding['encoding'])
	test_ner_df = pd.read_csv("data/cleaned_data/test_named_entity.csv", encoding='utf-8')
	test_ner_training_df = pd.read_csv("data/cleaned_data/train_named_entity.csv")
	chat_complex_df = pd.read_csv("data/cleaned_data/test_chat_level_complex.csv", encoding=chat_encoding['encoding'])
	conv_complex_df = pd.read_csv("data/cleaned_data/test_conv_level_complex.csv", encoding=chat_encoding['encoding'])
	test_forward_flow_df = pd.read_csv("data/cleaned_data/fflow.csv", encoding=chat_encoding['encoding'])
	conv_complex_timestamps_df = pd.read_csv("data/cleaned_data/test_conv_level_complex_timestamps.csv", encoding=chat_encoding['encoding'])

		
	# TESTING DATASETS -------------------------------

	testing_chat = FeatureBuilder(
		input_df = chat_df,
		vector_directory = "./vector_data/",
		output_file_path_chat_level = "./output/chat/test_chat_level_chat.csv",
		output_file_path_user_level = "./output/user/test_chat_level_user.csv",
		output_file_path_conv_level = "./output/conv/test_chat_level_conv.csv",
		custom_features = [ # these require vect_data, so they now need to be explicitly included in order to calculate them
            "(BERT) Mimicry",
            "Moving Mimicry",
            "Forward Flow",
            "Discursive Diversity"
        ],
		turns = False,
	)
	testing_chat.featurize(col="message")

	testing_conv = FeatureBuilder(
		input_df = conv_df,
		vector_directory = "./vector_data/",
		output_file_path_chat_level = "./output/chat/test_conv_level_chat.csv",
		output_file_path_user_level = "./output/user/test_conv_level_user.csv",
		output_file_path_conv_level = "./output/conv/test_conv_level_conv.csv",
		custom_features = [
            "(BERT) Mimicry",
            "Moving Mimicry",
            "Forward Flow",
            "Discursive Diversity"
        ],
		turns = False,
	)
	testing_conv.featurize(col="message")

	test_ner_feature_builder = FeatureBuilder(
		input_df = test_ner_df,
		ner_training_df = test_ner_training_df,
		vector_directory = "./vector_data/",
		output_file_path_chat_level = "./output/chat/test_named_entity_chat_level.csv",
		output_file_path_user_level = "./output/user/test_named_entity_user_level.csv",
		output_file_path_conv_level = "./output/conv/test_named_entity_conversation_level.csv",
		custom_features = [
            "(BERT) Mimicry",
            "Moving Mimicry",
            "Forward Flow",
            "Discursive Diversity"
        ],
		turns = False,
	)
	test_ner_feature_builder.featurize(col="message")

	# testing perturbed chat level features
	testing_chat_complex = FeatureBuilder(
		input_df = chat_complex_df,
		vector_directory = "./vector_data/",
		output_file_path_chat_level = "./output/chat/test_chat_level_chat_complex.csv",
		output_file_path_user_level = "./output/user/test_chat_level_user_complex.csv",
		output_file_path_conv_level = "./output/conv/test_chat_level_conv_complex.csv",
		custom_features = [
            "(BERT) Mimicry",
            "Moving Mimicry",
            "Forward Flow",
            "Discursive Diversity"
        ],
		turns = False,
	)
	testing_chat_complex.featurize(col="message")

	# testing conv features
	testing_conv_complex = FeatureBuilder(
		input_df = conv_complex_df,
		vector_directory = "./vector_data/",
		output_file_path_chat_level = "./output/chat/test_conv_level_chat_complex.csv",
		output_file_path_user_level = "./output/user/test_conv_level_user_complex.csv",
		output_file_path_conv_level = "./output/conv/test_conv_level_conv_complex.csv",
		custom_features = [
            "(BERT) Mimicry",
            "Moving Mimicry",
            "Forward Flow",
            "Discursive Diversity"
        ],
		turns = False,
	)
	testing_conv_complex.featurize(col="message")

	testing_conv_complex_ts = FeatureBuilder(
		input_df = conv_complex_timestamps_df,
		vector_directory = "./vector_data/",
		output_file_path_chat_level = "./output/chat/test_conv_level_chat_complex_ts.csv",
		output_file_path_user_level = "./output/user/test_conv_level_user_complex_ts.csv",
		output_file_path_conv_level = "./output/conv/test_conv_level_conv_complex_ts.csv",
		custom_features = [
            "(BERT) Mimicry",
            "Moving Mimicry",
            "Forward Flow",
            "Discursive Diversity"
        ],
		turns = False,
	)
	testing_conv_complex_ts.featurize(col="message")

	# testing forward flow
	testing_forward_flow = FeatureBuilder(
		input_df = test_forward_flow_df,
		vector_directory = "./vector_data/",
		output_file_path_chat_level = "./output/chat/test_forward_flow_chat.csv",
		output_file_path_user_level = "./output/user/test_forward_flow_user.csv",
		output_file_path_conv_level = "./output/conv/test_forward_flow_conv.csv",
		custom_features = [
			"(BERT) Mimicry",
			"Moving Mimicry",
			"Forward Flow",
			"Discursive Diversity"
		],
		turns = False,
	)

	testing_forward_flow.featurize(col="message")