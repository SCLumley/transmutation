import re
import random
import colorama
import sys
from colorama import Fore

random.seed(42645)

ingredients = ["b","a","q","l","p","n"]
mandatoryEffects = [
    "1 Gold",
    "1 Brimstone Powder",
    "1 Aqua Forte",
    "1 Quicksilver",
    "1 Lead Dust",
    "1 Phosphoric Salt",
    "1 Nitre",
    "The Mixture has Essence of Mind",
    "The Mixture has Essence of Body",
    "The Mixture has Essence of Spirit"
]

optionalEffects = [
    "2 Dice",
    "2 Dice",
    "2 Dice",
    "2 Dice",
    "3 Gold",
    "3 Gold",
    "6 Gold",
    "You have found Brimstone Powder has this many lateral reactions :",
    "You have found Aqua Forte has this many lateral reactions :",
    "You have found Quicksilver has this many lateral reactions :",
    "You have found Lead Dust has this many lateral reactions :",
    "You have found Phosphoric Salt has this many lateral reactions:",
    "You have found Nitre has this many lateral reactions :"
    "You have found Brimstone Powder has this many vertical reactions :",
    "You have found Aqua Forte has this many vertical reactions :",
    "You have found Quicksilver has this many vertical reactions :",
    "You have found Lead Dust has this many vertical reactions :",
    "You have found Phosphoric Salt has this many vertical reactions :",
    "You have found Nitre has has this many vertical reactions :"
]

random.shuffle(optionalEffects)
NoptEffects=random.randrange(2,10)
effects = mandatoryEffects + optionalEffects[:NoptEffects]
vValence = [0,0,0,0,0,0]
lValence = [0,0,0,0,0,0]


def split(word):
    return [char for char in word]



def shufflesol(matrix):
    for effectIndex, effect in enumerate(effects):
        keepgoing = True
        while keepgoing:
            first = random.randrange(0,6)
            second = random.randrange(0, 6)
            if matrix[first][second] == 0 and matrix[second][first] == 0:
                matrix[first][second] = effectIndex + 1
                lValence[first] += 1
                vValence[second] += 1

                keepgoing = False
                break
    return matrix

def get_overlapping_pairs(string):
    ret = [] # we will return this later
    for i in range(len(string)-1): # loop through all indices except the last one
        ret.append(string[i:i+2]) # append to ret the two characters
                                  # beginning at that index
    return ret



solMatrix=[
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

exMatrix=[
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

###########Test


solMatrix = shufflesol(solMatrix)
#print(solMatrix)
recipeHistory=[]

# print("valencetest")
# print("b", 6 - solMatrix[0].count(0))
# print("a", 6 - solMatrix[1].count(0))
# print("q", 6 - solMatrix[2].count(0))
# print("l", 6 - solMatrix[3].count(0))
# print("p", 6 - solMatrix[4].count(0))
# print("n", 6 - solMatrix[5].count(0))

keepgoing = True
while keepgoing:
    mystring = input(Fore.WHITE + "Input recipe:\n")
    textcolour=""
    if mystring == "quit":
        keepgoing=False
        print("solution:\n")
        for n in solMatrix:
            print(n)
        i = 1
        for n in effects:
            print(i, ": ", n)
            i += 1
        break
    else:
        if mystring in recipeHistory:
            print("Sorry, you mixed that before. What you would get if you could mix it again:")
            textcolour=Fore.RED
        recipeHistory.append(mystring)
        pairs = get_overlapping_pairs(mystring)

        weakReactions = 0
        strongReactions = 0
        exhaustedReactions = 0
        products=[]
        nonProducts=[]
        for pair in pairs:
            first = ingredients.index(pair[0])
            second = ingredients.index(pair[1])
            if solMatrix[second][first] != 0 and second != first:
                weakReactions += 1
            if solMatrix[first][second] != 0 and exMatrix[first][second] == 0:
                strongReactions += 1
                products.append(effects[solMatrix[first][second]-1])
                if effects[solMatrix[first][second]-1] in optionalEffects:
                    exMatrix[first][second] = 1
            elif solMatrix[first][second] != 0 and exMatrix[first][second] == 1:
                exhaustedReactions += 1
                nonProducts.append(effects[solMatrix[first][second]-1])

        wincount = 0
        if weakReactions > 0:
            print(textcolour + "There were: ", weakReactions, " weak reactions.")
        if strongReactions > 0:
            print(textcolour + "There were: ", strongReactions, " strong reactions. Gain the following:")
            random.shuffle(products)

            for p in products:
                if "Essence" in p:
                    wincount+=1
                if "vertical reactions" in p:
                    if "Brimstone Powder" in p:
                        print("\t",p,vValence[0])
                    if "Aqua Forte" in p:
                        print("\t",p,vValence[1])
                    if "Quicksilver" in p:
                        print("\t",p,vValence[2])
                    if "Lead Dust" in p:
                        print("\t",p,vValence[3])
                    if "Phosphoric Salt" in p:
                        print("\t",p,vValence[4])
                    if "Nitre" in p:
                        print("\t",p,vValence[5])
                if "lateral reactions" in p:
                    if "Brimstone Powder" in p:
                        print("\t",p,lValence[0])
                    if "Aqua Forte" in p:
                        print("\t",p,lValence[1])
                    if "Quicksilver" in p:
                        print("\t",p,lValence[2])
                    if "Lead Dust" in p:
                        print("\t",p,lValence[3])
                    if "Phosphoric Salt" in p:
                        print("\t",p,lValence[4])
                    if "Nitre" in p:
                        print("\t",p,lValence[5])
                else:
                    print("\t",p)
        if exhaustedReactions > 0:
            print(textcolour + "There were: ", exhaustedReactions, " Exhausted Reactions.")
            random.shuffle(nonProducts)
            for p in nonProducts:
                if "vertical reactions" in p:
                    if "Brimstone Powder" in p:
                        print("\t",p,vValence[0])
                    if "Aqua Forte" in p:
                        print("\t",p,vValence[1])
                    if "Quicksilver" in p:
                        print("\t",p,vValence[2])
                    if "Lead Dust" in p:
                        print("\t",p,vValence[3])
                    if "Phosphoric Salt" in p:
                        print("\t",p,vValence[4])
                    if "Nitre" in p:
                        print("\t",p,vValence[5])
                if "lateral reactions" in p:
                    if "Brimstone Powder" in p:
                        print("\t",p,lValence[0])
                    if "Aqua Forte" in p:
                        print("\t",p,lValence[1])
                    if "Quicksilver" in p:
                        print("\t",p,lValence[2])
                    if "Lead Dust" in p:
                        print("\t",p,lValence[3])
                    if "Phosphoric Salt" in p:
                        print("\t",p,lValence[4])
                    if "Nitre" in p:
                        print("\t",p,lValence[5])
                else:
                    print("\t",p)
        if weakReactions == 0 and strongReactions == 0 and exhaustedReactions == 0:
            print(textcolour + "There were no reactions.")
        if wincount == 3:
            print(Fore.YELLOW + "You have sythesised the philosopher's stone!")
            print("solution:\n")
            for n in solMatrix:
                print(n)
            i=1
            for n in effects:
                print(i,": ",n)
                i+=1

            sys.exit()
        print("\n")









