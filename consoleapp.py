import game

sd = input("Input game seed:\n")
pn = input("Player Number:\n")
dif = input("Input Difficulty:\n")

newGame = game.game(sd,pn,dif)

print(newGame.getStartingFacts())

quit = False
while not newGame.getGameOver() or not quit:
    mystring = input("Input recipy to mix:\n")

    if mystring == "quit":
        print(newGame.getSolution())
        quit=True
        break
    else:
        newGame.mix(mystring)
        print(newGame.getLastResult())

