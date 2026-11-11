using UnityEngine;

public class NobleManagerScript : MonoBehaviour
{
    [SerializeField] private NobleScript[] nobleScriptList;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    public float[] GetInfo() {
        float[] nobles = new float[35];
        int noblenumber = 0;
        foreach (var noble in nobleScriptList)
        {
            for (int i = 0; i < 7; i++)
            {
                nobles[noblenumber * 7 + i] = noble.GetInfo()[i];
            }
        }
        return nobles;
    }
}
