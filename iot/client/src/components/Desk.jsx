import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Desk = ({ lastObject }) => {
  const [audio] = useState(new Audio('music.m4a'));
  const [turnedOn, setTurnedOn] = useState(false);

  useEffect(() => {
    audio.autoplay = false;
    if (lastObject.object === 'desk') {
      if (!turnedOn) audio.play();
      setTurnedOn(!turnedOn);
    }
  }, [lastObject]);

  return <Wrapper>{turnedOn ? <Img src='speaker-on.jpg'></Img> : <Img src='speaker-off.jpg'></Img>}</Wrapper>;
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

export default Desk;
