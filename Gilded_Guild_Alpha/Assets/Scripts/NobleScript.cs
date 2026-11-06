using UnityEngine;
using TMPro;

public class NobleScript : MonoBehaviour
{
    [SerializeField] private TMP_Text Requirement1;
    [SerializeField] private TMP_Text Requirement2;
    [SerializeField] private TMP_Text Requirement3;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    private Color ColorPicker()
    {
        int r = 0, g = 0, b = 0;
        int randomNumber = Random.Range(1, 6); // 1 white 2 black 3 red 4 green 5 blue 6 excluded
        if (randomNumber == 1) { r = 255; g = 255; b = 255; }
        else if (randomNumber == 2) { r = 0; g = 0; b = 0; }
        else if (randomNumber == 3) { r = 255; }
        else if (randomNumber == 4) { g = 255; }
        else if (randomNumber == 5) { b = 255; }
        Color temp = new Color(r, g, b);
        return temp;
    }

    public void Start()
    {
        int RequirementsNumber = Random.Range(2, 4); // 2 or 3 requirements
        if (RequirementsNumber == 2) { }
    }
}
