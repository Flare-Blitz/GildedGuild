using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class GemCounter : MonoBehaviour {
    [SerializeField] private TMP_Text GemCount;
    [SerializeField] private int counter = 0;
    [SerializeField] private char ColorLetter = 'N';

    [SerializeField] private ActionSetup actionSetup;

    public void AddOne() {
        counter = int.Parse(GemCount.text);
        counter++;
        GemCount.text = counter.ToString();
    }
    public void ChooseGemColor() {
        actionSetup.ActionInput(ColorLetter);
    }
}
