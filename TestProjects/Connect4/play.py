import torch
import numpy as np
from connect4 import Connect4
from agent import Agent

def play_against_bot():
    # 1. Setup the game and agent
    game = Connect4()
    agent = Agent()
    
    # 2. Load the trained model
    # Ensure the file path matches where you saved it (e.g., 'model/model.pth')
    model_path = './model/model.pth'
    try:
        # weights_only=True is safer for loading
        agent.model.load_state_dict(torch.load(model_path, weights_only=True))
        agent.model.eval() # Set to evaluation mode (turns off dropout/learning)
        print("Model loaded successfully!")
    except FileNotFoundError:
        print(f"Could not find model at {model_path}. Make sure you've trained it first!")
        return

    # 3. Choose sides
    print("Connect 4: Human vs. AI")
    human_turn = input("Do you want to go first? (y/n): ").lower() == 'y'
    
    game.resetBoard()
    # If human is 'R', bot is 'Y'. If human is 'Y', bot is 'R'.
    # In your connect4.py, the game always starts with 'R'
    
    while True:
        game.printBoard()
        
        if (game.turn == 'R' and human_turn) or (game.turn == 'Y' and not human_turn):
            # --- HUMAN TURN ---
            print(f"\nYour turn ({game.turn})")
            while True:
                try:
                    move = int(input("Select a column (1-7): ")) - 1
                    if 0 <= move <= 6 and game.matrix[0][move] == '0':
                        game.takeAction(move)
                        break
                    else:
                        print("Invalid move! Column is full or out of range.")
                except ValueError:
                    print("Please enter a number between 1 and 7.")
        else:
            # --- AI TURN ---
            print(f"\nAI is thinking ({game.turn})...")
            state = agent.get_state(game)
            state_tensor = torch.tensor(state, dtype=torch.float).unsqueeze(0)
            
            with torch.no_grad():
                prediction = agent.model(state_tensor).squeeze(0)
                
                # Apply Action Masking (Crucial!)
                # We set the score of illegal moves to a very low number
                for i in range(7):
                    if game.matrix[0][i] != '0':
                        prediction[i] = -1e9
                
                move = torch.argmax(prediction).item()
            
            print(f"AI chose column: {move + 1}")
            game.takeAction(move)

        # 4. Check for Game Over
        if game.checkVictory():
            game.printBoard()
            print(f"\nGAME OVER! Player {game.turn} wins!")
            break
        elif game.checkDraw():
            game.printBoard()
            print("\nGAME OVER! It's a draw!")
            break

        # Switch turns manually if your takeAction doesn't do it automatically
        game.turn = 'Y' if game.turn == 'R' else 'R'

if __name__ == '__main__':
    play_against_bot()