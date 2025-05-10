
import React from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { useControls, folder } from 'leva'

// Datos iniciales
const data = [
  { id: 1, type: 'box', name: 'Cubo Rojo' },
  { id: 2, type: 'sphere', name: 'Esfera Azul' },
  { id: 3, type: 'box', name: 'Caja Verde' },
]

// Componente de objeto 3D con controles dinámicos
function Object3D({ id, type, name }) {
  const { position, scale, rotation, color } = useControls(name, {
    Transformaciones: folder({
      position: { value: [0, 0, 0], step: 0.1 },
      scale: { value: [2, 2, 2], step: 0.1 },
      rotation: { value: [0, 0, 0], step: 0.1 },
    }),
    Apariencia: folder({
      color: '#ffffff',
    }),
  })

  const geometry =
    type === 'box' ? <boxGeometry /> :
    type === 'sphere' ? <sphereGeometry args={[0.5, 32, 32]} /> :
    null

  return (
    <mesh position={position} scale={scale} rotation={rotation}>
      {geometry}
      <meshStandardMaterial color={color} />
    </mesh>
  )
}

// Escena principal
function Scene() {
  return (
    <>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} />
      {data.map((item) => (
        <Object3D key={item.id} {...item} />
      ))}
      <OrbitControls />
    </>
  )
}

// Render principal
export default function App() {
  return (
    <Canvas style={{width:'100vw',height:'100vh'}} camera={{ position: [0, 4, 10], fov: 50 }}>
      <Scene />
    </Canvas>
  )
}
