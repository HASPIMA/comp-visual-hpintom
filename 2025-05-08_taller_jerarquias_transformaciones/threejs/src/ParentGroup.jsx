import { useRef } from "react";
import { useFrame } from "@react-three/fiber";

export default function ParentGroup({ rotationY, positionX, positionY, positionZ }) {
  // Reference to the group containing child meshes
  const groupRef = useRef();

  // This hook is called every frame (~60 times per second)
  useFrame(() => {
    if (groupRef.current) {
      // Apply the rotation and translation to the parent group
      groupRef.current.rotation.y = rotationY;
      groupRef.current.position.set(positionX, positionY, positionZ);
    }
  });

  return (
    // <group> allows us to transform the meshes together
    <group ref={groupRef}>
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="red" />
      </mesh>
      <mesh position={[1.5, 0, 0]}>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshStandardMaterial color="green" />
      </mesh>
      <mesh position={[-1.5, 1.5, 0]}>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshStandardMaterial color="blue" />
      </mesh>
    </group>
  );
}
