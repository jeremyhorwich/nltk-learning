from nltk.util import ngrams
from nltk.corpus import brown
from collections import Counter

def trainModel(mostCommonThreshold: int):
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

def getMostFrequestNGrams(tokenizedCorpus: list[str], mostCommonThreshold: int, nGram: int) -> Counter:
    modifiedCorpus = ["." for i in range(0,nGram - 1)]      #Padding the beginning so we count how the first sentence starts
    for token in tokenizedCorpus:
        if token.isalpha():
            modifiedCorpus.append(token.lower())
            continue
        for i in range(0,nGram - 1):
            modifiedCorpus.append(".")
    parsedNGrams = list(ngrams(modifiedCorpus),nGram)
    return Counter(parsedNGrams).most_common(mostCommonThreshold)

def filterUsefulNGrams(nGramsWithCounts: list[str]) -> dict:
    filteredNGramsWithCounts = dict()
    for gram in nGramsWithCounts:
        if not gram[-1].isalpha():
            continue
        if gram in filteredNGramsWithCounts: #This logic is just a little too long for me to want to put it in a dict comprehension
            frequencyOfPotentialReplacement = nGramsWithCounts[gram]
            frequencyOfExistingDefinition = filteredNGramsWithCounts[gram]
            if frequencyOfPotentialReplacement < frequencyOfExistingDefinition:
                continue
        filteredNGramsWithCounts[gram] = nGramsWithCounts[gram]
    #We don't need the counts anymore, so we can construct our dictionary based on existing information and prediction
    cleanNGramList = {gram[:-1]:gram[-1] for gram in filteredNGramsWithCounts}
    return cleanNGramList

#Give us the option to export the results

def testModel():
    pass

def getTestData():
    #Tokenize the test data
    pass

def tagWords(tokenizedWords: list[str], defaultPOS: str, unigrams: dict, bigrams: dict, trigrams: dict) -> list[str]:
    tags = list()
    for i, word in enumerate(tokenizedWords):
        if word in unigrams:
            tags.append(unigrams[word])
            continue
        if [tokenizedWords[i-1], word] in trigrams:
            tags.append(trigrams[[tokenizedWords[i-1], word]])
            continue
        if word in bigrams:
            tags.append(bigrams(word))
            continue
        tags.append(defaultPOS)
    return tags
    #Convert as many of the unigrams as possible into POS using data from above
    #Loop through the test data. For each word:
    #   If our next word is part of a known trigram, use that
    #   Otherwise if our next word is part of a known bigram, use that
    #   Otherwise use our default value
    pass

def calculateAccuracyOfTags():
    #Afterwards, compare results against NLTK's POS tagger and spit out our accuracy
    pass