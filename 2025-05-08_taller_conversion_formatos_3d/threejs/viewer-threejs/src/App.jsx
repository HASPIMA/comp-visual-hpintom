import React, { useState, Suspense } from 'react'
import { Canvas, useLoader } from '@react-three/fiber'
import { OrbitControls, useGLTF } from '@react-three/drei'
import { OBJLoader } from 'three-stdlib'
import { STLLoader } from 'three-stdlib'
import './App.css'

// This component loads and displays the selected 3D model format
function Model({ format }) {
  if (format === 'GLB') {
    // Load GLB model (if working properly)
    const gltf = useGLTF('/models/icosphere.glb')
    return <primitive object={gltf.scene} />
  }

  if (format === 'OBJ') {
    // Load OBJ format using the OBJLoader
    const obj = useLoader(OBJLoader, '/models/icosphere.obj')
    return (
      <group scale={[1.5, 1.5, 1.5]}>
        <primitive object={obj} />
      </group>
    )
  }

  if (format === 'STL') {
    // Load STL geometry and apply material
    const geometry = useLoader(STLLoader, '/models/icosphere.stl')
    return (
      <mesh geometry={geometry} scale={[1.5, 1.5, 1.5]}>
        <meshStandardMaterial color="lightblue" />
      </mesh>
    )
  }

  return null
}

function App() {
  const [format, setFormat] = useState('OBJ') // Default format

  return (
    <div className="app">
      {/* UI controls: switch between formats */}
      <div style={{ position: 'absolute', top: 20, left: 20, zIndex: 1 }}>
        <h3>3D Format Viewer</h3>
        <button onClick={() => setFormat('OBJ')}>OBJ</button>
        <button onClick={() => setFormat('STL')}>STL</button>
        <button onClick={() => setFormat('GLB')}>GLB</button>
        <p>Current format: <strong>{format}</strong></p>
      </div>

      {/* 3D canvas scene */}
      <Canvas camera={{ position: [0, 0, 3] }}>
        {/* Lighting */}
        <ambientLight intensity={0.4} />
        <directionalLight position={[2, 2, 2]} intensity={1} />
        <pointLight position={[0, 0, 4]} intensity={1} />

        {/* Interactive rotation/zoom */}
        <OrbitControls />

        {/* Load selected model */}
        <Suspense fallback={null}>
          <Model format={format} />
        </Suspense>
      </Canvas>
    </div>
  )
}

export default App
