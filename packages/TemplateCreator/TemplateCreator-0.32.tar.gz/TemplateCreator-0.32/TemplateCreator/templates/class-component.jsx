import React, { component } from 'react';
import PropTypes from 'prop-types';

import styles from './{{ component_name }}.styles.scss';

class {{ component_name }} extends Component {
  constructor(props) {
    super(props);
    this.state = {  }
  }
  render() {
    return (
      <div className={styles.container}>{{ component_name }}</div>
    );
  }
}

{{ component_name }}.propTypes = {

};

{{ component_name }}.defaultProps = {

};

export default {{ component_name }};
