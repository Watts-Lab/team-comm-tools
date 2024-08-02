"""
file: lexical_features_v2.py
---
A faster version of the lexical_features.py file.
"""
# Importing packages
import pickle
import re
import pandas as pd
import os
from pathlib import Path

def get_liwc_rate(regex, chat):
	""""
	Computes the LIWC features as a rate per 100 words, per best practice (Yeomans et al. 2023; https://www.mikeyeomans.info/papers/PGCR_yeomans.pdf, p. 42)

	We apply the following formula:
	Rate of word use / 100 words = count / chat length * (chat length / 100)

	Args:
		regex (str): The regular expression for the lexicon.
		chat(str): The message (utterance) being analyzed.

	Returns:
		float: The rate at which the message uses words from a given lexicon.
	"""
	if(len(chat) > 0):
		return (len(re.findall(regex, chat))/(len(chat)))*(len(chat)/100)
	else:
		return 0

def liwc_features(chat_df: pd.DataFrame, message_col) -> pd.DataFrame:
	"""
		This function takes in the chat level input dataframe and computes lexical features 
		(rates at which the message contains contains words from a given lexicon, such as LIWC).
			  
	Args:
		chat_df (pd.DataFrame): This is a pandas dataframe of the chat level features. Should contain 'message' column.
		message_col (str): This is a string with the name of the column containing the message / text.

	Returns:
		pd.DataFrame: Dataframe of the lexical features stacked as columns.
	"""
	# Load the preprocessed lexical regular expressions
	current_dir = os.path.dirname(__file__)
	lexicon_pkl_file_path = os.path.join(current_dir, './assets/lexicons_dict.pkl')
	lexicon_pkl_file_path = os.path.abspath(lexicon_pkl_file_path)
	with open(lexicon_pkl_file_path, "rb") as lexicons_pickle_file:
		lexicons_dict = pickle.load(lexicons_pickle_file)
	
	# Return the lexical features stacked as columns
	return pd.concat(
		# Finding the # of occurrences of lexicons of each type for all the messages.
		[pd.DataFrame(chat_df[message_col + "_original"].apply(lambda chat: get_liwc_rate(regex, chat)))\
										.rename({message_col + "_original": lexicon_type + "_lexical_per_100"}, axis=1)\
			for lexicon_type, regex in lexicons_dict.items()], 
		axis=1
	)
