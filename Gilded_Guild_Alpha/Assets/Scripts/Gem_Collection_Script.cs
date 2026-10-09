using UnityEngine;

public class Gem_Collection_Script : MonoBehaviour
{
    public GameObject GemSlot1; // maybe raw image
    public GameObject GemSlot2;
    public GameObject GemSlot3;

    public GameObject SameGemSlot1;
    public GameObject SameGemSlot2;

    private string[] colors = new string[3];
    private int itt = 0;

    public void SetGemColor(string color) {
        if (colors != null)
        {
            colors[itt++] = color;
            // first gem slot filled 
            return;
        }
        if (colors[0] == color) //if the same
        {
            // set the mode to 2 of the same color
            return;
        }
        else // else
        {
            // set the second and third to the colors
            colors[itt++] = color;
        }
    }

    // maybe add a function to give the colors

    public void reset() {
        colors = null;
        itt = 0;
    }
}
