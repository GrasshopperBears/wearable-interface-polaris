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
import FireExtinguisher from './components/FireExtinguisher';
import Glassdoor from './components/Glassdoor';
import Blackboard from './components/Blackboard';

// ['microwave', 'book', 'wall', 'waterfilter', 'desk', 'kettle']

const App = () => {
  const [socket, setSocket] = useState(undefined);
  const [lastObject, setLastObject] = useState({ object: undefined, arrived: Date.now() });
  const [displayName, setDisplayName] = useState('');

  useEffect(() => {
    const serverSocket = io('http://localhost:4000');
    setSocket(serverSocket);
    serverSocket.on('detect', (newObject) => {
      setLastObject({ object: newObject, arrived: Date.now() });
    });
    return () => {
      serverSocket.disconnect();
      setSocket(undefined);
    };
  }, []);

  useEffect(() => {
    let timer = undefined;
    if (lastObject.object) {
      setDisplayName(lastObject.object);
      timer = setTimeout(() => {
        setDisplayName('');
      }, 1000);
    }
    return () => {
      if (timer) clearTimeout(timer);
    };
  }, [lastObject]);

  return (
    <MainContainer className='App'>
      <Row>
        <ObjectGrid>{displayName.length > 0 && <ObjectName>{displayName}</ObjectName>}</ObjectGrid>
        <ObjectGrid object='microwave' lastObject={lastObject.object}>
          <Microwave lastObject={lastObject} />
        </ObjectGrid>
        <ObjectGrid object='book' lastObject={lastObject.object}>
          <Book lastObject={lastObject} />
        </ObjectGrid>
        <ObjectGrid object='fireextinguisher' lastObject={lastObject.object}>
          <FireExtinguisher lastObject={lastObject} />
        </ObjectGrid>
        <ObjectGrid object='glassdoor' lastObject={lastObject.object}>
          <Glassdoor lastObject={lastObject} />
        </ObjectGrid>
      </Row>
      <Row>
        <ObjectGrid object='wall' lastObject={lastObject.object}>
          <Wall lastObject={lastObject} />
        </ObjectGrid>
        <ObjectGrid object='waterfilter' lastObject={lastObject.object}>
          <Waterfilter lastObject={lastObject} />
        </ObjectGrid>
        <ObjectGrid object='desk' lastObject={lastObject.object}>
          <Desk lastObject={lastObject} />
        </ObjectGrid>
        <ObjectGrid object='kettle' lastObject={lastObject.object}>
          <Kettle lastObject={lastObject} />
        </ObjectGrid>
        <ObjectGrid object='blackboard' lastObject={lastObject.object}>
          <Blackboard lastObject={lastObject} />
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
  overflow: hidden;
`;

const Row = styled.div`
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 50%;
`;

const ObjectName = styled.p`
  font-size: 2.5rem;
  margin-top: 8rem;
  text-align: center;
`;

export default App;
