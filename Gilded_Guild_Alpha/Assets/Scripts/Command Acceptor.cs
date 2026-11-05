using UnityEngine;

public class CommandAcceptor : MonoBehaviour
{
    [SerializeField] private GemCounterManager gemCounterManger;
    // [SerializeField] private buyingScriptManager BuyingManager;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void CommandAccept(string choice) {
        if (choice.StartsWith('W') ||
            choice.StartsWith('U') ||
            choice.StartsWith('R') ||
            choice.StartsWith('G') ||
            choice.StartsWith('B'))
        {
            if (choice[0] == choice[1]) {
                if (choice[0] == 'W') { gemCounterManger.addWhite(); }
                if (choice[0] == 'U') { gemCounterManger.addBlack(); }
                if (choice[0] == 'R') { gemCounterManger.addRed();   }
                if (choice[0] == 'G') { gemCounterManger.addBlue();  }
                if (choice[0] == 'B') { gemCounterManger.addGreen(); }
            }
            else
            {
                foreach (char gem in choice) {
                    if (gem == 'W') { gemCounterManger.addWhite(); }
                    if (gem == 'U') { gemCounterManger.addBlack(); }
                    if (gem == 'R') { gemCounterManger.addRed();   }
                    if (gem == 'G') { gemCounterManger.addBlue();  }
                    if (gem == 'B') { gemCounterManger.addGreen(); }
                }
            }
        }
        if (choice.StartsWith('P')) { 
            //
        }
        if (choice.StartsWith('E')) { 
            //
        }
    }
}
