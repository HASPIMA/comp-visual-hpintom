using UnityEngine;

public class CubeScript : MonoBehaviour
{
    Vector3 initialPosition;
    void Start()
    {
        Debug.Log("Initial position: " + transform.position);
        initialPosition = transform.position;
    }

    void Update()
    {
        // Random translation along the X or Y axis every few seconds
        if (Time.frameCount % 60 == 0)
        {
            float randomX = Random.Range(-1f, 1f);
            float randomY = Random.Range(-1f, 1f);
            transform.Translate(new Vector3(randomX, randomY, 0));
            Debug.Log("New position: " + transform.position);

            // Reset position after 5 seconds
            if (Time.frameCount % 300 == 0)
            {
                transform.position = initialPosition;
                Debug.Log("Position reset to: " + transform.position);
            }
        }

    }
}
