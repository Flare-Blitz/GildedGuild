using UnityEngine;

public class BoardStateEncoding : MonoBehaviour
{
    [SerializeField] private ConfirmButton confirmButton;
    [SerializeField] private CreateRuntimeModel CreateRuntimeModel;
    [SerializeField] private CardCount[] CardCountList;
    [SerializeField] private CardSelectionManager[] cardSelectionRow;

    /*
    Order of Encoding:
        0-2 Player count
        3-6 Player Position
        7-12 Gems in bank
            [white, blue, black, red, green, gold]
        13-15 Remaining cards
        16-165 Market Cards
        196-230 Noble
        231-288 Current player
        289-346 Next Player
        347-404 Next Player
        405-462 Next Player
    Notes:
        None of the values exceed 1
        Color order for ML is W B U R G A
        Color order on scripts in unity are W U R G B A
    */

    public float[] BoardEncoding()
    {
        float[] state = new float[462];
        for (int i = 0; i < 6; i++)
        {
            float[] temp = GetBankGems();
            state[7 + i] = temp[i];
        }
        for (int i = 0; i < 3; i++)
        {
            float[] temp = GetRemainingCards();
            state[13 + i] = temp[i];
        }
        for (int i = 0; i < 180; i++)
        {
            float[] temp =  GetMarketCards();
            state[16 + i] = temp[i];
        }
        for (int i = 0; i < 0; i++)
        {
            float[] temp =  GetNobles();
            state[13 + i] = temp[i];
        }
        for (int i = 0; i < 0; i++)
        {
            float[] temp = GetPlayer(0);
            state[13 + i] = temp[i];
        }
        for (int i = 0; i < 0; i++)
        {
            float[] temp = GetPlayer(1);
            state[13 + i] = temp[i];
        }
        for (int i = 0; i < 0; i++)
        {
            float[] temp = GetPlayer(2);
            state[13 + i] = temp[i];
        }
        for (int i = 0; i < 0; i++)
        {
            float[] temp = GetPlayer(3);
            state[13 + i] = temp[i];
        }
        
        return state;
    }

    public void Start() { 
        updateUserInput();
    }

    public void updateUserInput()
    {
        CreateRuntimeModel.AcceptUserInput(BoardEncoding());
    }
    public float[] GetBankGems() {
        float[] bank = new float[6];
        //retrieve the amount of gems you can grab
        bank = confirmButton.GetBankCounts();
        // divide by 7 or for gold 5
        for (int i = 0; i < 5; i++) { bank[i] = bank[i] / 7f; }
        bank[5] = 1f;
        return bank;
    }
    public float[] GetRemainingCards() {
        float[] decks = new float[3];
        // retrieve the amount of gems you can grab
        for (int i = 0; i < 3; i++) {
            // divide by 40
            
            decks[i] = CardCountList[i].getCardCount() / 40f;
        }
        
        return decks;
    }
    public float[] GetCardAt(int x, int y) {
        float[] card = new float[15];
        card = cardSelectionRow[x].SelectCard(y);
        return card;
    }
    public float[] GetMarketCards()
    {
        float[] market = new float[180];
        for (int i = 0; i < 2; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                float[] temp = GetCardAt(i, j);
                for (int k = 0; k < 15; k++)
                {
                    market[(i * 15 * 4) + (j * 15) + k] = temp[k];
                }
            }
        }
        return market;
    }
    public float[] GetNobles()
    {
        float[] nobles = new float[35];
        // presence flag
        // points given / 5
        // requirements / 7 W U B R G 
        //do that ^ 3 times
        return nobles;
    }
    public float[] GetPlayer(int x) {
        float[] player = new float[58];
        // total points / max number of points
        // cheap gems player has / 10 WUBRG
        // gold gems player has / 5
        // expensive gems player has / 7 WUBRG
        // Number of Nobles / IDK 
        // Reserved cards in player hand * 3
        return player;
    }
}
