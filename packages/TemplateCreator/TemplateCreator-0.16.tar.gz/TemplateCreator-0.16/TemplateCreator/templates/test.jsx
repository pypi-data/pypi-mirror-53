import React from 'react';
import { mount } from 'enzyme';
import GeneralUtils from '../../common/utils.js';

describe('{{ component_name }}', () => {
  let wrapper;

  const component = (<{{ component_name }} />);

  beforeAll(() => GeneralUtils.renderIntoDocument(component));

  beforeEach(() => {
    wrapper = mount(component);
  });

  it('test', () => {

  });
});
