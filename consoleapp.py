import game

sd=1
pn=1
dif=1

while True:
    sd = input("Input game seed (0-9999999):\n")
    if sd.isnumeric() and int(sd) > 0:
        break
    else:
        print("invalid game seed. Please input a positive integer")

while True:
    pn = input("Input your player number (1-6):\n")
    if pn.isnumeric() and int(pn) > 0 and int(pn) < 6:
        break
    else:
        print("invalid Player Number. Please input a integer between 1 and 6 (inclusive)")

while True:
    dif = input("Input Difficulty (0-5, hardest is 0):\n")
    if dif.isnumeric() and int(dif) >= 0 and int(dif) < 5:
        break
    else:
        print("invalid Difficulty. Please input a integer between 0 and 5 (inclusive)")



newGame = game.game(int(sd),int(pn),int(dif))

print(newGame.getStartingFacts())

quit = False
while not newGame.getGameOver() and not quit :
    mystring = input("Input recipe to mix:\n")

    if mystring == "quit":
        print(newGame.getSolution())
        quit=True
        break
    else:
        newGame.mix(mystring)
        print(newGame.getLastResult())

