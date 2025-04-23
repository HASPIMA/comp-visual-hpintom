import * as THREE from "three";
import { useRef, useState } from "react";
import { Canvas, useFrame, ThreeElements } from "@react-three/fiber";

function Box(props: ThreeElements["mesh"]) {
  const meshRef = useRef<THREE.Mesh>(null!);
  const [scale, setScale] = useState(1);

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
