#Train using existing data
#Use Brown corpus for data
#Take 100 most common of each type:
# Trigram
# Bigram
# Unigram
#   Track the frequency of each n-gram (prob with dictionary where dict[n-gram] = frequency
#   Look into Counter from collections
#   At the end of the loop, save the most common 100 to a dictionary

#Also count the most common unigram so we have a default value to fall back on

#Make predictions using trained model
#Tokenize the test data
#Convert as many of the unigrams as possible into POS using data from above
#Loop through the test data
#   Using the trigrams, convert as many to POS as possible
#   When no more trigrams are possible, convert as many to bigrams as possible
#   When no more bigrams are possible, use our default value
#       Should test one of two ways: Either we keep looping until no more n-gram is possible, then move onto n-1. OR do each type once.
#   Afterwards, compare results against NLTK's POS tagger and spit out our accuracy