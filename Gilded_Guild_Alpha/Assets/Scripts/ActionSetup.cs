using UnityEngine;
using TMPro;

public class ActionSetup : MonoBehaviour
{
    
    [SerializeField] private TMP_Text ActionTextBox;
    void Start() { ActionTextBox.text = ""; }
    public void ActionInput(char input) {
        // if input is a color gem
        if (input == 'W' || input == 'U' || input == 'R' || input == 'G' || input == 'B')
        {
            collectGem(input);
        }
        //if input is for buying card
        else if (input == 'C') { }
        // covers all else
        else { Debug.Log("The Input is not Valid: " + input); }

        //update the textBox
    }
    private void reserveCard( char input) { }
    private void cardBuy( char input) { 
        // MAY BE STRING BASED?
    }
    private void collectGem( char inputChar ) {
        string input = inputChar.ToString();
        // input = W U R G B 
        // These Conditionals are written with what I don't want

        // if empty
        if (ActionTextBox.text == "") { ActionTextBox.text += input; }

        // if the textbox doesn't contain the instructions for the action
        else if (ActionTextBox.text[0] != 'W' && ActionTextBox.text[0] != 'U' && ActionTextBox.text[0] != 'R' && ActionTextBox.text[0] != 'G' && ActionTextBox.text[0] != 'B') { ActionTextBox.text = ""; ActionTextBox.text += input; }

        // if the instructions can be valid
        else if (ActionTextBox.text.Length >= 3) { return; }
        else if (ActionTextBox.text.Length == 1 && input == ActionTextBox.text) { ActionTextBox.text += input + " "; }


        // add the selected gems
        else { ActionTextBox.text += input; } 
    }
}
