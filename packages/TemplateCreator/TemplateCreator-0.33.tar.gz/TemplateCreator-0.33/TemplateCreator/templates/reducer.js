import initialState from './{{ component_name }}.state';
import { SUCCESS_SUFFIX } from '../../constants';

const {{ component_name }} = (state = initialState, action) => {
  switch (action.type) {

    default:
      return state;
  }
};

export default {{ component_name }};
