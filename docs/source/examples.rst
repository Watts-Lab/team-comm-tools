.. _examples:

Getting Started Guide
======================

**Note:** This page is constantly being improved. This page is a work in progress!

Getting Started
****************

To use our tool, please ensure that you have Python >= 3.10 installed and a working version of `pip <https://pypi.org/project/pip/>`_, which is Python's package installer. Then, in your local environment, run the following:

.. code-block::

   pip install team_comm_tools


You will also need to manually install some additional required dependencies to set up the package. In your terminal, run the following:

.. code-block::
   
   ./setup.sh

Once complete, you should see, "Installation and requirements check completed successfully." This means you are ready to go!

Using the Package
******************

After you install it, the Team Communication Toolkit can be imported at the top of any Python script. We have provided a simple example file, "featurize.py", under our `examples folder <https://github.com/Watts-Lab/team_comm_tools/tree/main/examples>`_ on GitHub, and this walkthrough will highlight some of our top use cases. However, it won't follow the file exactly.

Importing the Package
++++++++++++++++++++++

At the top of your Python script, write the following:

.. code-block:: python
   
   from team_comm_tools import FeatureBuilder

Now you have access to the :ref:`feature_builder`. This is the main class that you'll need to interact with the Team Communication Toolkit.

Running the FeatureBuilder on Your Data
++++++++++++++++++++++++++++++++++++++++

Next, you'll want to get some data to run your FeatureBuilder on! The FeatureBuilder accepts any Pandas DataFrame as the input, so you can read in data in whatever format you like. For the purposes of this walkthrough, we'll be using some jury deliberation data from `Hu et al. (2021) <https://dl.acm.org/doi/pdf/10.1145/3411764.3445433?casa_token=d-b5sCdwpNcAAAAA:-U-ePTSSE3rY1_BLXy1-0spFN_i4gOJqy8D0CeXHLAJna5bFRTee9HEnM0TnK_R-g0BOqOn35mU>`_. 

We first import Pandas and read in the dataframe:

.. code-block:: python
   
   import pandas as pd
   juries_df = pd.read_csv("./example_data/full_empirical_datasets/jury_conversations_with_outcome_var.csv", encoding='utf-8')


Now we are ready to call the FeatureBuilder on our data. All we need to do is declare a FeatureBuilder object and run the .featurize() function, like this:

.. code-block:: python

	jury_feature_builder = FeatureBuilder(
		input_df = juries_df,
		speaker_id_col = "speaker_nickname",
		message_col = "message",
		timestamp_col = "timestamp",
		grouping_keys = ["batch_num", "round_num"],
		vector_directory = "./vector_data/",
		output_file_path_chat_level = "./jury_output_chat_level.csv",
		output_file_path_user_level = "./jury_output_user_level.csv",
		output_file_path_conv_level = "./jury_output_conversation_level.csv",
		turns = True
	)
	jury_feature_builder.featurize(col="message")

Basic Input Columns
^^^^^^^^^^^^^^^^^^^^

* The **input_df** parameter is where you pass in your dataframe. In this case, we want to run the FeatureBuilder on the juries data that we read in!

* The **speaker_id_col** refers to the name of the column containing a unique identifier for each speaker / participant in the conversation. Here, in the data, the name of our columns is called "speaker_nickname."

	* If you do not pass anything in, "speaker_nickname" is the default value for this parameter.

* The **message_col** refers to the name of the column containing the utterances/messages that you want to featurize. In our data, the name of this column is "message."

	* If you do not pass anything in, "message" is the default value for this parameter.

* The **timestamp_col** refers to the name of the column containing when each utterance was said. In this case, we have exactly one timestamp for each message, stored in "timestamp." 

	* If you do not pass anything in, "timestamp" is the default value for this parameter.

	* Sometimes, you may have data on both the *start* and the *end* of a message; when people are speaking live, it's possible that they talk over each other! In this case, the parameter **timestamp_col** also accepts a tuple of two strings, assumed to be *(start, end)*. For example, if we had two columns insteac, we could use the following:

	.. code-block:: python

		timestamp_col = ("timestamp_start", "timestamp_end")

