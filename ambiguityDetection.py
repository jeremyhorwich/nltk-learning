def main():
    grammar = importGrammar("grouchoGrammar.txt")
    #sentence = input("Enter sentence: ")
    sentence = "I shot an elephant"
    print(detectAmbiguityOfSentence(sentence,grammar))

def importGrammar(fileName):
    grammarFile = open("grammars/" + fileName,"r")
    grammar = dict()
    for line in grammarFile:
        rule = parseGrammarRule(line)
        grammar.update(rule)
    return grammar

def parseGrammarRule(lineOfGrammar):
    splitLHSandRHS = lineOfGrammar.split("->")
    if len(splitLHSandRHS) != 2:
        raise Exception("Grammar in unexpected format")
    
    grammarRule = dict()
    combinationResult = splitLHSandRHS[0].strip()
    combinations = splitLHSandRHS[1].split("|")

    for combination in combinations:
        grammarRule[combination.strip("' \n")] = combinationResult
    return grammarRule    

def detectAmbiguityOfSentence(sentence, grammar):
    sentence = sentence.strip(" .!").lower()
    phraseList = sentence.split()

    detectAmbiguity(phraseList, grammar)

def detectAmbiguity(phraseList, grammar, rulesByPhraseType=None):
    if len(phraseList) == 1:
        return False

    if rulesByPhraseType is None:
        rulesByPhraseType = dict()

    rulesToExecuteCheck = set()
    rulesToExecute = list()
    indexInSentence = 0    #I could loop using the index and save this pointer, but I think phrase is more readable than phraseList[i]
    for phrase in phraseList:
        if phrase not in rulesByPhraseType:   #Saving all relevant combinations (subset of full grammar) for time efficiency reasons
            rulesByPhraseType[phrase] = findRulesByPhraseType(grammar, phrase)
        
        validRules = list()
        for rule in rulesByPhraseType[phrase]:
            if isRuleValid(indexInSentence, phraseList, rule):
                validRules.append(rule)

        if len(validRules) > 1:
            return True
        if len(validRules) == 0:
            indexInSentence += 1
            continue
        ruleToAppend = (validRules[0],grammar[validRules[0]],indexInSentence - validRules[0].split().index(phrase))
        if ruleToAppend not in rulesToExecuteCheck:
            rulesToExecuteCheck.add(ruleToAppend)
            rulesToExecute.append(ruleToAppend)
        indexInSentence += 1

    if len(rulesToExecute) == 0:
        return True
    modifiedPhraseList = executeRules(phraseList,rulesToExecute)
    return detectAmbiguity(modifiedPhraseList, grammar, rulesByPhraseType=rulesByPhraseType)
    #TODO: Think about if this would all be easier by creating a Phrase class (with rules applicable, neighbors, etc properties)

def executeRules(phraseList, rulesAtPosition):
    newSentence = list()
    nextPositionToModify = 0
    for ruleAndPosition in rulesAtPosition:
        ruleSize = len(ruleAndPosition[0].split())
        combinationResult = ruleAndPosition[1]
        positionInSentence = ruleAndPosition[2]
        
        while nextPositionToModify < positionInSentence:
            newSentence.append(phraseList[nextPositionToModify])
            nextPositionToModify += 1
        newSentence.append(combinationResult)
        nextPositionToModify += ruleSize
    while nextPositionToModify < len(phraseList):
        newSentence.append(phraseList[nextPositionToModify])
        nextPositionToModify += 1
    return newSentence

def isRuleValid(phraseByIndex, phraseList, rule):
    splitRule = rule.split()

    ruleSize = 0
    phrasePositionInRule = 0
    for phrase in splitRule:
        if phrase == phraseList[phraseByIndex]:
            phrasePositionInRule = ruleSize
        ruleSize += 1

    #Check appropriate elements of the sentence against our rule

    elementsChecked = 0
    while (elementsChecked < ruleSize):
        indexOfPhraseInSentence = phraseByIndex - phrasePositionInRule + elementsChecked
        if (indexOfPhraseInSentence < 0) or (indexOfPhraseInSentence >= len(phraseList)):
            return False
        if (phraseList[indexOfPhraseInSentence] != splitRule[elementsChecked]):
            return False
        elementsChecked += 1
    return True
                
def findRulesByPhraseType(grammar, phrase):
    rulesAppliedToPhrase = list()
    for rule in grammar:
        if phrase in rule.split():
            rulesAppliedToPhrase.append(rule)
    return rulesAppliedToPhrase

if __name__ == "__main__":
    main()


#New algorithm:
#Perform every rule available every time. If the sentence turns out not to work then we say it is ambiguous