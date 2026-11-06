using UnityEngine;

public class PsudeoTurns : MonoBehaviour
{
    [SerializeField] private int numberOfPlayers;
    [SerializeField] private GameObject PlayerHand;
    [SerializeField] private GameObject Canvas;

    private GameObject[] turnOrder;

    void Start()
    {
        turnOrder = new GameObject[numberOfPlayers];
        for (int i = 0; i < numberOfPlayers; i++) {
            turnOrder[i] = Instantiate(PlayerHand, PlayerHand.transform.position, PlayerHand.transform.rotation, Canvas.transform);
        }
        turnOrder[0].SetActive(true);
    }


}
