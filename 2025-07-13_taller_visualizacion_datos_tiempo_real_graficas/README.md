# Taller - Visualización de Datos en Tiempo Real: Gráficas en Movimiento

##  Fecha
2025-07-12



##  Objetivo del Taller

Explorar cómo visualizar datos numéricos que cambian en el tiempo mediante gráficos dinámicos que se actualicen en vivo. Se busca simular una métrica que pueda ser monitoreada como si viniera de un sensor o fuente real, con aplicaciones en dashboards, visualización científica o monitoreo.

---

##  Tipo de datos utilizados

Se utilizaron datos **simulados**, generados mediante una función sinusoidal modificada con ruido aleatorio. Esta simulación representa fenómenos periódicos como temperatura, pulso, vibración o señal electromagnética, incorporando variabilidad natural con ruido.

La fórmula utilizada fue:

```
y = np.sin(t * 0.1) + np.random.normal(0, 0.1)
```

Donde `t` es el tiempo simulado (por frames).

---
##  Herramientas y tecnologías

- Python 3 (usado en Google Colab)
- `matplotlib` para la visualización animada
- `numpy` para generación de datos
- `pandas` para manipulación de series
- Grabadora externa para generar el GIF (no se usó exportación automática)



##  Código relevante

```python
def update(frame):
    t = frame
    x_data.append(t)
    y = np.sin(t * 0.1) + np.random.normal(0, 0.1)
    y_data.append(y)
    if len(x_data) > 100:
        x_data.pop(0)
        y_data.pop(0)
    line.set_data(x_data, y_data)
    ax.set_xlim(max(0, t - 100), t)
    return line,
```

La animación fue controlada con `FuncAnimation` de `matplotlib`, actualizando la señal en tiempo real en función del frame.

---

##  Evidencia visual

> El GIF adjunto muestra el gráfico actualizándose dinámicamente con el paso del tiempo. Los datos siguen una forma ondulada con variaciones aleatorias que simulan ruido o perturbaciones naturales.

![alt text](<Grabación 2025-07-13 002523.gif>)

---

## 💬 Reflexión final

La visualización de datos en tiempo real es una herramienta muy útil para monitorear procesos que evolucionan continuamente. Este ejercicio permitió experimentar con una animación fluida que refleja dinámicas simples pero efectivas.

**Dificultades encontradas**:

---

## ✅ Checklist

- [x] Simulación de datos dinámica
- [x] Visualización animada en tiempo real
- [x] GIF generado y vinculado
- [x] Código comentado y modular
- [x] README completo con reflexión
