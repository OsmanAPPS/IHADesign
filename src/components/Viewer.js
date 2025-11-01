import React, { useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import './Viewer.css';

// A more realistic fuselage using a cylinder
const Fuselage = ({ fuselageLength }) => {
  return (
    <mesh rotation={[Math.PI / 2, 0, 0]}>
      <cylinderGeometry args={[0.5, 0.7, fuselageLength, 32]} />
      <meshStandardMaterial color="silver" />
    </mesh>
  );
};

// Wings with a more appropriate shape
const Wings = ({ wingSpan }) => {
  return (
    <mesh position={[0, 0, 0]}>
      <boxGeometry args={[wingSpan, 0.2, 4]} />
      <meshStandardMaterial color="#b0b0b0" />
    </mesh>
  );
};

// Tail section with vertical and horizontal stabilizers
const Tail = ({ tailHeight, fuselageLength }) => {
  return (
    <group position={[0, 0, -fuselageLength / 2]}>
      {/* Vertical Stabilizer (Tail Fin) */}
      <mesh position={[0, tailHeight / 2 + 0.5, 0]}>
        <boxGeometry args={[0.2, tailHeight, 3]} />
        <meshStandardMaterial color="#b0b0b0" />
      </mesh>
      {/* Horizontal Stabilizers */}
      <mesh position={[0, 0.5, 0]}>
        <boxGeometry args={[8, 0.15, 2.5]} />
        <meshStandardMaterial color="#b0b0b0" />
      </mesh>
    </group>
  );
};

const Airplane = ({ wingSpan, fuselageLength, tailHeight }) => {
  const ref = useRef();

  return (
    <group ref={ref} rotation={[0, Math.PI / 2, 0]}>
      <Fuselage fuselageLength={fuselageLength} />
      <Wings wingSpan={wingSpan} />
      <Tail tailHeight={tailHeight} fuselageLength={fuselageLength} />
    </group>
  );
};

const Viewer = ({ wingSpan, fuselageLength, tailHeight }) => {
  return (
    <div className="viewer">
      <Canvas camera={{ position: [20, 20, 20], fov: 50 }}>
        <ambientLight intensity={0.8} />
        <directionalLight position={[10, 10, 5]} intensity={1.5} />
        <directionalLight position={[-10, -10, -5]} intensity={0.7} />
        <Airplane
          wingSpan={wingSpan}
          fuselageLength={fuselageLength}
          tailHeight={tailHeight}
        />
        <OrbitControls />
        <gridHelper args={[100, 100]} />
      </Canvas>
    </div>
  );
};

export default Viewer;
