import React, { useState, useEffect, useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { Html } from '@react-three/drei'

function Box({ position, setPosition }) {
  const ref = useRef()
  const [active, setActive] = useState(false)

  // Rotate the cube continuously
  useFrame(() => {
    if (ref.current) {
      ref.current.rotation.y += 0.01
      ref.current.rotation.x += 0.005
    }
  })

  return (
    <mesh
      ref={ref}
      position={position}
      onClick={() => {
        setActive(!active)
        if (!active) {
          // When activating, move cube to random position
          const x = (Math.random() - 0.5) * 4
          const y = (Math.random() - 0.5) * 4
          const z = (Math.random() - 0.5) * 4
          setPosition([x, y, z])
        }
      }}
      scale={active ? 1.5 : 1}
    >
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color={active ? 'orange' : 'royalblue'} />
      {/* Show button inside the 3D scene when active */}
      {active && (
        <Html position={[0, 1.2, 0]}>
          <button onClick={() => alert('Button clicked!')}>Click me</button>
        </Html>
      )}
    </mesh>
  )
}

function Controls({ setPosition }) {
  useEffect(() => {
    function onKeyDown(e) {
      if (e.key === 'r' || e.key === 'R') {
        setPosition([0, 0, 0]) // Reset cube position to origin
      }
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [setPosition])

  return null
}

export default function App() {
  const [position, setPosition] = useState([0, 0, 0])

  return (
    <>
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight />
        <pointLight position={[10, 10, 10]} />
        <Box position={position} setPosition={setPosition} />
        <Controls setPosition={setPosition} />
      </Canvas>
      {/* External reset button */}
      <div style={{ position: 'absolute', top: 20, left: 20, zIndex: 10 }}>
        <button onClick={() => setPosition([0, 0, 0])}>Reset Position (R)</button>
      </div>
    </>
  )
}
