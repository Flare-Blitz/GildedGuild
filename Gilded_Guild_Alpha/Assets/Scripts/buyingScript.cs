using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Globalization;
using System;

public class buyingScript : MonoBehaviour {
    // get the color
    [SerializeField] private RawImage CardColor;
    
    // get the price
    [SerializeField] private TMP_Text PriceWhite;
    [SerializeField] private TMP_Text PriceBlack;
    [SerializeField] private TMP_Text PriceRed;
    [SerializeField] private TMP_Text PriceGreen;
    [SerializeField] private TMP_Text PriceBlue;

    // check if you can buy
    [SerializeField] private TMP_Text PurseWhite;
    [SerializeField] private TMP_Text PurseBlack;
    [SerializeField] private TMP_Text PurseRed;
    [SerializeField] private TMP_Text PurseGreen;
    [SerializeField] private TMP_Text PurseBlue;

    [SerializeField] private TMP_Text CardWhite;
    [SerializeField] private TMP_Text CardBlack;
    [SerializeField] private TMP_Text CardRed;
    [SerializeField] private TMP_Text CardGreen;
    [SerializeField] private TMP_Text CardBlue;

    //update
    public CardUpdate CardUpdate;
    public void update() { CardUpdate.changeCard(); }

    public float[] getInfo() {
        float[] info = new float[15];
        // get the color
        float red = CardColor.color.r;
        float green = CardColor.color.g;
        float blue = CardColor.color.b;
        string color = red + green + blue == 3 ? "white"
                    : red + green + blue == 0 ? "black"
                    : red == 1 ? "red"
                    : green == 1 ? "green"
                    : blue == 1 ? "blue"
                    : "null or something I don't plan on using this";
        //get the price
        int whitePrice = int.Parse(PriceWhite.text);
        int blackPrice = int.Parse(PriceBlack.text);
        int redPrice = int.Parse(PriceRed.text);
        int greenPrice = int.Parse(PriceGreen.text);
        int bluePrice = int.Parse(PriceBlue.text);
        if (gameObject.activeSelf) { info[0] = 1f; } // may be auto set to 1 then set to 0 onDisable
        // card level 3 bit
        info[CardUpdate.getLevel()] = 1f;
        // card color W U B R G 5 bit
        if (color == "white") { info[4] = 1f; }
        else if (color == "black") { info[5] = 1f; }
        else if (color == "red") { info[6] = 1f; }
        else if (color == "green") { info[7] = 1f; }
        else if (color == "blue") { info[8] = 1f; }
        // points 1 bit / 5
        info[9] = CardUpdate.getPointValue() / 5f;
        // costs  W B U R G 5 bit
        info[10] = whitePrice / 7f;
        info[11] = bluePrice / 7f;
        info[12] = blackPrice / 7f;
        info[13] = redPrice / 7f;
        info[14] = greenPrice / 7f;
        return info;
    }

    public void buy() { 
        // get the color
        float red = CardColor.color.r;
        float green = CardColor.color.g;
        float blue = CardColor.color.b;

        //get the price
        int whitePrice = int.Parse(PriceWhite.text);
        int blackPrice = int.Parse(PriceBlack.text);
        int redPrice = int.Parse(PriceRed.text);
        int greenPrice = int.Parse(PriceGreen.text);
        int bluePrice = int.Parse(PriceBlue.text);

        //check if you can buy
        int whitePurse = int.Parse(PurseWhite.text);
        int wc = int.Parse(CardWhite.text);

        int blackPurse = int.Parse(PurseBlack.text);
        int bc = int.Parse(CardBlack.text);

        int redPurse = int.Parse(PurseRed.text); 
        int rc = int.Parse(CardRed.text);

        int greenPurse = int.Parse(PurseGreen.text); 
        int gc = int.Parse(CardGreen.text);

        int bluePurse = int.Parse(PurseBlue.text); 
        int uc = int.Parse(CardBlue.text);


        bool w = false;
        bool b = false;
        bool r = false;
        bool g = false;
        bool u = false;
        
        // TODO: add the check for gold
        if (whitePurse + wc >= whitePrice)    { w = true; }
        if (blackPurse +bc >= blackPrice)    { b = true; }
        if (redPurse + rc >= redPrice)        { r = true; } 
        if (greenPurse + gc >= greenPrice)    { g = true; }
        if (bluePurse +uc >= bluePrice)      { u = true; }

        // buy it
        if (w && b && r && g && u) {
            // TODO: add removal of gold bars 
            whitePurse -= Math.Max(0, whitePrice - wc);
            blackPurse -= Math.Max(0, blackPrice - bc);
            redPurse -= Math.Max(0, redPrice - rc);
            greenPurse -= Math.Max(0, greenPrice - gc);
            bluePurse -= Math.Max(0, bluePrice - uc);

            PurseWhite.text = whitePurse.ToString();
            PurseBlack.text = blackPurse.ToString();
            PurseRed.text = redPurse.ToString();
            PurseGreen.text = greenPurse.ToString();
            PurseBlue.text = bluePurse.ToString();

            //give the product
            string color = red + green + blue == 3 ? "white"
                        : red + green + blue == 0 ? "black"
                        : red == 1 ? "red"
                        : green == 1 ? "green"
                        : blue == 1 ? "blue"
                        : "null or something I don't plan on using this";
         
            int counter = 0;
            if (color == "white") {
                counter = int.Parse(CardWhite.text);
                counter++;
                CardWhite.text = counter.ToString();
            }
            else if (color == "black") {
                counter = int.Parse(CardBlack.text);
                counter++;
                CardBlack.text = counter.ToString();
            }
            else if (color == "red") {
                counter = int.Parse(CardRed.text);
                counter++;
                CardRed.text = counter.ToString();
            }
            else if (color == "green") {
                counter = int.Parse(CardGreen.text);
                counter++;
                CardGreen.text = counter.ToString();
            }
            else if (color == "blue") {
                counter = int.Parse(CardBlue.text);
                counter++;
                CardBlue.text = counter.ToString();
            }

            // reset
            CardUpdate.changeCard();
        }
       

    }

    

}
    

