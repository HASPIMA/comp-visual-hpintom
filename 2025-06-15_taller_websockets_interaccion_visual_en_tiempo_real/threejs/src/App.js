import React, { useEffect, useState } from "react";

function App() {
  const [position, setPosition] = useState({ x: 0, y: 0, color: "black" });

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8765");

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setPosition(data);
    };

    return () => socket.close();
  }, []);

  const style = {
    position: "absolute",
    left: `${position.x * 50 + 200}px`,
    top: `${position.y * 50 + 200}px`,
    width: "20px",
    height: "20px",
    backgroundColor: position.color,
    borderRadius: "50%",
    transition: "all 0.5s ease"
  };

  return (
    <div>
      <h1>WebSocket Visualizador</h1>
      <div style={style}></div>
    </div>
  );
}

export default App;
