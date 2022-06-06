import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Microwave = ({ lastObject }) => {
  const [audio] = useState(new Audio('microwave.m4a'));
  const [turnedOn, setTurnedOn] = useState(false);

  useEffect(() => {
    if (lastObject.object === 'microwave') {
      if (!turnedOn) audio.play();
      setTurnedOn(!turnedOn);
    }
  }, [lastObject]);

  return <Wrapper>{turnedOn ? <Img src='microwave-on.jpg'></Img> : <Img src='microwave-off.jpg'></Img>}</Wrapper>;
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

export default Microwave;
