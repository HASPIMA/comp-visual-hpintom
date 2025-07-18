

# Taller - Animación con AI en Unity para personajes autónomos

##  Fecha
2025-07-12



##  Objetivo del Taller

Implementar comportamientos autónomos en un personaje 3D dentro de Unity, combinando navegación con NavMesh, animaciones con `Animator`, y lógica de detección de jugador. Se busca que el personaje patrulle una zona, detecte a un objetivo y modifique su comportamiento de forma reactiva.

---

##  Comportamientos Implementados

1. **Patrullaje entre puntos** usando `NavMeshAgent` y un arreglo de `Transform[]`.
2. **Animación en tiempo real** con un `Animator Controller` que contiene los estados:
   - Idle
   - Walk
   - Run
   Las transiciones entre estos estados se activan con una variable `velocidad` actualizada por el script según la magnitud del `NavMeshAgent.velocity`.
3. **Detección de jugador** mediante `OnTriggerEnter()` con un `Collider` configurado como `Trigger`.
4. **Cambio de comportamiento**: al detectar al jugador, el personaje deja de patrullar y corre hacia él hasta alcanzarlo; una vez cerca, se detiene (Idle).

---

##  Herramientas y configuración en Unity

- Unity 2023+ con sistema moderno de navegación (`NavMeshSurface`)
- Modelo riggeado desde [Mixamo](https://mixamo.com)
- Animaciones individuales (`Idle.fbx`, `Walk.fbx`, `Run.fbx`)
- Configuración de `Animator Controller` con condiciones:
  - `velocidad > 2` → Run
  - `velocidad > 0.1` → Walk
  - `velocidad < 0.1` → Idle
- Terreno con obstáculos y puntos de patrullaje (`Empty GameObjects`)
- `Capsule` como jugador estático con `Tag: Player`



## 📄 Estructura del Proyecto

```
2025-07-12_taller_animacion_ai_unity/
├── escenas/
│   └── escena_final.unity
├── scripts/
│   ├── IA_PatrullajeConDeteccion.cs
├── capturas/
│   ├── patrullaje.gif
│   ├── deteccion.gif
├── README.md
```

---

##  Código relevante

### Script de patrullaje con detección de jugador:

```csharp
void Update() {
    float velocidad = agente.velocity.magnitude;
    animator.SetFloat("velocidad", velocidad);

    if (persiguiendo) {
        agente.SetDestination(jugador.position);
        if (Vector3.Distance(transform.position, jugador.position) < distanciaDeAlcance) {
            agente.ResetPath();
        }
    } else {
        if (!agente.pathPending && agente.remainingDistance < 0.5f) {
            index = (index + 1) % puntos.Length;
            agente.SetDestination(puntos[index].position);
        }
    }
}

void OnTriggerEnter(Collider other) {
    if (other.CompareTag("Player")) {
        persiguiendo = true;
    }
}
```

---

## 🎥 Evidencia visual

> Los GIFs muestran el personaje patrullando entre puntos, y cómo al detectar al jugador con su zona de visión (Collider), cambia a modo persecución y se detiene al alcanzarlo.
![alt text](<Grabación 2025-07-13 043428.gif>)



## 💬 Reflexión final

El taller permitió comprender de forma práctica cómo aplicar conceptos básicos de inteligencia artificial y animación en personajes de videojuegos. Las mayores dificultades estuvieron en:
- Configurar correctamente los avatares y animaciones importadas desde Mixamo.
- Ajustar los valores de velocidad del `NavMeshAgent` para que las transiciones entre animaciones se activaran correctamente.
- Lograr una detección funcional del jugador sin que ocurriera a través de muros (aunque finalmente se optó por una solución con `Collider`, sin raycast).

Este tipo de comportamientos son esenciales para NPCs en videojuegos, simulaciones, o proyectos XR.

---

## ✅ Checklist de entrega

- [x] Patrullaje funcional
- [x] Control de animaciones con velocidad
- [x] Detección de jugador con trigger
- [x] Cambio de comportamiento y parada
- [x] README documentado
- [x] Capturas o GIFs de evidencia