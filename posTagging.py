from nltk.util import ngrams
from nltk.corpus import brown
from collections import Counter
import pickle
import os

def trainModel(mostCommonThreshold: int):
    unigramDefinitions, posCorpus = getSampleData()

    #Counter returns type of list of tuple with count at end, so in order to get mostCommonPOS we need first element of first tuple
    mostCommonPOS = str((Counter([unigram[1] for unigram in unigramDefinitions]).most_common(1))[0][0]).replace(",","")
    mostCommonUnigrams = Counter(unigramDefinitions).most_common(mostCommonThreshold)
    unigrams = filterUsefulNGrams(mostCommonUnigrams)

    mostCommonBigrams = getMostFrequestNGrams(posCorpus,mostCommonThreshold,2)
    bigrams = filterUsefulNGrams(mostCommonBigrams)

    mostCommonTrigrams = getMostFrequestNGrams(posCorpus,mostCommonThreshold,3)
    trigrams = filterUsefulNGrams(mostCommonTrigrams)

    return (mostCommonPOS, unigrams, bigrams, trigrams)

def getSampleData():
    brownTaggedWords = brown.tagged_words(categories="lore", tagset="universal")
    isolatedTags = [tag for (word,tag) in brownTaggedWords]
    return brownTaggedWords, isolatedTags

def getMostFrequestNGrams(tokenizedCorpus: list[str], mostCommonThreshold: int, nGram: int) -> Counter:
    modifiedCorpus = ["." for i in range(0,nGram - 1)]      #Padding the beginning so we count how the first sentence starts
    for token in tokenizedCorpus:
        if token.isalpha():
            modifiedCorpus.append(token.upper())
            continue
        for i in range(0,nGram - 1):
            modifiedCorpus.append(".")
    parsedNGrams = list(ngrams(modifiedCorpus,nGram))
    return Counter(parsedNGrams).most_common(mostCommonThreshold)

def filterUsefulNGrams(nGramsWithCounts: list[tuple]) -> dict:
    filteredNGramsWithCounts = dict()
    for gramCounter in nGramsWithCounts:
        gram = gramCounter[0]
        count = gramCounter[1]
        if not gram[-1].isalpha():
            continue
        if gram in filteredNGramsWithCounts: #This logic is just a little too long for me to want to put it in a dict comprehension
            frequencyOfPotentialReplacement = count
            frequencyOfExistingDefinition = filteredNGramsWithCounts[gram]
            if frequencyOfPotentialReplacement < frequencyOfExistingDefinition:
                continue
        filteredNGramsWithCounts[gram] = count
    #We don't need the counts anymore, so we can construct our dictionary based on existing information and prediction
    cleanNGramList = {gram[:-1]:gram[-1] for gram in filteredNGramsWithCounts}
    return cleanNGramList

def exportModel(trainedModel,fileName: str) -> None:
    with open(os.path.join("tmp", fileName + ".pkl"),"wb") as export:
            pickle.dump(trainedModel,export)
    return

def importModel(fileName: str) -> tuple:
    with open(os.path.join("tmp",fileName + ".pkl"),"rb") as importedModel:
        trainedModel = pickle.load(importedModel)
    return trainedModel

def testModel(trainedModel):
    wordsToTag, accurateTags = getTestData()            #TODO: Why is the length of these lists when nonalpha'd different?
    predictedTags = tagWords(wordsToTag, trainedModel)
    accuracy = calculateAccuracyOfTags(accurateTags, predictedTags)
    print(accuracy)
    return

def getTestData():
    brownTaggedWords = brown.tagged_words(categories="news", tagset="universal")        #TODO: Simply split one category in two
    isolatedWords = [word for (word, tag) in brownTaggedWords]
    isolatedTags = [tag for (word,tag) in brownTaggedWords if word.isalpha()]
    return isolatedWords, isolatedTags

def tagWords(tokenizedWords: list[str], trainedModel) -> list[str]:
    defaultPOS, unigrams, bigrams, trigrams = trainedModel

    if defaultPOS is None or type(defaultPOS) is not str:
        raise Exception("Model in unexpected format")
    for object in (unigrams, bigrams, trigrams):
        if object is None or type(object) is not dict:
            raise Exception("Model in unexpected format")
    tags = list()
    for i, word in enumerate(tokenizedWords):
        if not word.isalpha():                  #Tagging punctuation will artificially inflate accuracy of results
            continue
        if word in unigrams:                    #We do unigrams first because direct POS definitions for each word are ideal
            tags.append(unigrams[word])
            continue
        if (tokenizedWords[i-1], word) in trigrams:
            tags.append(trigrams[[tokenizedWords[i-1], word]])
            continue
        if word in bigrams:
            tags.append(bigrams(word))
            continue
        tags.append(defaultPOS)
    return tags

#TODO: Why are we replacing all our words with the default? Look at above tagWords function. Also ending up with fewer tags than we started with. 

def calculateAccuracyOfTags(accurateTags: list[str], predictedTags: list[str]) -> float:
    accuratePredictions = 0
    for i in range(0,len(accurateTags)):
        if accurateTags[i] == predictedTags[i]:
            accuratePredictions += 1
    return (accuratePredictions / len(accurateTags))

#TODO: Wrap exporting and importing in simple command line inputs

def main():
    #trainedModel = trainModel(100)
    #exportModel(trainedModel,"model")
    trainedModel = importModel("model")
    testModel(trainedModel)
    return

if __name__ == "__main__":
    main()