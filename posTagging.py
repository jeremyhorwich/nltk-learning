from nltk.util import ngrams
from nltk.corpus import brown
from collections import Counter

#Train using existing data

def trainModel():
    #Get sample data (in two parts as described below)
    #Clean 100 most common (w,t pairings)
    #Clean bigram and trigram pairings
    #Return: 100 most common of (unigram -> POS), (bigram), (trigram)
    pass

def getSampleData():
    brownTaggedWords = brown.tagged_words(categories="lore", tagset="universal")
    isolatedTags = [tag for (word,tag) in brownTaggedWords]
    return brownTaggedWords, isolatedTags

'''
Looks like we need this information two ways:

(1) We need the 100 most common (w, t) pairings
(2) For (w1,t1),(w2,t2),...,(wN,tN) we need (t1,t2,...tN)
'''

getSampleData()

def getMostFrequestNGrams(tokenizedCorpus: list[str], mostCommonThreshold: int, nGram: int) -> list[str]:
    modifiedCorpus = ["." for i in range(0,nGram - 1)]      #Padding the beginning so we count how the first sentence starts
    for token in tokenizedCorpus:
        if token.isalpha():
            modifiedCorpus.append(token.lower())
            continue
        for i in range(0,nGram - 1):
            modifiedCorpus.append(".")
    parsedNGrams = list(ngrams(modifiedCorpus),nGram)
    return Counter(parsedNGrams).most_common(mostCommonThreshold)

def createPOSDefinitionsFromNGrams(nGrams: list) -> list:
    #Discard any entries which describe the end of a sentence (any whose definition is a period)
    #Need to handle case of gram with more than one definition (take definition with greater frequency - just check
    #if it is already in the return dictionary and compare its frequency with that in the return)
    pass


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