.. _word_ttr:

Word Type-Token Ratio
=====================

High-Level Intuition
*********************
This feature measures the ratio of the number of unique words ("types") to the total number of words ("tokens") is an utterance. This is a standard measure of `lexical density <https://en.wikipedia.org/wiki/Lexical_density>`_.

Citation
*********
`Reichel, et al. (2015) <https://cpb-us-e1.wpmucdn.com/sites.northwestern.edu/dist/f/1603/files/2017/01/Reichel_etal_Interspeech_2015-2i4gnzk.pdf>`_

`Williamson (2009) <https://www.sltinfo.com/wp-content/uploads/2014/01/type-token-ratio.pdf>`_

Implementation Basics 
**********************
The Type-Token Ratio is calculated as follows: Number of Unique Words / Number of Total Words.

The function assumes that punctuation is retained when being inputted, but parses it out within the function.

Interpreting the Feature 
*************************
A low type-token ratio indicates that an individual is using many of the same words over and over; for example, if an individual is speaking with great hesitation, repeating themselves, or using filler and functional words ("um", "that is", "the"), there will be fewer unique words relative to the total number of words. Individuals who choose their words carefully, with minimal repetition, will tend to have a higher type-token ratio. The mode of communication can also impact lexical density; individuals typically have a lower type-token ratio when speaking out loud than when writing.

Related Features 
*****************
N/A