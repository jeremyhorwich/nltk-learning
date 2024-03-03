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

def exportModel(trainedModel) -> bool:
    modelNameValid = False
    while (not modelNameValid):
        modelName = input("Save model as ")
        if modelName.lower() == "quit":
            break
        if not modelName.isalnum():
            print("Model name not alphanumeric")
            continue
        modelNameValid = True
    
    if not modelNameValid:
        return False
    
    modelPath = os.path.join("tmp", modelName + ".pkl")

    if os.path.isfile(modelPath):
        os.remove(modelPath)

    with open(modelPath,"wb") as export:
            pickle.dump(trainedModel,export)
    return

def importModel(fileName: str) -> tuple:
    filePath = os.path.join("tmp",fileName + ".pkl")

    if not os.path.isfile(filePath):
        return None

    with open(filePath,"rb") as importedModel:
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
    i = -1                                          #We'll start at i=0 when we hit our first alpha word
    for word in tokenizedWords:
        if not word.isalpha():                      #Tagging punctuation will artificially inflate accuracy of results
            continue
        i += 1
        word = word.lower()
        if (word,) in unigrams:                     #We do unigrams first because direct POS definitions for each word are ideal
            tags.append(unigrams[(word,)])
            continue
        if (tags[i-2], tags[i-1]) in trigrams:
            tags.append(trigrams[(tags[i-2], tags[i-1])])
            continue
        if (tags[i-1],) in bigrams:
            tags.append(bigrams[(tags[i-1],)])
            continue
        tags.append(defaultPOS)
    return tags

def calculateAccuracyOfTags(accurateTags: list[str], predictedTags: list[str]) -> float:
    accuratePredictions = 0
    for i in range(0,len(accurateTags)):
        if accurateTags[i] == predictedTags[i]:
            accuratePredictions += 1
    return (accuratePredictions / len(accurateTags))

def getModelFromUserInput():
    trainingModelFound = False
    while (not trainingModelFound):
        modelYN = input("Import model? Y/N ")
        if modelYN.lower() == "quit":
            break
        if modelYN.lower() == "y":
            modelName = input("Name of model? ")
            if modelName.lower() == "quit":
                break
            trainedModel = importModel(modelName)
            if trainedModel is None:
                print("Model not found")
                continue
            return trainedModel
        if modelYN.lower() == "n":
            modelLength = input("Model length? ")
            if modelLength.lower() == "quit":
                break
            if not modelLength.isdigit():
                print("Enter an integer")
                continue
            modelLength = int(modelLength)
            if not 0 < modelLength < 5000:
                print("Model length not in acceptable range")
                continue
            trainedModel = trainModel(modelLength)
            exportModelYN = input("Export model? Y for export ")
            if exportModelYN.lower() == "y":
                exportModel(trainedModel)
            return trainedModel
    return None

def main():
    trainedModel = getModelFromUserInput()
    if trainedModel is None:
        return
    testModel(trainedModel)
    #trainedModel = trainModel(100)
    #exportModel(trainedModel,"model")
    #trainedModel = importModel("model")
    return

if __name__ == "__main__":
    main()