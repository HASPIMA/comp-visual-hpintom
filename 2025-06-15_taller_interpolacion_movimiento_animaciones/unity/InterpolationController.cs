using UnityEngine;
using TMPro;


public class InterpolationController : MonoBehaviour
{
    public TextMeshProUGUI timerText;
    public Transform pointA;
    public Transform pointB;
    public Transform pointC;
    public float duration = 3.0f;

    private float t = 0f;
    private bool goingForward = true;

    void Update()
    {
        timerText.text = $"t: {t:F2}";
        Debug.Log("t = " + t.ToString("F2"));

        // Avanza en el tiempo normalizado (0 → 1)
        t += Time.deltaTime / duration;

        // Suavizado tipo ease-in/ease-out
        float smoothT = Mathf.SmoothStep(0f, 1f, t);

        // Posición interpolada entre A y B
        // transform.position = Vector3.Lerp(pointA.position, pointB.position, smoothT);
        transform.position = QuadraticBezier(pointA.position, pointC.position, pointB.position, smoothT);

        // Rotación interpolada entre A y B
        Quaternion startRot = pointA.rotation;
        Quaternion endRot = pointB.rotation;
        transform.rotation = Quaternion.Slerp(startRot, endRot, smoothT);

        // Cuando llega al destino, invertir la dirección
        if (t >= 1f)
        {
            var temp = pointA;
            pointA = pointB;
            pointB = temp;
            t = 0f;
        }
    }

    void OnDrawGizmos()
    {
        if (pointA != null && pointB != null)
        {
            Gizmos.color = Color.yellow;
            Gizmos.DrawLine(pointA.position, pointB.position);
        }

        if (pointA != null && pointB != null && pointC != null)
        {
            Gizmos.color = Color.green;
            Vector3 prev = pointA.position;

            for (float t = 0f; t <= 1f; t += 0.05f)
            {
                Vector3 pos = QuadraticBezier(pointA.position, pointC.position, pointB.position, t);
                Gizmos.DrawLine(prev, pos);
                prev = pos;
            }

            // Opcional: dibuja líneas hacia el punto de control
            Gizmos.color = Color.gray;
            Gizmos.DrawLine(pointA.position, pointC.position);
            Gizmos.DrawLine(pointC.position, pointB.position);
        }
    }

    Vector3 QuadraticBezier(Vector3 a, Vector3 b, Vector3 c, float t)
    {
        Vector3 ab = Vector3.Lerp(a, b, t);
        Vector3 bc = Vector3.Lerp(b, c, t);
        return Vector3.Lerp(ab, bc, t);
    }
}
