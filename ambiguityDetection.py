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

def detectAmbiguity(sentence, grammar):
    sentence = sentence.strip(" .!").lower()
    phraseList = sentence.split()

    rulesByPhraseType = dict()

    rulesToExecute = []
    indexInSentence = 0    #I could loop using the index and save this pointer, but I think phrase is more readable than phraseList[i]
    for phrase in phraseList:
        if phrase not in rulesByPhraseType:   #Saving all relevant combinations (subset of full grammar) for time efficiency reasons
            rulesByPhraseType[phrase] = findRulesByPhraseType(grammar, phrase)
        
        numberOfPossibleRules = len(findRulesByPhraseType[phrase])
        validRules = 0
        for rule in rulesByPhraseType[phrase]:
            if isRuleValid(indexInSentence, sentence, rule):
                validrules += 1

        if (numberOfPossibleRules == 1) and (validRules == 1):
            applicableRule = rulesByPhraseType[phrase][0]
            rulesToExecute.append(applicableRule,grammar[applicableRule],indexInSentence)
        if (validRules == 2):
            return True
        if (numberOfPossibleRules > 1):
            phrasesWithMultiplePossibilities.append(phrase)
        indexInSentence += 1

#Step 1: Check each element of the list
#Step 2: Check how many combinations it has
#   If it has 1 combination, combine.
#   If it has 2 available combinations, break and fail
#   If it has "1.5" an available combination and a currently unavailable combination, add it to another list (1.5 list)
#Step 3: Make new list (send grammar rules to be executed to a function which handles it)
#   If this new list is the same as the one before, then check your "1.5 list"
#       If there are no elements in the list (nothing can be changed) return an exception (unsolveable with current grammar, etc.)
#       If your 1.5 list has only one element, execute the available grammar rule for that element and make a new list
#       If this list has more than one element, we copy the sentence and perform the algorithm for each copied sentence (via recursion)
#Step 4: Return the result of the same function with the new argument of the new sentence (recursion)

def executeRules(sentence, rulesAtPosition):
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
            if phrase == sentence[positionInSentence]:
                anchorPositionInRule = ruleSize
            ruleSize += 1
        ruleStart = positionInSentence - anchorPositionInRule
        
        while nextPositionToModify < ruleStart:
            newSentence.append(sentence[nextPositionToModify])
            nextPositionToModify += 1
        newSentence.append(combinationResult)
        nextPositionToModify += ruleSize
    while nextPositionToModify < len(sentence) - 1:
        newSentence.append(sentence[nextPositionToModify])

def isRuleValid(phraseByIndex, sentence, rule):
    splitRule = rule.split()

    ruleSize = 0
    phrasePositionInRule = 0
    for phrase in splitRule:
        if phrase == sentence[phraseByIndex]:
            phrasePositionInRule = ruleSize
        ruleSize += 1

    #Check appropriate elements of the sentence against our rule

    elementsChecked = 0
    while (elementsChecked < ruleSize):
        if (sentence[phraseByIndex - phrasePositionInRule + elementsChecked] == rule[elementsChecked]):
            return False
    return True
            

#TODO: Think about if this would all be easier by creating a Phrase class (with rules applicable, neighbors, etc properties)
    
def findRulesByPhraseType(grammar, phrase):
    rulesAppliedToPhrase = list()
    for rule in grammar:
        if phrase in rule.split():
            rulesAppliedToPhrase.append(rule)
    return rulesAppliedToPhrase