# Worshop 1: Transformations

This workshop aims to explore the fundamental concepts of geometric transformations
(translation, rotation and scale) in different visual programming environments.

## Python (Colab or Jupyter Notebook)

Tools: matplotlib, numpy, imageio

* Create a 2D figure with points or shapes
* Apply translation, rotation, and scaling using transformation matrices
* Generate an animation (using loops or interpolation)
* Animate the transformation based on time (t) or the frame
* Export as an animated GIF using `imageio`

> [!TIP]
> Display the resulting matrix of each transformation and how it changes over time

### Results for python

## Unity (LTS version) (Optional)

Scenario:

* Create an empty 3D project
* Add a cube or sphere to the scene
* Create a C# script that applies:
* Random translation along the X or Y axis every few seconds
* Constant rotation dependent on `Time.deltaTime`
* Oscillating scale based on `Mathf.Sin(Time.time)`

> [!IMPORTANT]
> Use `transform.Translate()`, `transform.Rotate()`, `transform.localScale`

## Three.js with React Three Fiber

Scenario:

* Create a project using Vite and React Three Fiber
* Add a 3D object (cube or sphere)
* Apply animations with `useFrame` to:
  * Move the object along a sine or circular trajectory
  * Rotate it on its own axis with incremental change each frame
  * Scale it smoothly with a time-based function (`Math.sin(clock.elapsedTime)`)

> [!TIP]
> Include `OrbitControls` to navigate the scene

### Results for Three.js

## Processing (2D or 3D)

Scenario:

* Create a simple sketch (2D or 3D)
* Draw a geometric figure (rect, ellipse, or box)
* Apply transformations using:
  * `translate()`, `rotate()`, `scale()`
  * `pushMatrix()` and `popMatrix()` to isolate transformations
  * `frameCount`, `millis()`, or `sin()` to create time-based transformations

> [!NOTE]
> A cube that rotates, moves in a wavy motion, and scales cyclically over time

### Results for Processing
