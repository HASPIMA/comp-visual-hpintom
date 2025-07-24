// src/Model.jsx
import { useLoader } from '@react-three/fiber'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { useEffect } from 'react'
import { Edges } from '@react-three/drei'
import * as THREE from 'three'

export default function Model() {
  const obj = useLoader(OBJLoader, '/modelo.obj')

  useEffect(() => {
    obj.traverse((child) => {
      if (child instanceof THREE.Mesh) {
        child.material = new THREE.MeshStandardMaterial({ color: 'lightblue', wireframe: false })
      }
    })
  }, [obj])

  return (
    <primitive object={obj}>
      <Edges threshold={15} color="black" />
    </primitive>
  )
}
