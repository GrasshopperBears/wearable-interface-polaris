import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Book = ({ lastObject }) => {
  const [turnedOn, setTurnedOn] = useState(false);

  useEffect(() => {
    if (lastObject.object === 'book') setTurnedOn(!turnedOn);
  }, [lastObject]);

  return <Wrapper>{turnedOn ? <Img src='phone-on.jpg'></Img> : <Img src='phone-off.jpg'></Img>}</Wrapper>;
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

export default Book;
