import React, { Component } from 'react';
import Button from '@material-ui/core/Button';

import timeFormat from './util/TimeFormater';

class Timer extends Component {
  state = {
    status: false,
    time: 0,
    start: 0
  };

  startSignalHandler = () => {
    if (!this.state.status) {
      this.props.startSignal();
    }

    this.state.status ? this.stopTimer() : this.startTimer();
    this.setState({ status: !this.state.status });
  };

  startTimer = () => {
    this.setState({
      time: this.state.time,
      start: Date.now() - this.state.time
    });

    this.timer = setInterval(
      () =>
        this.setState({
          time: Date.now() - this.state.start
        }),
      1000
    );
  };

  flipStatus = () => {
    this.setState({ status: !this.state.status });
  };

  stopTimer = () => {
    clearInterval(this.timer);
  };

  resetSignalHandler = () => {
    this.props.resetSignal();
    this.setState({ time: 0 });
  };

  render() {
    const { status, time } = this.state;
    return (
      <div style={container}>
        <h2 style={timerStyle}>{timeFormat(time)}</h2>
        <Button
          variant='contained'
          color='primary'
          style={buttonStyle}
          onClick={this.startSignalHandler}
        >
          {status ? 'Stop' : 'Start'}
        </Button>
        <Button
          variant='contained'
          color='primary'
          style={buttonStyle}
          onClick={this.resetSignalHandler}
        >
          Reset
        </Button>
      </div>
    );
  }
}

const buttonStyle = {
  margin: '10px'
};

const timerStyle = {
  border: '2px rgb(63, 81, 181) solid',
  borderRadius: '2px',
  backgroundColor: 'rgb(240, 240, 240)'
};

const container = {
  maxWidth: '200px'
};

export default Timer;
