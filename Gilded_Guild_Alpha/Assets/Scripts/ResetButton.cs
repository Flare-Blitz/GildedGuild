using UnityEngine;
using TMPro;

public class ResetButton : MonoBehaviour
{
    [SerializeField] private TMP_Text ActionTextBox;
    public void Reset() { 
        ActionTextBox.text = "";
    }
}