* **In the FeatureBuilder, we assume that every conversation has a unique identifying string, and that all the messages belonging to the same conversation have the same identifier.** Typically, we would use the column **conversation_id_col** to indicate the name of this identifier. However, we also support cases in which there is more than one identifer per conversation, and our example here illustrates this functionality. The **grouping_keys** parameter means that we want to group by more than one column, and allow the FeatureBuilder to treat unique combinations of the grouping keys as the "conversational identifier". This means that we treat each unique combination of "batch_num" and "round_num" as a different conversation.

	* In cases where you are using **conversation_id_col**, "conversation_num" is the default value for this parameter.

	* If we were to use just one of the columns as our conversation identifier instead --- for example, treat each instance of "batch_num" as a unique conversation, we would use this syntax: 

	.. code-block:: python

		conversation_id_col = "batch_num"

* The **vector_directory** is the name of a directory in which we will store some pre-processed information. Some features require running inference from HuggingFace's `RoBERTa-based sentiment model <https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment>`_, and others require generating `SBERT vectors <https://sbert.net/>`_. These processes take time, and we cache the outputs so that subsequent runs of the FeatureBuilder on the same dataset will not take as much time. Therefore, we require you to pass in a location where you'd like us to save these outputs.

	* **Note that we do not require the name of the vector directory to be a folder that already exists**; if it doesn't exist, we will create it for you.

	* Inside the folder, we will store the RoBERTa outputs in a subfolder called "sentiment", and the SBERT vectors in a subfolder called "sentence." We will create both of these subfolders for you.

	* The **turns** parameter, which we will discuss later, controls whether or not you'd like the FeatureBuilder to treat successive utterances by the same individual as a single "turn," or whether you'd like them to be treated separately. We will cache different versions of outputs based on this parameter; we use a subfolder called "chats" (when **turns=False**) or "turns" (when **turns=True**).

* There are three output files for each run of the FeatureBuilder, which mirror the three levels of analysis: utterance-, speaker-, and conversation-level. (Please see the section on `Generating Features: Utterance-, Speaker-, and Conversation-Level <intro#generating_features>`_ for more details.) However, this means that we require you to provide a path for where you would like us to store each of the output files; **output_file_path_chat_level** (Utterance- or Chat-Level Features), **output_file_path_user_level** (Speaker- or User-Level Features), and **output_file_path_conv_level** (Conversation-Level Features).

	* We expect that you pass in a **path**, not just a filename. For example, the path needs to be "./my_file.csv", and not just "my_file.csv"; you will get an error if you pass in only a name without the "/".

	* Regardless of your path location, we will automatically append the name "output" to the fornt of your file path, such that **all of the outputs will be generated in a folder called "output."**

	* Within the "output" folder, **we will also generate sub-folders such that the three files will be located in subfolders called "chat," "user," and "conv," respectively.**

	* If you pass in a path that already contains the above automatically-generated elements (for example, "./output/chat/my_chat_features.csv"), we will skip these steps and directly save it in the relevant folder.

	* Similar to the **vector_directory** parameter, the "chat" directory will be renamed to "turn" depending on the value of the **turns** parameter.

	* This means that the following two ways of specifying an output path are equivalent, assuming that turns=False:

	.. code-block:: python

		output_file_path_chat_level = "./jury_output_chat_level.csv"

		output_file_path_chat_level = "./output/chat/jury_output_chat_level.csv"

	* And these two ways of specifying an output path are equivalent, assumign that turns=True:

	.. code-block:: python

		output_file_path_chat_level = "./jury_output_turn_level.csv"

		output_file_path_chat_level = "./output/turn/jury_output_turn_level.csv"

* The **turns** parameter controls whether we want to treat successive messages from the same person as a single turn. For example, in a text conversation, sometimes individuals will send many message in rapid succession, as follows:

	* **John**: Hey Michael

	* **John**: How are you?

	* **John**: I wanted to talk you real quick!

		* These messages by John can be thought of as a single turn, in which he says, "Hey Michael, how are you? I wanted to talk to you real quick!" Instead, however, John sent three messages in a row, suggesting that he took three "turns." When the **turns** parameter is set to True, the FeatureBuilder will automatically combine messages like this into a single "turn."

		* We note, however, that one of our features (`:ref:turn_taking_index`) will always give the value of "1" in the case when you set **turns=True**, since, by definition, people will never take multiple "turns" in a row.


Advanced Configuration Columns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
More advanced users of the FeatureBuilder should consider the following optional parameters, depending on their needs.

Customizing Sentence Vectors
""""""""""""""""""""""""""""""

* The **regenerate_vectors** parameter controls whether you'd like the FeatureBuilder to re-generate the content in the **vector_directory**, even if we have already cached the output of a previous run. It is useful if the underlying data has changed, but you want to give the output file the same name as a previous run of the FeatureBuilder.

	* By default, **we assume that, if your output file is named the same, that the underlying vectors are the same**. If this isn't true, you should set **regenerate_vectors = True** in order to clear out the cache and re-generate the RoBERTa and SBERT outputs.

