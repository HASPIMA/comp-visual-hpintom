import * as THREE from "three";
import { useRef, useState } from "react";
import { Canvas, useFrame, ThreeElements } from "@react-three/fiber";

function Box(props: ThreeElements["mesh"]) {
  const meshRef = useRef<THREE.Mesh>(null!);
  const [scale, setScale] = useState(1);

  useFrame((state, delta) => {
    const radius = 1.5;
    const angle = state.clock.elapsedTime;

    // Move the mesh up and down in a circular motion
    meshRef.current.position.y = Math.sin(angle) * radius;
    meshRef.current.position.x = Math.cos(angle) * radius;

    // Rotate the mesh around its own axis
    meshRef.current.rotation.x += delta;

    // Scale the mesh based on its position
    // It will scale up and down between 0.5 and 1.5
    const scaleFactor = Math.abs(Math.sin(angle) / 2 + 1);
    setScale(scaleFactor);
  });

  return (
    <mesh {...props} ref={meshRef} scale={scale}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={"#2f74c0"} />
    </mesh>
  );
}

function App() {
  return (
    <Canvas>
      <ambientLight intensity={Math.PI / 2} />
      <spotLight
        position={[10, 10, 10]}
        angle={0.15}
        penumbra={1}
        decay={0}
        intensity={Math.PI}
      />
      <pointLight position={[-10, -10, -10]} decay={0} intensity={Math.PI} />
      <Box position={[-1.5, 0, 0]} />
    </Canvas>
  );
}

export default App;
