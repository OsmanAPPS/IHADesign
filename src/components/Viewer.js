import React, { useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import './Viewer.css';

const Airplane = ({ wingSpan, fuselageLength, tailHeight }) => {
  const ref = useRef();

  return (
    <group ref={ref}>
      {/* Fuselage */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[1, 1, fuselageLength]} />
        <meshStandardMaterial color="gray" />
      </mesh>
      {/* Wings */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[wingSpan, 0.2, 3]} />
        <meshStandardMaterial color="red" />
      </mesh>
      {/* Tail */}
      <mesh position={[0, tailHeight / 2, -fuselageLength / 2]}>
        <boxGeometry args={[1, tailHeight, 1]} />
        <meshStandardMaterial color="red" />
      </mesh>
    </group>
  );
};

const Viewer = ({ wingSpan, fuselageLength, tailHeight }) => {
  return (
    <div className="viewer">
      <Canvas>
        <ambientLight intensity={0.8} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <directionalLight position={[-10, -10, -5]} intensity={0.5} />
        <Airplane
          wingSpan={wingSpan}
          fuselageLength={fuselageLength}
          tailHeight={tailHeight}
        />
        <OrbitControls />
      </Canvas>
    </div>
  );
};

export default Viewer;
