import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Glassdoor = ({ lastObject }) => {
  const [turnedOn, setTurnedOn] = useState(false);

  useEffect(() => {
    if (lastObject.object === 'glassdoor') setTurnedOn(!turnedOn);
  }, [lastObject]);

  return <Wrapper>{turnedOn ? <Img src='lock.mp4' autoPlay={true}></Img> : <Img src='unlock.mp4' autoPlay={true}></Img>}</Wrapper>;
};

const Wrapper = styled.div`
  width: 100%;
  height: 100%;
`;

const Img = styled.video`
  width: 100%;
  height: 100%;
  object-fit: contain;
`;

export default Glassdoor;
