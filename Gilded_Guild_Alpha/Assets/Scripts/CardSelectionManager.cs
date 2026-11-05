using UnityEngine;

public class CardSelectionManager : MonoBehaviour
{
    [SerializeField] private buyingScript[] CardRow; // card Column starting at 0

    public float[] SelectCard(int choice)
    {
        return CardRow[choice].getInfo();
    }
    public void SelectCardBuy(int choice) {
        CardRow[choice].buy();
    }
    public void SelectCardReserve(int choice) { 
        CardRow[choice].update(); 
    }

}
