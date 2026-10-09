using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class GemCounter : MonoBehaviour {
    [SerializeField] private TMP_Text GemCount;
    [SerializeField] private int counter = 0; 

    public void AddOne() {
        counter = int.Parse(GemCount.text);
        counter++;
        GemCount.text = counter.ToString();
    }

}
