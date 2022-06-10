import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const FireExtinguisher = ({ lastObject }) => {
  const [turnedOn, setTurnedOn] = useState(false);

  useEffect(() => {
    if (lastObject.object === 'fireextinguisher') setTurnedOn(!turnedOn);
  }, [lastObject]);

  return (
    <Wrapper>
      {turnedOn ? (
        <Container>
          <Img src='message.png'></Img>
          <Text>"Help! There's a fire!"</Text>
        </Container>
      ) : (
        <></>
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
  font-size: 2rem;
  font-weight: bold;
`;

const Img = styled.img`
  width: 40%;
  height: 40%;
  object-fit: contain;
  margin: 1rem;
`;

export default FireExtinguisher;
