// src/LevaControls.jsx
import { Leva, useControls } from "leva";
import { useEffect } from "react";

export default function LevaControls({ onChange }) {
  // Define real-time controls with Leva:
  // These control the parent group's rotation and translation
  const controls = useControls({
    rotationY: { value: 0, min: -Math.PI, max: Math.PI, step: 0.01 },
    positionX: { value: 0, min: -5, max: 5, step: 0.1 },
    positionY: { value: 0, min: -5, max: 5, step: 0.1 },
    positionZ: { value: 0, min: -5, max: 5, step: 0.1 },
  });

  // When the values in Leva change, update the parent's state.
  // This prevents setting state during render, avoiding errors.
  useEffect(() => {
    onChange(controls);
  }, [controls, onChange]);

  return <Leva collapsed />;
}
