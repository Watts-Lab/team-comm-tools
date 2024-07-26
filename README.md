# The Team Communication Toolkit
The Team Communication Toolkit is a research project and Python package that aims to make it easier for social scientists to explore text-based conversational data.

## Getting Started

If you are new to this repository, welcome! Please follow the steps below to get started.

### Step 1: Clone the Repo
First, clone this repository into your local development environment: 

```
git clone https://github.com/Watts-Lab/team-comm-tools.git
```

### Step 2: Download Dependencies
Second, we *strongly* recommend using a virtual environment to install the dependencies required for the project.=
The dependencies of the project are listed in `src/requirements.txt`: https://github.com/Watts-Lab/team-comm-tools/blob/main/src/requirements.txt

**Python Version**: We recommend `python3.11` when running this repository.

Later versions of Python (e.g., 3.12) are currently incompatible with the `sentence-transformers` library. There is an open issue here: https://github.com/google/sentencepiece/issues/968 [Updated as of January 30, 2024]

#### Run Initial Scripts for Dependencies
Before starting the featurizer, you need to run the following to obtain dependencies for the project:

```
python3 -m spacy download en_core_web_sm
```
```
import nltk
nltk.download('nps_chat')
nltk.download('punkt')
```

### Step 3: Run the Featurizer
At this point, you should be ready to run the featurizer! Navigate to the `examples` folder, and use the following command:

```
python3 featurize.py
```
This calls the `featurizer.py` file, which declares a FeatureBuilder object for different dataset of interest, and featurizes them using our framework. The `featurize.py` file provides an end-to-end worked example of how you can declare a FeatureBuilder and call it on data; equally, you can replace this file with any file / notebook of your choosing, as long as you import the FeatureBuilder module.

## Contributing Code and Automated Unit Testing
If you would like to contribute to the repository, we have implemented a [Pull Request Template](https://github.com/Watts-Lab/team-comm-tools/blob/main/.github/pull_request_template.md) with a basic checklist that you should consider when adding code (e.g., improving documentation or developing a new feature).

We have also implemented automated unit testing of all code (which runs upon every push to GitHub), allowing us to ensure that new features function as expected and do not break any previous features. The points below highlight key steps to using our automated test suite.

1. Draft test inputs (`conversation_num`, `speaker`, `message`) and expected outputs for your feature. 

- For example,  "This is a test message." should return 5 for `num_words` at the chat level (note that `conversation_num` and `speaker` have no effect on the ultimate result, so they can be chosen arbitrarily).
- Testing a conversation level feature, say `discursive_diversity`, requires a series of chats rather than just one chat. For example, "This is a test message." (speaker 1), "This is a test message." (speaker 1), "This is a test message." (speaker 2), "This is a test message." (speaker 2), within the same conversation, should return 0. Note that the `conversation_num` for each new test should be distinct from all previous `conversation_num`, even if the feature being tested is different.

2. Once you have test inputs, add each CHAT (and its associated conversation_num and speaker) as a separate row in either `test_chat_level.csv` or `test_conv_level.csv`, within `./src/testing/data/cleaned_data`. The format of the CSV is as follows: `id, conversation_num, speaker_nickname, message, expected_column, expected_value`, where `expected_column` is the feature name (i.e. num_words).

3. Push all your changes to GitHub, including feature development and test dataset additions. Go under the "Actions" tab in the toolbar. Notice there's a new job running called "Testing-Features". A green checkmark at the conclusion of this job indicates all new tests have passed. A red cross means some test has failed. Navigate to the uploaded "Artifact" (near the bottom of the status page) for list of failed tests and their associated inputs/outputs.

4. Debug and iterate!
