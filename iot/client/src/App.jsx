import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

// ['microwave', 'book', 'wall', 'waterfilter', 'desk', 'kettle']

const App = () => {
  const [socket, setSocket] = useState(undefined);

  useEffect(() => {
    const serverSocket = io('http://localhost:4000');
    setSocket(serverSocket);
    return () => {
      serverSocket.disconnect();
      setSocket(undefined);
    };
  }, []);

  return <div className='App'></div>;
};

export default App;
