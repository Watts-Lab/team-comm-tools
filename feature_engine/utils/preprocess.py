import re
import pandas as pd

def preprocess_conversation_columns(df, conversation_id, cumulative_grouping = False, within_task = False):
	# remove all special characters from df
	df.columns = df.columns.str.replace('[^A-Za-z0-9_]', '', regex=True)

	# If data is grouped by batch/round, add a conversation num
	if {'batch_num', 'round_num'}.issubset(df.columns):
		df[conversation_id] = df.groupby(['batch_num', 'round_num']).ngroup()
		df = df[df.columns.tolist()[-1:] + df.columns.tolist()[0:-1]] # make the new column first
	if ({'gameId', 'roundId', 'stageId'}.issubset(df.columns) and conversation_id in {'gameId', 'roundId', 'stageId'}):
		if(cumulative_grouping):
			df = create_cumulative_rows(df, conversation_id, within_task)
			df[conversation_id] = df['cumulative_Id'] # set it to be the cumulative grouping
		else:
			df[conversation_id] = df[conversation_id] # set it to the desired grouping

	return(df)

def assert_key_columns_present(df, column_names):
	# remove all special characters from df
	df.columns = df.columns.str.replace('[^A-Za-z0-9_]', '', regex=True)
	conversation_id = column_names['conversation_id_col']
	speaker_id = column_names['speaker_id_col']
	message = column_names['message_col']

	# Assert that key columns are present
	if {conversation_id, message, speaker_id}.issubset(df.columns):
		print(f"Confirmed that data has columns: {conversation_id}, {message}, {speaker_id}")
		# ensure no NA's in essential columns
		df[message] = df[message].fillna('')
		df[conversation_id] = df[conversation_id].fillna(0)
		df[speaker_id] = df[speaker_id].fillna(0)
	else:
		missing_columns = {conversation_id, message, speaker_id} - set(df.columns)
		print(f"Missing required columns: {missing_columns}")
		print("Columns available: ")
		print(df.columns)
		raise KeyError(f"Missing required columns: {missing_columns}")

def preprocess_text_lowercase_but_retain_punctuation(text):
	# Only turns the text lowercase
	return(text.lower())

def preprocess_text(text):
	# For each individual message: preprocess to remove anything that is not an alphabet or number from the string
	return(re.sub(r"[^a-zA-Z0-9 ]+", '',text).lower())

def preprocess_naive_turns(chat_data, column_names):
	conversation_id = column_names['conversation_id_col']
	speaker_id = column_names['speaker_id_col']
	message = column_names['message_col']
	# Combine adjacent rows of the same speaker in the same conversation
	
	# Generate 'turn_id' per chat per conversation, dependent on the active speaker
	turn_id_per_conv = chat_data.groupby([conversation_id], sort=False).apply(lambda df : get_turn_id(df, speaker_id))
	turn_id_per_conv = turn_id_per_conv.to_frame().reset_index().rename(columns={0:'turn_id'})
	chat_data = pd.concat([chat_data, turn_id_per_conv["turn_id"]], axis=1)
	
	# Use turn_id to compress messages with the same turn id per conversation
	chat_data = chat_data.groupby(conversation_id, sort=False).apply(lambda df : df.groupby('turn_id', as_index=False).apply(lambda x: compress(x, message))).reset_index(drop=True)
	
	return chat_data

def get_turn_id(df, speaker_id) :
	df["speaker_nickname_x"] = df[speaker_id].shift()
	return (df[speaker_id] != df["speaker_nickname_x"]).cumsum()
	
def compress(turn_df, message):
	result = turn_df.iloc[0]
	if (len(turn_df) > 1):
		result[message] = turn_df[message].str.cat(sep=' ')
		result['message_lower_with_punc'] = turn_df['message_lower_with_punc'].str.cat(sep=' ')
	return result

def create_cumulative_rows(input_df, conversation_id, within_task = False):
	"""
	function: create_cumulative_rows

	This function takes a chat-level dataframe and duplicates rows such that we can analyze
	convesations in the context of what came before.

	For example, rather than analyzing only the chats from a single stage, this function makes it possible
	to also incorporate chats from previous stages / tasks in the same conversation.
	
	@param conversation_id: The ID (stage or round) that the user wants to group on.
	@param within_task (defaults to False). This parameter determines whether we want to restrict
	the analysis only to chats that were of the same task (e.g., same `roundId`). By default, we look at 
	every chat that came before, regardless of the task.
	"""

	# If the conversation_id is the gameId, return as is -- no changes requred
	if(conversation_id == "gameId"): return input_df

	result_df = pd.DataFrame(columns=input_df.columns)

	# prev stageId
	prev_stageId = None

	# Iterate through rows
	for index, current_row in input_df.iterrows():
			
		# current stageId
		if current_row["stageId"] != prev_stageId: # we have transitioned to a new stageId

			prev_stageId = current_row["stageId"]

			if(conversation_id == 'stageId'):
				# Duplicate rows from all previous stageId's with the same 'gameId'
				if(within_task): # ensure roundId's are the same
					previous_rows = input_df.loc[(input_df['stageId'] != current_row['stageId']) & (input_df['timestamp'] < current_row['timestamp']) & (input_df['gameId'] == current_row['gameId']) & (input_df['roundId'] == current_row['roundId'])].copy()
				else:
					previous_rows = input_df.loc[(input_df['stageId'] != current_row['stageId']) & (input_df['timestamp'] < current_row['timestamp']) & (input_df['gameId'] == current_row['gameId'])].copy()
				if(not previous_rows.empty):
					previous_rows['cumulative_Id'] = current_row["stageId"]
					result_df = pd.concat([result_df, previous_rows], ignore_index=True)
			if(conversation_id == 'roundId'):
				# Duplicate rows from all previous roundId's with the same gameId
				previous_rows = input_df.loc[(input_df['roundId'] != current_row['roundId']) & (input_df['timestamp'] < current_row['timestamp']) & (input_df['gameId'] == current_row['gameId'])].copy()
				if(not previous_rows.empty):
					previous_rows['cumulative_Id'] = current_row["roundId"]
					result_df = pd.concat([result_df, previous_rows], ignore_index=True)

			cur_Id_rows = input_df.loc[(input_df[conversation_id] == current_row[conversation_id])].copy()
			cur_Id_rows['cumulative_Id'] = current_row[conversation_id]
			# Concatenate the current row to the result DataFrame
			result_df = pd.concat([result_df, cur_Id_rows], ignore_index=True).drop_duplicates()

	return result_df
