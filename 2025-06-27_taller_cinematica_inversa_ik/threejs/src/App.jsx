import { Canvas, useFrame } from '@react-three/fiber'
import { Leva, useControls } from 'leva'
import * as THREE from 'three'
import { useRef } from 'react'

function BrazoIK() {
  const { x, y } = useControls({
    x: { value: 2, min: -5, max: 5 },
    y: { value: 2, min: -5, max: 5 },
  })

  const longitudes = [2, 2, 2]

  const ref1 = useRef(), ref2 = useRef(), ref3 = useRef(), manoRef = useRef(), lineaRef = useRef()
  const trayectoria = useRef([])

  useFrame(() => {
    const objetivo = new THREE.Vector2(x, y)

    // Posiciones en 3D (corrección principal)
    const p1 = new THREE.Vector3()
    const p2 = new THREE.Vector3()
    const p3 = new THREE.Vector3()
    const p4 = new THREE.Vector3()

    ref1.current.getWorldPosition(p1)
    ref2.current.getWorldPosition(p2)
    ref3.current.getWorldPosition(p3)
    manoRef.current.getWorldPosition(p4)

    // CCD IK: desde mano a base
    const segmentos = [
      { joint: ref3, pos: p3 },
      { joint: ref2, pos: p2 },
      { joint: ref1, pos: p1 },
    ]

    for (let i = 0; i < 3; i++) {
      const { joint } = segmentos[i]
      joint.current.updateWorldMatrix(true, false)
      joint.current.parent.updateWorldMatrix(true, false)

      const actual3D = new THREE.Vector3()
      joint.current.getWorldPosition(actual3D)

      const actual2D = new THREE.Vector2(actual3D.x, actual3D.y)
      const p4_2D = new THREE.Vector2(p4.x, p4.y)

      const toEnd = p4_2D.clone().sub(actual2D).normalize()
      const toTarget = objetivo.clone().sub(actual2D).normalize()

      const angle = Math.acos(THREE.MathUtils.clamp(toEnd.dot(toTarget), -1, 1))
      const cross = toEnd.cross(toTarget)

      if (cross !== 0 && !isNaN(angle)) {
        joint.current.rotation.z += cross > 0 ? angle : -angle
      }

      // Actualizar posición de la mano para el siguiente paso
      manoRef.current.getWorldPosition(p4)
    }

    // Trayectoria
    const puntoActual = new THREE.Vector3()
    manoRef.current.getWorldPosition(puntoActual)
    trayectoria.current.push(puntoActual.clone())
    if (trayectoria.current.length > 100) trayectoria.current.shift()

    // Actualizar línea
    const geometry = new THREE.BufferGeometry().setFromPoints(trayectoria.current)
    lineaRef.current.geometry.dispose()
    lineaRef.current.geometry = geometry
  })

  return (
    <>
      {/* Primer segmento */}
      <group ref={ref1} position={[0, 0, 0]}>
        <mesh position={[longitudes[0] / 2, 0, 0]}>
          <boxGeometry args={[longitudes[0], 0.3, 0.3]} />
          <meshStandardMaterial color="#689f38" />
        </mesh>

        {/* Segundo segmento */}
        <group ref={ref2} position={[longitudes[0], 0, 0]}>
          <mesh position={[longitudes[1] / 2, 0, 0]}>
            <boxGeometry args={[longitudes[1], 0.3, 0.3]} />
            <meshStandardMaterial color="#388e3c" />
          </mesh>

          {/* Tercer segmento */}
          <group ref={ref3} position={[longitudes[1], 0, 0]}>
            <mesh ref={manoRef} position={[longitudes[2] / 2, 0, 0]}>
              <boxGeometry args={[longitudes[2], 0.3, 0.3]} />
              <meshStandardMaterial color="#1b5e20" />
            </mesh>

            {/* Esfera como mano */}
            <mesh position={[longitudes[2], 0, 0]}>
              <sphereGeometry args={[0.2, 16, 16]} />
              <meshStandardMaterial color="#9c1c46" />
            </mesh>
          </group>
        </group>
      </group>

      {/* Punto objetivo */}
      <mesh position={[x, y, 0]}>
        <sphereGeometry args={[0.15, 16, 16]} />
        <meshStandardMaterial color="#9c1c46" />
      </mesh>

      {/* Línea trayectoria */}
      <line ref={lineaRef}>
        <bufferGeometry />
        <lineBasicMaterial color="#9c1c46" linewidth={2} />
      </line>
    </>
  )
}

export default function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', backgroundColor: '#fbeceb' }}>
      <Canvas camera={{ position: [0, 0, 10], fov: 50 }}>
        <ambientLight />
        <pointLight position={[10, 10, 10]} />
        <BrazoIK />
      </Canvas>
      <Leva collapsed />
    </div>
  )
}
