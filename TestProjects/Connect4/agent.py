from connect4 import Connect4
from model import Linear_QNet, QTrainer
from collections import deque
import torch
import numpy as np
import random
from pathlib import Path
import os

MAX_MEMORY = 100_000
BATCH_SIZE = 128
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 1.0  # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(126, 64, 64, 7) # declares a ( (3*6*7), 16, 16, 7 ) NN
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.random = False

    # def get_state(self, game):
    #     board = np.zeros((3, 6, 7), dtype=int)
    #     if game.turn == 'R':
    #         opponent = 'Y'
    #     else:
    #         opponent = 'R'
        
    #     board[0] = int(game.matrix == '0')
    #     board[1] = int(game.matrix == game.turn)
    #     board[2] = int(game.matrix == opponent)

    #     print(np.array(board.flatten()))
    #     input()

    #     return np.array(board.flatten())

    def get_state(self, game):
        # Convert list of lists to a numpy array first
        matrix_as_array = np.array(game.matrix)
        
        board = np.zeros((3, 6, 7), dtype=float)
        if game.turn == 'R':
            opponent = 'Y'
        else:
            opponent = 'R'
        
        # Correct boolean indexing
        board[0] = (matrix_as_array == '0').astype(float)
        board[1] = (matrix_as_array == game.turn).astype(float)
        board[2] = (matrix_as_array == opponent).astype(float)

        return board.flatten()
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, game):
        # random moves: tradeoff exploration / exploitation
        final_move = [0,0,0,0,0,0,0]

        self.epsilon = max(0.05, 1.0 - (self.n_games / 10000))
        # self.epsilon = 0.0
        if random.random() < self.epsilon:
            move = random.randint(0, 6)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            #Make illegal moves impossible
            for idx, val in enumerate(prediction):
                if game.matrix[0][idx] != '0':
                    prediction[idx] -= 100
            move = torch.argmax(prediction).item()

        final_move[move] = 1

        return final_move
    
    def loadOldModel(self, file_name='model.pth'):
        model_folder_path = './model'
        file_name = os.path.join(model_folder_path, file_name)
        if Path(file_name).is_file():
            state_dict = torch.load(file_name, weights_only=True)
            self.model.load_state_dict(state_dict)
            self.random = False
        else:
            self.random = True
    
def train():

    newAgent = Agent()
    oldAgent = Agent()

    #Temp code to further test against random bot
    # newAgent.model.load()
    # oldAgent = None

    winrate = 0

    game = Connect4()

    game.playGame()

    newAgent.loadOldModel()
    oldAgent.n_games = 10000
    
    for y in range(50):
        newAgentTurn = 'First'
        oldAgent.loadOldModel()

        wins = 0.0
        losses = 0.0
        draws = 0.0
        dqs = 0.0

        #Simulate 500 games
        for x in range(5000):
            newAgent.n_games += 1
            oldAgent.n_games += 1
            print(f"Session #: {y}, Game #: {x}; AVG = {wins} : {losses}")

            while True:

                state_old = newAgent.get_state(game)

                final_move = newAgent.get_action(state_old, game)

                reward, done, result = game.takeBotTurn(final_move)

                if(done):
                    state_new = newAgent.get_state(game)

                    if result == 'Victory':
                        wins += 1
                    elif result == 'Draw':
                        draws += 1
                    elif result == 'Illegal':
                        dqs += 1
                else:
                    if oldAgent.random == False:
                        enemy_state = oldAgent.get_state(game)
                        enemy_action = oldAgent.get_action(enemy_state, game)
                        enemy_reward, enemy_done, result = game.takeBotTurn(enemy_action)
                    else:
                        enemy_reward, enemy_done, result = game.takeRandomTurn()

                    done = enemy_done
                    if enemy_done:
                        if result == 'Victory':
                            reward -= enemy_reward
                            losses += 1
                        elif result == 'Draw':
                            reward += enemy_reward
                            draws += 1

                    # reward -= enemy_reward
                    state_new = newAgent.get_state(game)

                # train short memory
                newAgent.train_short_memory(state_old, final_move, reward, state_new, done)

                # remember
                newAgent.remember(state_old, final_move, reward, state_new, done)

                if done:

                    game.resetBoard()

                    # train long memory, plot result
                    newAgent.train_long_memory()

                    if newAgentTurn == 'First':
                        newAgentTurn = 'Second'
                        enemy_state = oldAgent.get_state(game)
                        enemy_action = oldAgent.get_action(enemy_state, game)
                        game.takeBotTurn(enemy_action)
                    else:
                        newAgentTurn = 'First'

                    break

        print(f"Wins: {wins}")
        print(f"Losses: {losses}")
        print(f"Draws: {draws}")
        print(f"DQs: {dqs}")
        if wins > losses:
            winrate = wins/(wins + losses)
            newAgent.model.save()

if __name__ == '__main__':
    train()