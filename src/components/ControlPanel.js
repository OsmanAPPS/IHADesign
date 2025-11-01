import React from 'react';
import './ControlPanel.css';

const ControlPanel = ({
  wingSpan,
  setWingSpan,
  fuselageLength,
  setFuselageLength,
  tailHeight,
  setTailHeight,
}) => {
  return (
    <div className="control-panel">
      <h2>Airplane Controls</h2>
      <div className="control">
        <label>Wing Span: {wingSpan}</label>
        <input
          type="range"
          min="10"
          max="50"
          value={wingSpan}
          onChange={(e) => setWingSpan(Number(e.target.value))}
        />
      </div>
      <div className="control">
        <label>Fuselage Length: {fuselageLength}</label>
        <input
          type="range"
          min="20"
          max="80"
          value={fuselageLength}
          onChange={(e) => setFuselageLength(Number(e.target.value))}
        />
      </div>
      <div className="control">
        <label>Tail Height: {tailHeight}</label>
        <input
          type="range"
          min="5"
          max="20"
          value={tailHeight}
          onChange={(e) => setTailHeight(Number(e.target.value))}
        />
      </div>
    </div>
  );
};

export default ControlPanel;
