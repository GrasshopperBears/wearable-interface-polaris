import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Blackboard = ({ lastObject }) => {
  const [turnedOn, setTurnedOn] = useState(false);

  useEffect(() => {
    if (lastObject.object === 'blackboard') setTurnedOn(!turnedOn);
  }, [lastObject]);

  return <Wrapper>{turnedOn ? <Img src='screen-down.jpeg'></Img> : <Img src='screen-up.jpeg'></Img>}</Wrapper>;
};

const Wrapper = styled.div`
  width: 100%;
  height: 100%;
`;

const Img = styled.img`
  width: 100%;
  height: 100%;
  object-fit: contain;
`;

export default Blackboard;
