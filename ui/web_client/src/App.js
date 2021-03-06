import React, { Component } from 'react';
import logo from './logo.png';
import './App.css';

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import MenuIcon from '@material-ui/icons/Menu';
import IconButton from '@material-ui/core/IconButton';

import openSocket from 'socket.io-client';

import Timer from './Timer';
import LogPanel from './LogPanel';

let initialState = {
  main: '',
  img: '',
  showLogs: true,
  gettension: '',
  qrcode: '',
  sequence: '',
  worldcamfeed: '',
  embarkedcamfeed: '',
  embarkedopencv: '',
  paths: ''
};

class App extends Component {
  state = initialState;

  timerRef = React.createRef();

  initialState() {
    initialState.socket = this.state.socket;
    this.setState(initialState);
  }

  componentWillMount() {
    let sockObj = {
      socket: openSocket('http://localhost:4001?token=UI')
    };
    let tstate = Object.assign({}, initialState, sockObj);
    this.setState(tstate);
  }

  componentDidMount() {
    this.state.socket.on('event', resp => {
      this.setState({ [resp.dest]: resp.data });
    });

    this.state.socket.on('sendStopSignal', resp => {
      this.timerRef.current.flipStatus();
      this.timerRef.current.stopTimer();
    });

    this.getTensionPokeOnPi();
  }

  getTensionPokeOnPi = () => {
    let piSocket = openSocket('http://192.168.0.38:4000');
    piSocket.on('recvTension', resp => {
      this.setState({ gettension: resp * 4 });
    });

    piSocket.on('recvImage', resp => {
      this.setState({ embarkedopencv: resp });
    });

    setInterval(() => {
      piSocket.emit('getTension', 'From React UI Phantom');
      piSocket.emit('getImage', 'Un frame please');
    }, 500);
  };

  startSignal = () => {
    this.initialState();
    this.state.socket.emit('start', 'start');
    console.log('start signal sent');
  };

  resetSignal = () => {
    this.initialState();
    console.log('reset signal sent');
  };

  renderImage = image => {
    let imgR = 'data:image/jpg;base64, ' + image;
    if (image === '') {
      return <img src={logo} width={30} alt='logo' />;
    }

    return <img src={imgR} alt='logo' />;
  };

  openLogPanel = () => {
    document.getElementById('log-panel').style.display = 'block';
    document.getElementsByClassName('main-container')[0].style.justifyContent =
      'space-between';
  };

  closeLogPanel = () => {
    document.getElementById('log-panel').style.display = 'none';
    document.getElementsByClassName('main-container')[0].style.justifyContent =
      'center';
  };

  toggleLogPanel = () => {
    this.state.showLogs ? this.openLogPanel() : this.closeLogPanel();
    this.setState({ showLogs: !this.state.showLogs });
  };

  render() {
    return (
      <div style={app}>
        <AppBar position='static' color='primary'>
          <Toolbar style={toolbar}>
            <Typography variant='h6' color='inherit'>
              Station de base
            </Typography>
            <IconButton color='inherit'>
              <MenuIcon onClick={this.toggleLogPanel} />
            </IconButton>
          </Toolbar>
        </AppBar>

        <div
          className='main-container'
          id='main-container'
          style={mainContainer}
        >
          <Paper elevation={15} style={mainPaper}>
            <div style={container}>
              <Paper elevation={4} style={paperStyle}>
                <h4 style={textStyle}>Informations Robot</h4>
                <div style={textContainer}>
                  <span className='bold-font'>
                    Tension condensateur: {this.state.gettension}{' '}
                  </span>
                  <span className='bold-font'>
                    Statut Robot: {this.state.sequence}{' '}
                  </span>
                  <span className='bold-font'>
                    Code QR: {this.state.qrcode}{' '}
                  </span>
                </div>
              </Paper>
              <Paper elevation={4} style={paperStyle}>
                <Timer
                  ref={this.timerRef}
                  startSignal={this.startSignal}
                  resetSignal={this.resetSignal}
                />
              </Paper>
            </div>
            <div style={container}>
              <Paper elevation={4} style={paperStyle}>
                <h4 style={textStyle}>Caméra embarquée (live feed)</h4>
                <div> {this.renderImage(this.state.embarkedopencv)} </div>
              </Paper>
              <Paper elevation={4} style={paperStyle}>
                <h4 style={textStyle}>Caméra embarquée (image courante)</h4>
                <div> {this.renderImage(this.state.embarkedcamfeed)} </div>
              </Paper>
            </div>
            <div style={container}>
              <Paper elevation={4} style={paperStyle}>
                <h4 style={textStyle}>Trajectoire planifiée & réelle</h4>
                <div> {this.renderImage(this.state.paths)} </div>
              </Paper>
              <Paper elevation={4} style={paperStyle}>
                <h4 style={textStyle}>Caméra monde (image courante)</h4>
                <div> {this.renderImage(this.state.worldcamfeed)} </div>
              </Paper>
            </div>
          </Paper>
          <LogPanel socket={this.state.socket} />
        </div>
      </div>
    );
  }
}

const textStyle = {
  marginTop: '0px'
};

const app = {
  textAlign: 'center',
  height: '100%',
  margin: '0px'
};

const paperStyle = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  width: '100%',
  margin: '10px',
  padding: '10px'
};

const container = {
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'center',
  flexGrow: '1',
  margin: '0px'
};

const mainContainer = {
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'center',
  margin: '0px',
  overflow: 'auto'
};

const mainPaper = {
  marginLeft: '100px',
  height: 'calc(100% - 34px)',
  width: '90%',
  alignItems: 'center',
  marginRight: '100px',
  marginTop: '10px',
  paddingBottom: '10px'
};

const toolbar = {
  alignItems: 'center',
  justifyContent: 'space-between'
};

const textContainer = {
  display: 'flex',
  textAlign: 'left',
  flexDirection: 'column',
  width: '90%'
};

export default App;
