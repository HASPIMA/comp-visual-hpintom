import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import ParentGroup from "./ParentGroup";
import LevaControls from "./LevaControls";
import { useState } from "react";

function App() {
  // State to hold the current transformation values
  const [transform, setTransform] = useState({
    rotationY: 0,
    positionX: 0,
    positionY: 0,
    positionZ: 0,
  });

  return (
    <>
      {/* Leva panel to adjust transformations in real-time */}
      <LevaControls onChange={setTransform} />

      {/* Canvas containing the 3D scene */}
      <Canvas camera={{ position: [0, 2, 7], fov: 60 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[5, 5, 5]} />
        {/* Parent group with real-time props */}
        <ParentGroup {...transform} />
        <OrbitControls />
      </Canvas>
    </>
  );
}

export default App;
