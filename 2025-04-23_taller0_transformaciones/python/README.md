# Python final result

The final result is an animated GIF that shows a triangle (the original shape)
being transformed through a sequence of combined transformations over 60
frames.

![Animation](docs/animation.gif)

## The Animation Process

1. **Initial Setup**:
   - A triangle shape is defined as the original shape
   - 60 animation frames are created
   - The transformation parameters change gradually across frames:
     - Rotation angles from 0 to $2\pi$ radians
     - Scaling factors from 1 to 2
     - Translation distances from 0 to 5 units in both x and y directions
  
    ```py
    import numpy as np

    num_frames = 60
    angles = np.linspace(0, 2 * np.pi, num_frames)
    scales = np.linspace(1, 2, num_frames)
    translations = np.linspace(0, 5, num_frames)
    ```

2. **For Each Frame**:
   - A transformation matrix is computed by combining:
     - Scaling (S)
     - Rotation (R)
     - Translation (T)
   - The transformation is applied to the triangle using homogeneous coordinates
   - The transformed shape is plotted
   - The current transformation matrix is displayed on the plot
   - Each frame is saved as a PNG file in the "out" directory

3. **Final Output**:
   - All the frame images are combined into a smooth animation as a GIF
   - The GIF is saved as "out/animation.gif"
   - The resulting animation shows the triangle simultaneously rotating, growing in size, and moving diagonally

The final animation provides a visual demonstration of how composite 2D
transformations work in computer graphics, showing how rotation, scaling,
and translation can be combined into a single transformation matrix and applied to
a shape.
