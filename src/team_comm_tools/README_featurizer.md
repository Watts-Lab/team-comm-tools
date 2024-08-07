# Featurizer Documentation

The featurizer takes text conversations and transforms them into the following representations:

- A table of `chat-level features`, which generates a unique conversation feature for each chat (aka utterance, or message);
- A table of `conversation-level features`, which generates aggregations of features within each chat at the conversation level.
- A table of `user-level features`, which generates aggregations of features for each user, or speaker, in a conversation.

To set up and run the featurizer from scratch, you should do the following.

# Run the main featurizer [Do this every time you want to refresh/generate new features.]
- Declare a new FeatureBuilder object inside your Python file.
- Call the FeatureBuilder (using the `.featurize` command).