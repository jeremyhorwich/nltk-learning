#Determine if a sentence can be parsed more than one way

#Import the grammar

def importGrammar(fileName):
    grammar = open("grammars/" + fileName,"r")
    print(grammar.read())
    #Create a dictionary using left and right sides for value and key, respectively (maybe...)
    
#We go bottom up for this one.
#Check to see (broadly) if any elements of the lowest level can combine with neighboring elements in more than one way
#   For example: "elephant" -> N. N can be left-neighbored (Det N) to make NP or surrouned (Det N PP) to make NP. So
#   we will have to check whether its righthand neighbors can be combined to make a prepositional phrase
    
importGrammar("grouchoGrammar.txt")