import React from 'react';
import styled from 'styled-components';

const ObjectGrid = ({ children, object, lastObject }) => {
  return (
    <Wrapper selected={object === lastObject}>
      <Title>{object}</Title>
      {children}
    </Wrapper>
  );
};

const Wrapper = styled.div`
  box-sizing: border-box;
  width: 33vw;
  height: 50vh;
  border: ${({ selected }) => (selected ? '8px solid #FDCA40' : '')};
  position: relative;
`;

const Title = styled.div`
  background-color: black;
  color: white;
  font-size: 3rem;
  border-radius: 7px;
  text-align: center;
  width: 24rem;
  padding: 10px 0;
  position: absolute;
  left: calc(50% - 12rem);
`;

export default ObjectGrid;
