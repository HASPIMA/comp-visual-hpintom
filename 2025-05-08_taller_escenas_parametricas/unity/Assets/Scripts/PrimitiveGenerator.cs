using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;
using System.IO;

// Clase principal que controla la generación de objetos
public class SimplePrimitiveGenerator : MonoBehaviour
{
    // ----------------------------------------------------------------
    // Valores por defecto:
    // ----------------------------------------------------------------
    [Header("Parámetros Manuales (con valores por defecto)")]
    public Vector3[] posiciones = new Vector3[]
    {
        new Vector3(-2, 0, 0),
        new Vector3( 0, 0, 0),
        new Vector3( 2, 0, 0),
        new Vector3( 0, 2, 0)
    };

    public PrimitiveType[] tipos = new PrimitiveType[]
    {
        PrimitiveType.Sphere,
        PrimitiveType.Cube,
        PrimitiveType.Cylinder,
        PrimitiveType.Sphere
    };

    public Color[] colores = new Color[]
    {
        Color.red,
        Color.green,
        Color.blue,
        new Color(1f, 0.5f, 0f)  // naranja
    };

    public Vector3[] escalas = new Vector3[]
    {
        Vector3.one * 0.8f,
        new Vector3(1f, 2f, 1f),
        Vector3.one,
        new Vector3(1.5f, 1f, 0.5f)
    };

    [Header("UI Elements (Opcional)")]
    public Button regenerateButton;
    public Button exportJsonButton;

    // Internamente guardaremos instancias para destruirlas al regenerar
    private List<GameObject> instancias = new List<GameObject>();

    void Start()
    {
        // Conectar botones si existen
        if (regenerateButton != null)
            regenerateButton.onClick.AddListener(RegenerarEscena);
        if (exportJsonButton != null)
            exportJsonButton.onClick.AddListener(ExportarParametrosAJson);

        // Carga opcional desde JSON
        string ruta = Path.Combine(Application.streamingAssetsPath, "params.json");
        if (File.Exists(ruta))
            CargarDesdeJson(ruta);

        // Generar la primera vez con los valores por defecto (o los del JSON)
        GenerarObjetos();
    }

    /// <summary>
    /// Itera sobre los arrays y crea primitivas
    /// </summary>
    void GenerarObjetos()
    {
        // Asegurarnos de tener el mismo tamaño en todos
        int count = Mathf.Min(
            Mathf.Min(posiciones.Length, tipos.Length),
            Mathf.Min(colores.Length, escalas.Length)
        );

        for (int i = 0; i < count; i++)
        {
            // Ejemplo lógico: no crear cilindros si x < 0
            if (tipos[i] == PrimitiveType.Cylinder && posiciones[i].x < 0)
                continue;

            GameObject go = GameObject.CreatePrimitive(tipos[i]);
            go.transform.position = posiciones[i];
            go.transform.localScale = escalas[i];

            // Aplicar color
            Renderer rend = go.GetComponent<Renderer>();
            rend.material = new Material(Shader.Find("Standard"));
            rend.material.color = colores[i];

            instancias.Add(go);
        }
    }

    /// <summary>
    /// Destruye todas las instancias y vuelve a generar
    /// </summary>
    void RegenerarEscena()
    {
        foreach (var go in instancias)
            Destroy(go);
        instancias.Clear();
        GenerarObjetos();
    }

    /// <summary>
    /// Serializa los parámetros actuales a JSON y lo guarda
    /// </summary>
    void ExportarParametrosAJson()
    {
        List<PrimitiveData> lista = new List<PrimitiveData>();
        for (int i = 0; i < posiciones.Length; i++)
        {
            lista.Add(new PrimitiveData
            {
                posicion = posiciones[i],
                tipo = tipos[i].ToString(),
                color = new float[] { colores[i].r, colores[i].g, colores[i].b, colores[i].a },
                escala = escalas[i]
            });
        }
        string json = JsonUtility.ToJson(new PrimitiveDataList { items = lista }, true);
        string ruta = Path.Combine(Application.streamingAssetsPath, "exported_params.json");
        File.WriteAllText(ruta, json);
        Debug.Log("Parámetros exportados a: " + ruta);
    }

    /// <summary>
    /// Lee un archivo JSON y llena los arrays
    /// </summary>
    void CargarDesdeJson(string path)
    {
        string txt = File.ReadAllText(path);
        PrimitiveDataList lista = JsonUtility.FromJson<PrimitiveDataList>(txt);

        int n = lista.items.Count;
        posiciones = new Vector3[n];
        tipos = new PrimitiveType[n];
        colores = new Color[n];
        escalas = new Vector3[n];

        for (int i = 0; i < n; i++)
        {
            var d = lista.items[i];
            posiciones[i] = d.posicion;
            tipos[i] = (PrimitiveType)System.Enum.Parse(typeof(PrimitiveType), d.tipo);
            colores[i] = new Color(d.color[0], d.color[1], d.color[2], d.color[3]);
            escalas[i] = d.escala;
        }
    }

    // Clases auxiliares para JSON
    [System.Serializable]
    public class PrimitiveData
    {
        public Vector3 posicion;
        public string tipo;
        public float[] color;
        public Vector3 escala;
    }

    [System.Serializable]
    public class PrimitiveDataList
    {
        public List<PrimitiveData> items;
    }
}
