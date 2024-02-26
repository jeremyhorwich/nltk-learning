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
#Give us the option to export the results

#Make predictions using trained model
#Tokenize the test data
#Convert as many of the unigrams as possible into POS using data from above
#Loop through the test data. For each word:
#   If our next word is part of a known trigram, use that
#   Otherwise if our next word is part of a known bigram, use that
#   Otherwise use our default value
#Afterwards, compare results against NLTK's POS tagger and spit out our accuracy