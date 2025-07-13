using UnityEngine;
using UnityEngine.AI;

public class IA_PatrullajeConDeteccion : MonoBehaviour
{
    public Transform[] puntos;
    private int index = 0;
    private NavMeshAgent agente;
    private Animator animator;

    private Transform jugador;
    private bool persiguiendo = false;
    public float distanciaDeAlcance = 1.5f;

    void Start()
    {
        agente = GetComponent<NavMeshAgent>();
        animator = GetComponent<Animator>();
        jugador = GameObject.FindGameObjectWithTag("Player").transform;

        if (puntos.Length > 0)
            agente.SetDestination(puntos[index].position);
    }

    void Update()
    {
        float velocidad = agente.velocity.magnitude;
        

        if (persiguiendo)
        {
            animator.SetFloat("velocidad", 2.1f);
            agente.SetDestination(jugador.position);

            // Si está cerca del jugador, detenerse (idle)
            if (Vector3.Distance(transform.position, jugador.position) < distanciaDeAlcance)
            {
                agente.ResetPath();  // se detiene
                animator.SetFloat("velocidad", 0.01f);
            }
        }
        else
        {
            animator.SetFloat("velocidad", velocidad);
            if (!agente.pathPending && agente.remainingDistance < 0.5f)
            {
                index = (index + 1) % puntos.Length;
                agente.SetDestination(puntos[index].position);
            }
        }
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            persiguiendo = true;
        }
    }
}
