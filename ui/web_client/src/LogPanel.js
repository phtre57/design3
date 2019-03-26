import React, { Component } from 'react';

class LogPanel extends Component {
  render() {
    return (
      <div id="log-panel" style={logPanel}>
          <p>drop some logs over here</p>
      </div>
    );
  }
}

const logPanel = {
  backgroundColor: 'white',
  position: 'absolute',
  right: '0',
  height: '100%',
  width: '20%',
  display: 'none',
  overflow: 'hidden',
  webkitBoxShadow: '-6px 2px 8px #999999'
};

export default LogPanel;