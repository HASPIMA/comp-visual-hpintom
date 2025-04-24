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
        // Reset position after 5 seconds
        bool shouldReset = Time.frameCount % 300 == 0;

        // Random translation along the X or Y axis every few seconds
        bool isNewFrameEvent = Time.frameCount % 80 == 0;
        if (!shouldReset && isNewFrameEvent)
        {
            float randomX = Random.Range(-1f, 1f);
            float randomY = Random.Range(-1f, 1f);
            transform.Translate(new Vector3(randomX, randomY, 0));
            Debug.Log("New position: " + transform.position);
        }

        if (shouldReset)
        {
            transform.position = initialPosition;
            Debug.Log("Position reset to the original one");
        }

        // Constant rotation dependent on Time.deltaTime
        float rotationSpeedY = 50f; // degrees per second
        float rotationAmount = rotationSpeedY * Time.deltaTime;
        transform.Rotate(new Vector3(0, rotationAmount, 0));

    }
}
