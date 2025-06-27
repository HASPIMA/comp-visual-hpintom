import { Canvas, useFrame } from '@react-three/fiber'
import { Leva, useControls, button } from 'leva'
import { useRef, useState } from 'react'
import * as THREE from 'three'

function EscenaInteractiva() {
  const mallaRef = useRef()
  const [rotar, setRotar] = useState(false)

  const { escala, color, rotacion } = useControls({
    escala: { value: 1, min: 0.2, max: 3 },
    color: '#4caf50',
    rotacion: button(() => {
      setRotar((prev) => !prev)
    }),
  })

  useFrame(() => {
    if (rotar && mallaRef.current) {
      mallaRef.current.rotation.y += 0.01
    }
  })

  return (
    <mesh ref={mallaRef} scale={[escala, escala, escala]}>
      <torusGeometry args={[1, 0.4, 16, 100]} />
      <meshStandardMaterial color={color} />
    </mesh>
  )
}

export default function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', backgroundColor: '#fdf6ec' }}>
      <Canvas camera={{ position: [0, 0, 6], fov: 60 }}>
        <ambientLight />
        <pointLight position={[10, 10, 10]} />
        <EscenaInteractiva />
      </Canvas>
      <Leva collapsed={false} />
    </div>
  )
}
