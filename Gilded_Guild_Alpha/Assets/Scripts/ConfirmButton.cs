using UnityEngine;
using TMPro;

public class ConfirmButton : MonoBehaviour
{
    [SerializeField] private TMP_Text ActionTextBox;
    [SerializeField] private GemCounterManager gemCounterManager;
    private string Action;
    private int WhiteBankCount = 7, BlackBankCount = 7, RedBankCount = 7, GreenBankCount = 7, BlueBankCount = 7;

    public float[] GetBankCounts() {
        // W B U R G
        float[] bankCounts = new float[6];
        bankCounts[0] = WhiteBankCount;
        bankCounts[1] = BlueBankCount;
        bankCounts[2] = BlackBankCount;  
        bankCounts[3] = RedBankCount;
        bankCounts[4] = GreenBankCount;
        return bankCounts;
    }

    public void confirmClick()
    {
        Action = ActionTextBox.text; // get the action 
        ActionTextBox.text = ""; // reset the ActionTextBox
        
        // Gem Collection
        if (Action[0] == 'W' || Action[0] == 'U' || Action[0] == 'R' || Action[0] == 'G' || Action[0] == 'B')
        {
            foreach (var item in Action) { 
                if      (item == 'W' && WhiteBankCount > 0) { gemCounterManager.addWhite(); WhiteBankCount--; }
                else if (item == 'U' && BlackBankCount > 0) { gemCounterManager.addBlack(); BlackBankCount--; }
                else if (item == 'R' && RedBankCount   > 0) { gemCounterManager.addRed();   RedBankCount--;   }
                else if (item == 'G' && GreenBankCount > 0) { gemCounterManager.addGreen(); GreenBankCount--; }
                else if (item == 'B' && BlueBankCount  > 0) { gemCounterManager.addBlue();  BlueBankCount--;  }
                else return;
            }
        }


        // Submits your turn
        //gameObject.SetActive(false);
        //turns on the next player's confirm button
    }
};