* We currently support only the automatically-generated SBERT vectors as inputs to our vector-dependent features. A future update will add support for additional vector types.

Customizing the Generated Features
"""""""""""""""""""""""""""""""""""

* The **custom_features** parameter allows you to specify features that do not exist within our default set. **We currently default to NOT generating four features that depend on SBERT vectors, as the process for generating the vectors tends to be slow.** However, these features can provide interesting insights into the extent to which individuals in a conversation speak "similarly" or not, based on a vector similarity metric. To access these features, simply use the **custom_features** parameter:

	.. code-block:: python

		custom_features = [
            "(BERT) Mimicry",
            "Moving Mimicry",
            "Forward Flow",
            "Discursive Diversity"]


    * You can chose to add any of these features depending on your preference.

* The parameters **ner_training_df** and **ner_cutoff** are required if you would like the FeatureBuilder to identify named entities in your conversations. For example, the sentence, "John, did you talk to Michael this morning?" has two named entities: "John" and "Michael." The FeatureBuilder includes a tool that automatically detects these named entities, but it requires the user (you!) to specify some training data with examples of the types of named entities you'd like to recognize. This is because proper nouns can take many forms, from standard Western-style names (e.g., "John") to pseudonymous online nicknames (like "littleHorse"). More information about these parameters can be found in :ref:`named_entity_recognition`.

Customizing What Counts as a "Conversation"
""""""""""""""""""""""""""""""""""""""""""""

* The **analyze_first_pct** parameter allows you to "cut off" and separately analyze the first X% of a conversation, in case you wish to separately study different sections of a conversation as it progresses. For example, you may be interested in knowing how the attributes of the first 50% of a conversation differ from the attributes of the entire conversation. Then you can sepcify the following:

	.. code-block:: python

		analyze_first_pct: [0.5, 1.0]

	* This will first analyze the first 50% of each conversation, and then analyze the full conversation.

	* By default, we will simply analyze 100% of each conversation.

* The parameters **cumulative_grouping** and **within_task** address a special case of having multiple conversational identifiers; **they assume that the same team has multiple sequential conversations, and that, in each conversation, they perform one or more separate activities**. This was originally created as a companion to a multi-stage Empirica game (see: `<https://github.com/Watts-Lab/multi-task-empirica>`_). For example, imagine that a team must complete 3 different tasks, each with 3 different subparts. Then we can model this event in terms of 1 team (High level), 3 tasks (Mid level), and 3 subparts per task (Low level).

	* In such an activity, we assume that there are three levels of identifiers: High, Mid, and Low.

	* The "High" level identifier can be thought of as the team's identifier, and the same team then completes multiple different activities (or has multiple different conversations), each with one or more subparts. 

	* The "Mid" level identifier is a sequence of separate conversations about different topics.

	* The "Low" level identifier assumes that, within each topic, there are one or more subparts/subtasks. For example, suppose that teams must discuss three different political issues (Gun Control, Death Penalty, and Abortion), and within each topic, they need to discuss it from two perspectives (Democrat, Republican). In this case, there would be an identifier for each of the 3 Mid-level activities (political issues), and for each Low-level subpart (Democrat/Republican).

	* If your activity does not have any subparts, set your Low-level identifier equal to the Mid-level identifier.

	* The **cumulative_grouping** parameter accounts for the case in which, in such a nested sequence of conversations, you may want to count a team's previous conversations as "part" of the current conversation. For example, suppose that the team first discussed the Gun Control issue, and then moves on to discuss the Death Penalty issue. You may imagine that a heated discussion about Gun Control might impact the later discussion about the Death Penalty, and you may want to incorporate the previous topic when analyzing the second conversation. **In effect, the cumulative_grouping paramter creates a duplicate of the "earlier" conversation and groups it with the later conversation, so that analyses of sequential conversations can incorporate information from what happened before.**

		* Thus, without **cumulative_grouping**, we would have 6 independent conversations:

			#. Gun Control, Democrat

			#. Gun Control, Republican

			#. Death Penalty, Democrat

			#. Death Penalty, Republican

			#. Abortion, Democrat

			#. Abortion, Republican

		* But with **cumulative_grouping = True**, we would have the following conversations, in which we treat each conversation as building on the last one:

			#. Gun Control, Democrat

			#. Gun Control, Democrat; Gun Control, Republican

			#. Gun Control, Democrat; Gun Control, Republican; Death Penalty, Democrat

			#. Gun Control, Democrat; Gun Control, Republican; Death Penalty, Democrat; Death Penalty, Republican

			#. Gun Control, Democrat; Gun Control, Republican; Death Penalty, Democrat; Death Penalty, Republican; Abortion, Democrat

			#. Gun Control, Democrat; Gun Control, Republican; Death Penalty, Democrat; Death Penalty, Republican; Abortion, Democrat; Abortion, Republican

	* A further consideration is that the user may only wish to make a conversation "cumulative" at the Mid level, but not across all Mid levels. For example, extending the political discussion case, you may think that discussing the Democratic perspective on the same issue might influence the discussion of the Republican perspective, but you may think the Gun Control, Death Penalty, and Abortion issues are separate topics that should not be treated as the same "conversation." In this case, setting **within_task = True** would combine conversations at the "Low" level, but would not combine conversations at the "Mid" level.

		* Thus, with **cumulative_grouping = True**, we would have the following conversations:
			
			#. Gun Control, Democrat

			#. Gun Control, Democrat; Gun Control, Republican

			#. Death Penalty, Democrat

			#. Death Penalty, Democrat; Death Penalty, Republican

			#. Abortion, Democrat

			#. Abortion, Democrat, Abortion, Republican

	* Finally, it is important to remember that, since cumulative groupings mean that we progressively consider more and more of the same conversation, **your conversation dataframe will substantially increase in size**, and this may affect the runtime of your FeatureBuilder.


Customizing Feature Aggregations.
"""""""""""""""""""""""""""""""""""

