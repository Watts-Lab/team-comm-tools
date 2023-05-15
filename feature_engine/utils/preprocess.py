import re

def preprocess_conversation_columns(df):
	# remove all special characters from df
	df.columns = df.columns.str.replace('[^A-Za-z0-9_]', '', regex=True)
	
	# If data is grouped by batch/round, add a conversation num
	if {'batch_num', 'round_num'}.issubset(df.columns):
		df['conversation_num'] = df.groupby(['batch_num', 'round_num']).ngroup()
		df = df[df.columns.tolist()[-1:] + df.columns.tolist()[0:-1]] # make the new column first

	return(df)

def assert_key_columns_present(df):
	# remove all special characters from df
	df.columns = df.columns.str.replace('[^A-Za-z0-9_]', '', regex=True)

	# Assert that key columns are present
	if {'conversation_num', 'message', 'speaker_nickname'}.issubset(df.columns):
		print("Confirmed that data has `conversation_num`, `message`, and `speaker_nickname` columns!")
	else:
		print("One of `conversation_num`, `message`, or `speaker_nickname` is missing! Raising error...")
		print("Columns available: ")
		print(df.columns)
		raise KeyError

def preprocess_text_lowercase_but_retain_punctuation(text):
  	# Only turns the text lowercase
	return(text.lower())

def preprocess_text(text):
  	# For each individual message: preprocess to remove anything that is not an alphabet or number from the string
	return(re.sub(r"[^a-zA-Z0-9 ]+", '',text).lower())