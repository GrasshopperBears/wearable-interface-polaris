import React from 'react';
import styled from 'styled-components';

const ObjectGrid = ({ children, object, lastObject }) => {
  return (
    <Wrapper selected={object && object === lastObject}>
      {object && <Title>{object}</Title>}
      {children}
    </Wrapper>
  );
};

const Wrapper = styled.div`
  box-sizing: border-box;
  width: 33vw;
  height: 50vh;
  border: ${({ selected }) => (selected ? '8px solid #FDCA40' : '1px solid #000000')};
  position: relative;
`;

const Title = styled.div`
  background-color: black;
  color: white;
  font-size: 2rem;
  border-radius: 7px;
  text-align: center;
  width: 18rem;
  padding: 10px 0;
  position: absolute;
  top: 1rem;
  left: calc(50% - 9rem);
`;

export default ObjectGrid;
