import { Leva, useControls } from 'leva'
import { Canvas, useFrame } from '@react-three/fiber'
import * as THREE from 'three'
import { useRef } from 'react'

function BrazoArticulado() {
  // Referencias
  const baseRef = useRef(null)
  const articulacion2Ref = useRef(null)
  const articulacion3Ref = useRef(null)
  const articulacion4Ref = useRef(null)
  const manoRef = useRef(null)
  const lineaRef = useRef(null)
  const trayectoria = useRef([])

  // Controles con Leva
  const { autoAnimar, angulo1, angulo2, angulo3, angulo4 } = useControls({
    autoAnimar: false,
    angulo1: { value: 0, min: -Math.PI, max: Math.PI },
    angulo2: { value: 0, min: -Math.PI, max: Math.PI },
    angulo3: { value: 0, min: -Math.PI, max: Math.PI },
    angulo4: { value: 0, min: -Math.PI, max: Math.PI },
  })

  // Lógica de animación
  useFrame(({ clock }) => {
    const t = clock.getElapsedTime()
    if (!manoRef.current || !lineaRef.current) return

    if (baseRef.current) baseRef.current.rotation.z = autoAnimar ? Math.sin(t) : angulo1
    if (articulacion2Ref.current) articulacion2Ref.current.rotation.z = autoAnimar ? Math.sin(t * 1.5) : angulo2
    if (articulacion3Ref.current) articulacion3Ref.current.rotation.z = autoAnimar ? Math.sin(t * 2) : angulo3
    if (articulacion4Ref.current) articulacion4Ref.current.rotation.z = autoAnimar ? Math.sin(t * 2.5) : angulo4

    const posicionMano = new THREE.Vector3()
    manoRef.current.getWorldPosition(posicionMano)
    trayectoria.current.push(posicionMano.clone())
    if (trayectoria.current.length > 100) trayectoria.current.shift()

    const geometria = new THREE.BufferGeometry().setFromPoints(trayectoria.current)
    lineaRef.current.geometry.dispose()
    lineaRef.current.geometry = geometria
  })

  return (
    <>
      {/* Primer brazo */}
      <group ref={baseRef} position={[0, 0, 0]}>
        <mesh position={[1, 0, 0]}>
          <boxGeometry args={[2, 0.3, 0.3]} />
          <meshStandardMaterial color="#a5d6a7" />
        </mesh>

        {/* Segundo */}
        <group ref={articulacion2Ref} position={[2, 0, 0]}>
          <mesh position={[1, 0, 0]}>
            <boxGeometry args={[2, 0.3, 0.3]} />
            <meshStandardMaterial color="#66bb6a" />
          </mesh>

          {/* Tercero */}
          <group ref={articulacion3Ref} position={[2, 0, 0]}>
            <mesh position={[1, 0, 0]}>
              <boxGeometry args={[2, 0.3, 0.3]} />
              <meshStandardMaterial color="#388e3c" />
            </mesh>

            {/* Cuarto */}
            <group ref={articulacion4Ref} position={[2, 0, 0]}>
              <mesh ref={manoRef} position={[1, 0, 0]}>
                <boxGeometry args={[2, 0.3, 0.3]} />
                <meshStandardMaterial color="#1b5e20" />
              </mesh>

              {/* Bola final ("mano") */}
              <mesh position={[2, 0, 0]}>
                <sphereGeometry args={[0.2, 16, 16]} />
                <meshStandardMaterial color="#4dd0e1" />
              </mesh>
            </group>
          </group>
        </group>
      </group>

      {/* Línea de trayectoria */}
      <primitive ref={lineaRef} object={new THREE.Line()} />
    </>
  )
}

export default function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', backgroundColor: '#f9f1e7' }}>
      <Canvas camera={{ position: [0, 0, 10], fov: 50 }}>
        <ambientLight />
        <pointLight position={[10, 10, 10]} />
        <BrazoArticulado />
      </Canvas>
      <Leva collapsed />
    </div>
  )
}
