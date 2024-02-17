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
     

def detectAmbiguity(sentence, grammar):
    sentence = sentence.strip(" .!").lower()
    phraseList = sentence.split()

    rulesByPhraseType = dict()
    for i in range(len(phraseList)):
        phraseList[i] = grammar[phraseList[i]]
        if phraseList[i] not in rulesByPhraseType:
            rulesByPhraseType[phraseList[i]] = findRulesByPhraseType(grammar, phraseList[i])
    print(rulesByPhraseType["NP"])

def findRulesByPhraseType(grammar, phrase):
    rulesAppliedToPhrase = list()
    for rule in grammar:
        if phrase in rule.split():
            rulesAppliedToPhrase.append(rule)
    return rulesAppliedToPhrase

grammar = importGrammar("grouchoGrammar.txt")
detectAmbiguity("I shot an elephant in my pajamas",grammar)

#Step 1: Loop through sentence and replace all of the words with their linguistic abstraction
#Step 2: We check each element in the list (each current unit of abstraction)
#   For each unit, we mark down how many combinations it is applicable to in the grammar against the current list
#   If no combinations, we skip (ie. N next to V) to the next linguistic unit
#   If only one combination, combine. But we must check against a combination that might not exist yet (see Det N PP)
#   If two combinations, then we break and return a fail
#Step 3: Create a new list and run through the loop again
#Step 4: If our list has only one element (meaning we've created an unambiguous sentence) then we quit loop and return success
    
#We have to loop through all keys in the dictionary
    

