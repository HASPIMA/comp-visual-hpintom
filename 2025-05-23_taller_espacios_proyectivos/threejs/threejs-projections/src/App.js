


import React, { useRef } from 'react';
import { Canvas, useThree, useFrame } from '@react-three/fiber';
import { OrbitControls , PerspectiveCamera, OrthographicCamera} from '@react-three/drei';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useLocation
} from 'react-router-dom';



function RotatingObjects() {
  const groupRef = useRef();

  // Rotar el grupo lentamente (solo para demo)
  useFrame(() => {
    if (groupRef.current) {
      groupRef.current.rotation.y += 0.01;
    }
  });

  return (
    <group ref={groupRef}>
      <mesh position={[-1, 0, -1]}>
        <boxGeometry args={[0.5, 0.5, 0.5]} />
        <meshStandardMaterial color="orange" />
      </mesh>
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.4, 32, 32]} />
        <meshStandardMaterial color="skyblue" />
      </mesh>
      <mesh position={[1, 0, 1]}>
        <coneGeometry args={[0.3, 1, 32]} />
        <meshStandardMaterial color="lightgreen" />
      </mesh>
    </group>
  );
}

function Scene({ cameraType }) {
  const { size } = useThree();
  const aspect = size.width / size.height;
  const orthoSize = 2;

  if (cameraType === 'perspective') {
    return (
      <>
        <perspectiveCamera
          key="perspective"
          makeDefault
          position={[0, 0, 10]}
          fov={60}
          near={0.1}
          far={1000}
        />
        <OrbitControls
          enableZoom={true}
          enablePan={true}
          minDistance={5}
          maxDistance={20}
          target={[0, 0, 0]}
        />
        <RotatingObjects />
      </>
    );
  } else {
    return (
      <>
        <orthographicCamera
          key="orthographic"
          makeDefault
          position={[0, 0, 10]}
          zoom={100}
          near={0.1}
          far={1000}
          left={-aspect * orthoSize}
          right={aspect * orthoSize}
          top={orthoSize}
          bottom={-orthoSize}
          isOrthographicCamera={true}
        />
        {/* Cámara fija, sin controles que muevan la cámara */}
        {/* Rotamos los objetos */}
        <RotatingObjects />
      </>
    );
  }
}

function Navigation() {
  const location = useLocation();

  return (
    <div style={{ position: 'absolute', top: 20, left: 20, zIndex: 1 }}>
      <Link to="/perspective">
        <button disabled={location.pathname === '/perspective'} style={{ marginRight: 8 }}>
          Perspective
        </button>
      </Link>
      <Link to="/orthographic">
        <button disabled={location.pathname === '/orthographic'}>
          Orthographic
        </button>
      </Link>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Navigation />
      <Canvas style={{ height: '100vh', width: '100vw' }}>
        <Routes>
          <Route path="/perspective" element={<Scene cameraType="perspective" />} />
          <Route path="/orthographic" element={<Scene cameraType="orthographic" />} />
          <Route path="*" element={<Scene cameraType="perspective" />} />
        </Routes>
      </Canvas>
    </Router>
  );
}
