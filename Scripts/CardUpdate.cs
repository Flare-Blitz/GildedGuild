using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Globalization;
public class CardUpdate : MonoBehaviour
{
    [SerializeField] private TMP_Text PriceWhite;
    [SerializeField] private TMP_Text PriceBlack;
    [SerializeField] private TMP_Text PriceRed;
    [SerializeField] private TMP_Text PriceGreen;
    [SerializeField] private TMP_Text PriceBlue;
    [SerializeField] private RawImage CardColor;
    [SerializeField] private int Level = 0;



    // used for determining the color of the card
    byte r = 0;
    byte g = 0;
    byte b = 0;

    int MaxCardPrice = 0; // Determined by level

    int totalPrice = 0;

    int whiteCost = 0;
    int blackCost = 0;
    int redCost = 0;
    int greenCost = 0;
    int blueCost = 0;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        changeCard();
    }

    public void changeCard() {
        // randomly picks a color for the card to be
        int randomNumber = Random.Range(1, 6); // 1 white 2 black 3 red 4 green 5 blue 6 excluded
        if (randomNumber == 1) { r = 255; g = 255; b = 255; }
        else if (randomNumber == 2) { r = 0; g = 0; b = 0; }
        else if (randomNumber == 3) { r = 255; }
        else if (randomNumber == 4) { g = 255; }
        else if (randomNumber == 5) { b = 255; }
        else { /*error*/ }
        CardColor.color = new Color32(r, g, b, 255);
        r = 0;
        g = 0;
        b = 0;
        
        // sets the values for the price
        if (Level == 1) { MaxCardPrice = 4; }
        else if (Level == 2) { MaxCardPrice = 7; }
        else if (Level == 3) { MaxCardPrice = 10; }

        whiteCost = 0;
        blackCost = 0;
        redCost = 0;
        greenCost = 0;
        blueCost = 0;

        while (MaxCardPrice > 0 || totalPrice < 1) { 
            int colorNum = Random.Range(1, 7); // 1 white 2 black 3 red 4 green 5 blue 6 skip 7 excluded
            
            totalPrice = whiteCost + blackCost + redCost + greenCost + blueCost;
            
            // once colorNum is picked add 1 to the associated color
            if (colorNum == 1) { whiteCost++; }
            else if (colorNum == 2) { blackCost++; }
            else if (colorNum == 3) { redCost++; }
            else if (colorNum == 4) { greenCost++; }
            else if (colorNum == 5) { blueCost++; }
            MaxCardPrice--;
        }
        PriceWhite.text = whiteCost.ToString();
        PriceBlack.text = blackCost.ToString();
        PriceRed.text = redCost.ToString();
        PriceGreen.text = greenCost.ToString();
        PriceBlue.text = blueCost.ToString();
    }
}