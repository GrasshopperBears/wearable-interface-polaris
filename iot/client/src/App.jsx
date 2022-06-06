import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import styled from 'styled-components';

import ObjectGrid from './components/ObjectGrid';
import Book from './components/Book';
import Desk from './components/Desk';
import Kettle from './components/Kettle';
import Microwave from './components/Microwave';
import Wall from './components/Wall';
import Waterfilter from './components/Waterfilter';

// ['microwave', 'book', 'wall', 'waterfilter', 'desk', 'kettle']

const App = () => {
  const [socket, setSocket] = useState(undefined);
  const [lastObject, setLastObject] = useState(undefined);

  useEffect(() => {
    const serverSocket = io('http://localhost:4000');
    setSocket(serverSocket);
    serverSocket.on('detect', (newObject) => {
      setLastObject(newObject);
    });
    return () => {
      serverSocket.disconnect();
      setSocket(undefined);
    };
  }, []);

  return (
    <MainContainer className='App'>
      <Row>
        <ObjectGrid object='microwave' lastObject={lastObject}>
          <Microwave />
        </ObjectGrid>
        <ObjectGrid object='book' lastObject={lastObject}>
          <Book />
        </ObjectGrid>
        <ObjectGrid object='wall' lastObject={lastObject}>
          <Wall />
        </ObjectGrid>
      </Row>
      <Row>
        <ObjectGrid object='waterfilter' lastObject={lastObject}>
          <Waterfilter />
        </ObjectGrid>
        <ObjectGrid object='desk' lastObject={lastObject}>
          <Desk />
        </ObjectGrid>
        <ObjectGrid object='kettle' lastObject={lastObject}>
          <Kettle />
        </ObjectGrid>
      </Row>
    </MainContainer>
  );
};

const MainContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
`;

const Row = styled.div`
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 50%;
`;

export default App;
