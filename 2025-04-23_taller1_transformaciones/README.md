# Transformations

## Python (Colab or Jupyter Notebook)

Tools: matplotlib, numpy, imageio

* Create a 2D figure with points or shapes
* Apply translation, rotation, and scaling using transformation matrices
* Generate an animation (using loops or interpolation)
* Animate the transformation based on time (t) or the frame
* Export as an animated GIF using imageio

> Optional: Display the resulting matrix of each transformation and how it changes over time

### Results for python

## Unity (LTS version) (Optional)

Scenario:

* Create an empty 3D project
* Add a cube or sphere to the scene
* Create a C# script that applies:
* Random translation along the X or Y axis every few seconds
* Constant rotation dependent on Time.deltaTime
* Oscillating scale based on Mathf.Sin(Time.time)

> Requirements: Use transform.Translate(), transform.Rotate(), transform.localScale
