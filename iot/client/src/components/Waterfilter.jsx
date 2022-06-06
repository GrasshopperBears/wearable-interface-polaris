import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Waterfilter = ({ lastObject }) => {
  const [turnedOn, setTurnedOn] = useState(false);

  useEffect(() => {
    if (lastObject.object === 'waterfilter') setTurnedOn(!turnedOn);
  }, [lastObject]);

  return (
    <Wrapper>
      {turnedOn ? (
        <Container>
          <Img src='water.jpg'></Img>
          <Text>Water ordered!</Text>
        </Container>
      ) : (
        <Container>
          <Img src='water-empty.jpg'></Img>
          <Text>Empty</Text>
        </Container>
      )}
    </Wrapper>
  );
};

const Wrapper = styled.div`
  width: 100%;
  height: 100%;
`;

const Container = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  padding-top: 2rem;
`;

const Text = styled.p`
  font-size: 3rem;
  font-weight: bold;
`;

const Img = styled.img`
  width: 70%;
  height: 70%;
  object-fit: contain;
`;

export default Waterfilter;
