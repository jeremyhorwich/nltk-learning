from nltk.util import ngrams
from nltk.corpus import brown
from collections import Counter

def trainModel(mostCommonThreshold):
    unigramDefinitions, posCorpus = getSampleData()

    mostCommonPOS = Counter([unigram[1] for unigram in unigramDefinitions]).most_common(1)
    mostCommonUnigrams = Counter(unigramDefinitions).most_common(mostCommonThreshold)
    unigrams = filterUsefulNGrams(mostCommonUnigrams)

    mostCommonBigrams = getMostFrequestNGrams(posCorpus,mostCommonThreshold,2)
    bigrams = filterUsefulNGrams(mostCommonBigrams)

    mostCommonTrigrams = getMostFrequestNGrams(posCorpus,mostCommonThreshold,3)
    trigrams = filterUsefulNGrams(mostCommonTrigrams)

    return mostCommonPOS, unigrams, bigrams, trigrams

def getSampleData():
    brownTaggedWords = brown.tagged_words(categories="lore", tagset="universal")
    isolatedTags = [tag for (word,tag) in brownTaggedWords]
    return brownTaggedWords, isolatedTags

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

def filterUsefulNGrams(nGramsWithCounts: list[str]) -> list:
    filteredNGramsWithCounts = dict()
    for gram in nGramsWithCounts:
        if not gram[-1].isalpha():
            continue
        if gram[:-1] in filteredNGramsWithCounts:
            frequencyOfPotentialReplacement = nGramsWithCounts[gram]
            frequencyOfExistingDefinition = nGramsWithCounts[filteredNGramsWithCounts[gram[:-1]]][1]
            if frequencyOfPotentialReplacement > frequencyOfExistingDefinition:
                filteredNGramsWithCounts[gram[:-1]] = [gram[-1],nGramsWithCounts[gram]]
    #We don't need the counts anymore
    cleanNGramList = {nGram:filteredNGramsWithCounts[nGram][0] for nGram in filteredNGramsWithCounts}
    return cleanNGramList

#Give us the option to export the results

#Make predictions using trained model
#Tokenize the test data
#Convert as many of the unigrams as possible into POS using data from above
#Loop through the test data. For each word:
#   If our next word is part of a known trigram, use that
#   Otherwise if our next word is part of a known bigram, use that
#   Otherwise use our default value
#Afterwards, compare results against NLTK's POS tagger and spit out our accuracy