from nltk.util import ngrams
from collections import Counter

#Train using existing data

def getSampleData():
    #Use Brown corpus for data
    pass

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

def createPOSDefinitionsFromNGrams():
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