* As we write in :ref:`_features_technical`, we compute aggregations of utterance-level features at chat- and speaker-level. That is, for every utterance-level feature (e.g., "number of words"), we compute metrics for that feature at the level of a conversation (e.g., "total number of words in this conversation") and at the level of an individual speaker in the conversation (e.g., "total number of words spoken by Bob").

* By default, **we aggregate all numeric columns, and we use the following four aggregation functions: Mean, Max, Min, Standard Deviation.** 

* However, it is possible to change the default by using the following six optional parameters:

	#. **convo_aggregation:** If this parameter is True, we will aggregate features at the conversational level; flip this parameter to False if you would NOT like to generate any aggregated :ref:`_conv_level_features`. Note that non-aggregated features (for example, Gini Coefficient, Information Diversity, Turn-Taking Index, and Burstiness) will still appear at the conversation level.

   #. **convo_methods:** Specifies which functions you want to aggregate at the conversation level (e.g., mean, std...).

   #. **convo_columns:** Specifies which features (at the utterance/chat level) users want aggregated for the conversational level. Defauts to all all numeric columns.

   #. **param user_aggregation:** If this parameter is True, we will aggregate features at the speaker/user level; flip this parameter to False if you would NOT like to generate any :ref:`_user_level_features`.

   #. **param user_methods:** Specifies which functions you want to aggregate at the speaker/user level (e.g., mean, std...).

   #. **param user_columns:** Specifies which features (at the utterance/chat level) you want to aggregate at the speaker/user level (e.g., mean, std...).


* Here is an example of how to user the parameters to turn off aggregation entirely:

	.. code-block:: python






Additional FeatureBuilder Considerations
++++++++++++++++++++++++++++++++++++++++

Here are some additional design details of the FeatureBuilder that you may wish to keep in mind:

	* **Outside of the required columns (Conversation Identifier, Speaker Identifier, Message, and Timestamp), the FeatureBuilder will ignore any remaining columns in your conversation data.** The FeatureBuilder strictly *appends* new columns to the input dataset. We made this design decision so that researchers can run the FeatureBuilder and conduct additional analyses (e.g, regression) directly on the output; for example, you may have additional information (metadata, outcome variables) included in your input dataframe that you want to analyze alongside the conversation features. We will not touch them.

		* The only caveat to this rule is if you happen to have a column that is named exactly the same as one of the conversation features that we generate. In that case, your column will be overwritten. Please refer to `<https://teamcommtools.seas.upenn.edu/HowItWorks>`_ for a list of all the features we generate, along with their column names.

	* **When summarizing features from the utterance level to the conversation and speaker level, we only consider numeric features.** This is perhaps a simplifying assumption more than anything else; although we do extract non-numeric information (for example, a Dale-Chall label of whether an utterance is "Easy" to ready or not; a list of named entities identified), we cannot summarize these efficiently, so they are not considered.
