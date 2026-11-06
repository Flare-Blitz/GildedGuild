using UnityEngine;
using TMPro;

public class DeckSelectionManager : MonoBehaviour
{
    [SerializeField] private CardSelectionManager[] DeckLevel;
    [SerializeField] private TMP_Text ActionSetup;
    [SerializeField] private GameObject ReserveScreen;


    public void CardSelect(int deckNumber, int rowNumber) // make tuple?
    {
        char actionChar = 'H'; // double check that H is the buy letter
        if (ReserveScreen.activeSelf) { actionChar = 'E'; } // double check E is the reserve letter

        ActionSetup.text = actionChar + deckNumber.ToString() + rowNumber.ToString();
    }

    public void CardBuy(int deckNumber, int rowNumber) { 
        DeckLevel[deckNumber].SelectCardBuy(rowNumber);
    }
    public void CardReserve(int deckNumber, int rowNumber)
    {
        DeckLevel[deckNumber].SelectCardReserve(rowNumber);
    }
}
