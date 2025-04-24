# Processing animation results

We got three squares that are animated in a circular motion, rotating and scaling
over time. The animation is created using the Processing programming language, which
is designed for visual arts and graphics. The code uses the `translate()` and
`rotate()` functions to manipulate the squares' positions and angles.

## Final Result

![Final Result](docs/animation.gif)

## Square Behaviors

### Square 1 (Black Square)

- **Color**: Filled with black (RGB value 0)
- **Size**: Starts with size of 50 pixels, dynamically changes based on the distance
of the mouse cursor from the center of the canvas
- **Position**: Set to coordinates (1, 2) in the canvas, near the top-left corner
- **Drawing Mode**: Uses CORNER rectMode, meaning the square is positioned with its
top-left corner at the given coordinates
- **Rotation**: Rotates based on a sine function that depends on both the frame count
and mouse Y position (`sin(frameCount * 0.01 + mouseY * 0.1)`)
- **Transformation**: Size changes based on mouse distance from center - moving the
mouse closer to the center shrinks the square, while moving it away enlarges the
square
- **Special Behavior**: This square doesn't move positions, but it rotates in place
and "breathes" (expands/contracts) based on mouse position

### Square 2 (Red Square)

- **Color**: Filled with red (RGB value 255, 0, 0)
- **Size**: Fixed at 100 pixels
- **Position**: Drawn at the center of the canvas (width/2, height/2)
- **Drawing Mode**: Uses CENTER rectMode, meaning the square is positioned with its
center at the given coordinates
- **Rotation**: Rotates based on a cosine function that depends on both the frame
count and mouse X position (`cos(frameCount * 0.1 + mouseX * 0.02)`)
- **Transformation**: The square rotates around its center point, with rotation speed
affected by both time (frameCount) and horizontal mouse movement
- **Special Behavior**: This square maintains its position and size but has a smooth,
oscillating rotation that changes direction based on the cosine wave

### Square 3 (Blue Square)

- **Color**: Filled with blue (RGB value 0, 0, 255)
- **Size**: Set to 100 pixels (same as Square 2)
- **Position**: Follows the mouse cursor position
- **Drawing Mode**: Uses CENTER rectMode, meaning the square is positioned with its
center at the mouse position
- **Rotation**: Constantly rotates at a steady rate (`frameCount * 0.05`),
independent of mouse position
- **Transformation**: The square follows the mouse position while continuously
rotating
- **Special Behavior**: Unlike the other squares, this one moves with the mouse
cursor to orbit around the canvas, creating a dynamic interaction with the user
