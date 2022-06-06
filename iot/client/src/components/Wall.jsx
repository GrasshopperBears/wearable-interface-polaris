import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Wall = ({ lastObject }) => {
  const [turnedOn, setTurnedOn] = useState(false);

  useEffect(() => {
    if (lastObject.object === 'wall') setTurnedOn(!turnedOn);
  }, [lastObject]);

  return <Wrapper>{turnedOn ? <Img src='light-on.jpg'></Img> : <Img src='light-off.jpg'></Img>}</Wrapper>;
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

export default Wall;
