import React, { Component } from 'react';

class LogPanel extends Component {
  state = {
    logs: []
  };

  componentDidMount() {
    this.props.socket.on('event', resp => {
      if (resp.type === 'img') {
        return;
      }

      let newLogs = this.state.logs;
      newLogs.push(resp.data);
      this.setState({ logs: newLogs });
    });
  }

  displayLogs = () => {
    let t = this.state.logs;

    return t.map(log => {
      return <p> {log} </p>;
    });
  };

  render() {
    return (
      <div id='log-panel' style={logPanel}>
        {this.displayLogs()}
      </div>
    );
  }
}

const logPanel = {
  backgroundColor: 'white',
  width: '40%',
  display: 'none',
  overflow: 'scroll',
  WebkitBoxShadow: '-6px 2px 8px #999999'
};

export default LogPanel;
