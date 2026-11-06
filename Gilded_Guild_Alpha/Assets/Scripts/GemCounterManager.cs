using UnityEngine;

public class GemCounterManager : MonoBehaviour
{
    [SerializeField] private GemCounter WhiteButton;
    [SerializeField] private GemCounter BlackButton;
    [SerializeField] private GemCounter RedButton;
    [SerializeField] private GemCounter GreenButton;
    [SerializeField] private GemCounter BlueButton;

    public void addWhite() 
    {
        WhiteButton.AddOne();
    }
    public void addBlack()
    {
        BlackButton.AddOne();
    }
    public void addRed()
    {
        RedButton.AddOne();
    }
    public void addGreen()
    {
        GreenButton.AddOne();
    }
    public void addBlue()
    {
        BlueButton.AddOne();
    }
}
