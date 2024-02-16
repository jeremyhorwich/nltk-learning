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

grammar = importGrammar("grouchoGrammar.txt")
     
#Step 1: Loop through sentence and replace all of the words with their linguistic abstraction
#Step 2: We check each element in the list (each current unit of abstraction)
#   For each unit, we mark down how many combinations it is applicable to in the grammar against the current list
#   If no combinations, we skip (ie. N next to V) to the next linguistic unit
#   If only one combination, combine. But we must check against a combination that might not exist yet (see Det N PP)
#   If two combinations, then we break and return a fail
#Step 3: Create a new list and run through the loop again
#Step 4: If our list has only one element (meaning we've created an unambiguous sentence) then we quit loop and return success
    
#We have to loop through all keys in the dictionary
    

