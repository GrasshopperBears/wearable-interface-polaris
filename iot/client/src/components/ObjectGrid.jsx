import React from 'react';
import styled from 'styled-components';

const ObjectGrid = ({ children, object, lastObject }) => {
  return <Wrapper selected={object === lastObject}>{children}</Wrapper>;
};

const Wrapper = styled.div`
  box-sizing: border-box;
  width: 33vw;
  height: 50vh;
  border: ${({ selected }) => (selected ? '8px solid #FDCA40' : '')};
`;

export default ObjectGrid;
