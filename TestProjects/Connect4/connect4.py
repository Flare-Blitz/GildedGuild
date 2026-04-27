import random

class Connect4:
    rows = 6
    cols = 7
    scoreLength = 4

    def __init__(self):
        self.matrix = [['0' for i in range(self.cols)] for j in range(self.rows)]

    def printBoard(self):

        for i in range(1, self.cols + 1):
            print(i, " ", end=" ")
        print()

        for i in range(self.cols):
            print("____", end="")
        print()

        for i in range(self.rows):
            for j in range(self.cols):
                print(self.matrix[i][j], " ", end=" ")
            print()

    def resetBoard(self):
        self.matrix = [['0' for i in range(self.cols)] for j in range(self.rows)]
        self.turn = 'R'

    def takeAction(self, column):
        for i in range(self.rows - 1, -1, -1):
            if self.matrix[i][column] == '0':
                self.matrix[i][column] = self.turn
                return True
        return False
    
    def evaluateBoard(self, rowPlaced, colPlaced):
        return 1; #For now, give 1 point for every legal move
    
    def makeRandomMove(self):
        while True:
            if self.takeAction(random.randint(0, 6)):
                return
            
    def takeRandomTurn(self):
        self.makeRandomMove()

        if self.checkVictory():
            return 50, True, 'Victory'
        elif self.checkDraw():
            return -10, True, 'Draw'
        else:
            if self.turn == 'R':
                self.turn = 'Y'
            else: 
                self.turn = 'R'
            return 0, False, 'Continue'
    
    def takeBotTurn(self, action):
        reward = 0
        # print(action)

        for index, value in enumerate(action):
            if value == 1:
                valid = self.takeAction(index)
                if not valid:
                    print(f"{self.turn} attempted an illegal move, getting random move")
                    reward += -50
                    return reward, True, 'Illegal'
                
                if self.checkVictory():
                    reward += 50
                    return reward, True, 'Victory'
                elif self.checkDraw():
                    reward += 10
                    return reward, True, 'Draw'
                else:
                    reward += 1
                    if self.turn == 'R':
                        self.turn = 'Y'
                    else: 
                        self.turn = 'R'
                    return reward, False, 'Continue'
                    
    def takeTurnTrainingBot(self):
        while True:
            self.printBoard()
            print("Player ", self.turn, " , select a column: ", end="")
            column = int(input()) - 1
            if column >= 0 and column < self.cols:
                if self.takeAction(column):
                    return True
                else:
                    print("Column Full")
            else:
                print("Invalid input!")

    def takeTurn(self):
        reward = 0
        while True:
            self.printBoard()
            print("Player ", self.turn, " , select a column: ", end="")
            column = int(input()) - 1
            valid = self.takeAction(column)
            if not valid:
                print(f"{self.turn} attempted an illegal move, getting random move")
                reward += -50
                continue
            
            if self.checkVictory():
                reward += 50
                return reward, True, 'Victory'
            elif self.checkDraw():
                reward += 10
                return reward, True, 'Draw'
            else:
                reward += 1
                if self.turn == 'R':
                    self.turn = 'Y'
                else: 
                    self.turn = 'R'
                return reward, False, 'Continue'

    def checkVictory(self):
        # Check Row Victory
        for i in range(self.rows):
            for j in range(0, self.cols - self.scoreLength + 1):
                line = True
                for k in range(self.scoreLength):
                    if(self.matrix[i][j + k] != self.turn):
                        line = False
                        break
                if line:
                    return True
                
        #Check Column Victory
        for i in range(0, self.rows - self.scoreLength + 1):
            for j in range(self.cols):
                line = True
                for k in range(self.scoreLength):
                    if(self.matrix[i + k][j] != self.turn):
                        line = False
                        break
                if line:
                    return True
                
        #Check Diagonal down-right Victory
        for i in range(0, self.rows - self.scoreLength + 1):
            for j in range(0, self.cols - self.scoreLength + 1):
                line = True
                for k in range(self.scoreLength):
                    if(self.matrix[i + k][j + k] != self.turn):
                        line = False
                        break
                if line:
                    return True
                
        #Check Diagonal up-right Victory
        for i in range(self.scoreLength - 1, self.rows):
            for j in range(0, self.cols - self.scoreLength + 1):
                line = True
                for k in range(self.scoreLength):
                    if(self.matrix[i - k][j + k] != self.turn):
                        line = False
                        break
                if line:
                    return True
                
        return False
                
    def checkDraw(self):
        for i in range(self.cols): #Check the top row of each column
            if self.matrix[0][i] == '0': #There is a column that isn't filled
                return False
            
        #There are no columns that have a spot leftover
        return True
    
    def playRandom(self):
        self.resetBoard()
        self.turn = 'R'
        self.player = 'R'
        while True:
            self.printBoard()
            if self.turn == self.player:
                self.takeTurn()
            else:
                self.makeRandomMove()

            if self.checkVictory():
                self.printBoard()
                print("Player ", self.turn, " Has Won!!!!")
                return
            elif self.checkDraw():
                self.printBoard()
                print("The game is a draw")
                return
            else:
                if self.turn == 'R':
                    self.turn = 'Y'
                else: 
                    self.turn = 'R'
    
    def playGame(self):
        self.resetBoard()

        # while True:
        #     self.printBoard()
        #     self.takeTurn()
        #     if self.checkVictory():
        #         self.printBoard()
        #         print("Player ", self.turn, " Has Won!!!!")
        #         return
        #     elif self.checkDraw():
        #         self.printBoard()
        #         print("The game is a draw")
        #         return
        #     else:
        #         if self.turn == 'R':
        #             self.turn = 'Y'
        #         else: 
        #             self.turn = 'R'

    def play2Player(self):
        self.resetBoard()
        self.turn = 'R'

        while True:
            self.takeTurn()
            if self.checkVictory():
                self.printBoard()
                print("Player ", self.turn, " Has Won!!!!")
                return
            elif self.checkDraw():
                self.printBoard()
                print("The game is a draw")
                return
            else:
                if self.turn == 'R':
                    self.turn = 'Y'
                else: 
                    self.turn = 'R'

                
if __name__ == '__main__':
    game = Connect4()

    # game.playRandom()
    game.play2Player()







        