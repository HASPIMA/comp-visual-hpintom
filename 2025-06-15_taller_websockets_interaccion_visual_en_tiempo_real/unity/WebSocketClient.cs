using UnityEngine;
using NativeWebSocket;
using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using System;

public class WebSocketClient : MonoBehaviour
{
    WebSocket websocket;
    public GameObject sphere;

    async void Start()
    {
        websocket = new WebSocket("ws://localhost:8765");

        websocket.OnOpen += () =>
        {
            Debug.Log("Conexión WebSocket abierta");
        };

        websocket.OnError += (e) =>
        {
            Debug.Log("Error! " + e);
        };

        websocket.OnClose += (e) =>
        {
            Debug.Log("Conexión cerrada con código: " + e);
        };

        websocket.OnMessage += (bytes) =>
        {
            string message = System.Text.Encoding.UTF8.GetString(bytes);
            Debug.Log("Mensaje recibido: " + message);
            try
            {
                Data data = JsonUtility.FromJson<Data>(message);
                UpdateSphere(data);
            }
            catch (Exception ex)
            {
                Debug.Log("Error al deserializar: " + ex.Message);
            }
        };

        await websocket.Connect();
    }

    void Update()
    {
#if !UNITY_WEBGL || UNITY_EDITOR
        websocket.DispatchMessageQueue();
#endif
    }

    void UpdateSphere(Data data)
    {
        Vector3 newPosition = new Vector3(data.x, data.y, 0);
        sphere.transform.position = newPosition;

        Color newColor;
        if (ColorUtility.TryParseHtmlString(data.color, out newColor))
        {
            sphere.GetComponent<Renderer>().material.color = newColor;
        }
        else
        {
            if (data.color == "red") newColor = Color.red;
            else if (data.color == "green") newColor = Color.green;
            else if (data.color == "blue") newColor = Color.blue;
            else newColor = Color.white;

            sphere.GetComponent<Renderer>().material.color = newColor;
        }
    }

    private async void OnApplicationQuit()
    {
        await websocket.Close();
    }

    [Serializable]
    public class Data
    {
        public float x;
        public float y;
        public string color;
    }
}
