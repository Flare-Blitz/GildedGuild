using UnityEngine;
using System.Runtime.InteropServices;

public class GameCommunicator : MonoBehaviour
{
    [DllImport("__Internal")]
    private static extern void GameOver(string userName, int score);

    public void SomeMethod()
    {
#if UNITY_WEBGL == true && UNITY_EDITOR == false
    GameOver ("Player1", 100);
    Debug.Log("Information Sent");
#endif
    }
}