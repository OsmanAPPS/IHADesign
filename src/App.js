import React, { useState } from 'react';
import './App.css';
import ControlPanel from './components/ControlPanel';
import Viewer from './components/Viewer';

function App() {
  const [wingSpan, setWingSpan] = useState(30);
  const [fuselageLength, setFuselageLength] = useState(50);
  const [tailHeight, setTailHeight] = useState(10);

  return (
    <div className="App">
      <div className="container">
        <ControlPanel
          wingSpan={wingSpan}
          setWingSpan={setWingSpan}
          fuselageLength={fuselageLength}
          setFuselageLength={setFuselageLength}
          tailHeight={tailHeight}
          setTailHeight={setTailHeight}
        />
        <Viewer
          wingSpan={wingSpan}
          fuselageLength={fuselageLength}
          tailHeight={tailHeight}
        />
      </div>
    </div>
  );
}

export default App;
