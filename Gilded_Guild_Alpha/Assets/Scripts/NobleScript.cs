using UnityEngine;
using TMPro;

public class NobleScript : MonoBehaviour
{
    [SerializeField] private TMP_Text Requirement1;
    public Color RequirementColor1 = Color.gray;
    [SerializeField] private TMP_Text Requirement2;
    public Color RequirementColor2 = Color.gray;
    [SerializeField] private TMP_Text Requirement3;
    public Color RequirementColor3 = Color.gray;



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

    public float[] GetInfo() {
        float[] nobles = new float[7];
        // presence flag
        if (gameObject.activeSelf) { nobles[0] = 1f; }
        // points given (always 3) / 5
        nobles[1] = 0.6f;
        // requirements / 7 W U B R G 
        if (RequirementColor1 == Color.white || RequirementColor2 == Color.white || RequirementColor3 == Color.white)
        {
            nobles[2] = 1f;
        }

        if (RequirementColor1 == Color.black || RequirementColor2 == Color.black || RequirementColor3 == Color.black)
        {
            nobles[3] = 1f;
        }

        if (RequirementColor1 == Color.blue || RequirementColor2 == Color.blue || RequirementColor3 == Color.blue)
        {
            nobles[4] = 1f;
        }

        if (RequirementColor1 == Color.red || RequirementColor2 == Color.red || RequirementColor3 == Color.red)
        {
            nobles[5] = 1f;
        }

        if (RequirementColor1 == Color.green || RequirementColor2 == Color.green || RequirementColor3 == Color.green)
        {
            nobles[6] = 1f;
        }
        return nobles;
    }

    public void Start()
    {
        int RequirementsNumber = Random.Range(2, 4); // 2 or 3 requirements
         // sets the first color to a random color
        RequirementColor1 = ColorPicker();
        // ensures the first color and second color dont match
        Color temp = ColorPicker();
       
        while (temp == RequirementColor1) { 
            temp = ColorPicker();
        }
        RequirementColor2 = temp;
        Requirement1.text = "4";
        Requirement2.text = "4";
        Requirement3.enabled = false;
        // since the 3 requirement still needs the first 2 this just runs for the 3rd
        if (RequirementsNumber == 3) {
            while (temp == RequirementColor1 || temp == RequirementColor2)
            {
                temp = ColorPicker();
            }
            RequirementColor3 = temp;
            Requirement1.text = "3";
            Requirement2.text = "3";
            Requirement3.enabled = true;
            Requirement3.text = "3";
        }
        Requirement1.color = RequirementColor1;
        Requirement2.color = RequirementColor2;
        Requirement3.color = RequirementColor3;
    }
}
