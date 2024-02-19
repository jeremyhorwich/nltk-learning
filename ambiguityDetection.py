#Determine if a sentence can be parsed more than one way

#Import the grammar

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
     

# grammar = importGrammar("grouchoGrammar.txt")
# detectAmbiguity("I shot an elephant in my pajamas",grammar)

def detectAmbiguityOfSentence(sentence, grammar, rulesByPhraseType):
    sentence = sentence.strip(" .!").lower()
    phraseList = sentence.split()

    detectAmbiguity(phraseList, grammar, rulesByPhraseType)

def detectAmbiguity(phraseList, grammar, rulesByPhraseType):
    if len(phraseList) == 1:
        return False

    if rulesByPhraseType is None:
        rulesByPhraseType = dict()

    rulesToExecute = list()
    possibleAmbiguities = list()
    indexInSentence = 0    #I could loop using the index and save this pointer, but I think phrase is more readable than phraseList[i]
    for phrase in phraseList:
        if phrase not in rulesByPhraseType:   #Saving all relevant combinations (subset of full grammar) for time efficiency reasons
            rulesByPhraseType[phrase] = findRulesByPhraseType(grammar, phrase)
        
        numberOfPossibleRules = len(findRulesByPhraseType[phrase])
        validRules = list()
        for rule in rulesByPhraseType[phrase]:
            if isRuleValid(indexInSentence, phraseList, rule):
                validRules.append(rule)

        if (len(validRules) > 1):
            return True
        if (numberOfPossibleRules == 1) and (len(validRules) == 1):
            rulesToExecute.append(validRules[0],grammar[validRules[0]],indexInSentence)
        if (numberOfPossibleRules > 1):
            for rule in validRules:
                possibleAmbiguities.append(rule, grammar[rule],indexInSentence)
        indexInSentence += 1

    if len(rulesToExecute) > 0:
        modifiedPhraseList = executeRules(phraseList,rulesToExecute)
        return detectAmbiguity(modifiedPhraseList, grammar, rulesByPhraseType)
    for possibleAmbiguity in possibleAmbiguities:
        branchedPhraseList = executeRules(phraseList,possibleAmbiguity)
        if  detectAmbiguity(branchedPhraseList,grammar,rulesByPhraseType):
            return True
    return False

def executeRules(phraseList, rulesAtPosition):
    newSentence = list()
    nextPositionToModify = 0
    for ruleAndPosition in rulesAtPosition:
        splitRule = ruleAndPosition[0].split()
        combinationResult = ruleAndPosition[1]
        positionInSentence = ruleAndPosition[2]
        ruleSize = 0
        anchorPositionInRule = 0

        #If we ever have a rule with two of the same constituent this will break, but I can't find a real example for this edge case
        for phrase in splitRule:
            if phrase == phraseList[positionInSentence]:
                anchorPositionInRule = ruleSize
            ruleSize += 1
        ruleStart = positionInSentence - anchorPositionInRule
        
        while nextPositionToModify < ruleStart:
            newSentence.append(phraseList[nextPositionToModify])
            nextPositionToModify += 1
        newSentence.append(combinationResult)
        nextPositionToModify += ruleSize
    while nextPositionToModify < len(phraseList):
        newSentence.append(phraseList[nextPositionToModify])
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
        if (phraseList[phraseByIndex - phrasePositionInRule + elementsChecked] == rule[elementsChecked]):
            return False
    return True
            

#TODO: Think about if this would all be easier by creating a Phrase class (with rules applicable, neighbors, etc properties)
    
def findRulesByPhraseType(grammar, phrase):
    rulesAppliedToPhrase = list()
    for rule in grammar:
        if phrase in rule.split():
            rulesAppliedToPhrase.append(rule)
    return rulesAppliedToPhrase