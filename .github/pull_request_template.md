_Pull Request Template_:
If you are merging in a feature or other major change, use this template to check your pull request!

# Basic Info
What's this pull request about? 
> [WRITE A BRIEF DESCRIPTION HERE.]

# My PR Adds or Improves Documentation
If your feature is about documentation, ensure that you check the boxes relevant to you.

## Docstrings
- [ ] Docstrings: I have followed the proper documentation format (https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html; Google Format recommended).
- [ ] Docstrings: Every function in the file has a block quote comment with a description of the feature.
- [ ] Docstrings: Every input argument is documented.
- [ ] Docstrings: The output type is documented, along with a description of what the output is for.
- [ ] Docstrings: I have linked the feature under the Table of Contents (docs/source/features/index.rst)

## Feature Wiki
- [ ] Conceptual Wiki: I made a copy of the TEMPLATE (docs/source/features_conceptual/TEMPLATE.rst)
- [ ] Conceptual Wiki: I replaced the word TEMPLATE at the top of the file with the name of the feature (.. _TEMPLATE:) Please do NOT delete any of the punctuation (the `.._` and `:`) in the header, as this is important for referencing the feature in the Table of Contents!
- [ ] Conceptual Wiki: I have answered the six sections of the template to the best of my ability.
- [ ] Conceptual Wiki: I have linked the feature under the Table of Contents (docs/source/features_conceptual/index.rst).

## General Documentation
- [ ] My documentation is linked in a toctree.
- [ ] I have confirmed that `make clean` and `make html` do not generate breaking errors.

# My PR is About Adding a New Feature to the Code Repository

## Adding Feature to the Feature Dictionary
- [ ] I have edited the `feature_dictionary.py` file with an appropriate entry for my feature. Below is a sample entry; *I confirm that all fields are accurately filled out*.

```
  "Function Word Accommodation": {
    "columns": ["function_word_accommodation"],
    "file": "./features/word_mimicry.py",
    "level": "Chat",
    "semantic_grouping": "Variance",
    "description": "The total number of function words used in a given turn that were also used in the previous turn. Function words are defined as a list of 190 words from the source paper.",
    "references": "(Ranganath et al., 2013)",
    "wiki_link": "https://github.com/Watts-Lab/team-process-map/wiki/C.9-Mimicry:-Function-word,-Content-word,-BERT,-Moving",
    "function": ChatLevelFeaturesCalculator.calculate_word_mimicry,
    "dependencies": [],
    "preprocess": [],
    "vect_data": False,
    "bert_sentiment_data": False
  }
```
- [ ] If my feature is at the chat level, my dictionary entry is in the top half of the file; if my feature is at the conversation level, my dictionary entry is in the bottom half of the file (below the comment that says, `### Conversation Level`).

## Documentation
Did you document your feature? You should follow the same requirements as above:
- [ ] Docstrings: I have followed the proper documentation format (https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html; Google Format recommended).
- [ ] Docstrings: Every function in the file has a block quote comment with a description of the feature.
- [ ] Docstrings: Every input argument is documented.
- [ ] Docstrings: The output type is documented, along with a description of what the output is for.
- [ ] Docstrings: I have linked the feature under the Table of Contents (docs/source/features/index.rst)

## Code Basics
- [ ] My feature is a .py file.
- [ ] My feature uses snake case in the name. That means the name of the format is `my_feature`, NOT `myFeature` (camel case).
- [ ] My feature has the name, `NAME_features.py`, where NAME is the name of my feature.
- [ ] My feature is located in `src/features/`.

## Testing
- [ ] I have thought about test cases for my features, with inputs and expected outputs.
- [ ] I have added test cases for my feature under the `tests/` folder.
- [ ] My feature passes the automated testing suite.

The location of my tests are here:
> [PASTE LINK HERE]

If you check all the boxes above, then you ready to merge!
