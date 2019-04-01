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

class App extends Component {
  state = {
    main: '',
    img: '',
    showLogs: true,
    socket: openSocket('http://localhost:4001?token=UI')
  };

  componentDidMount() {
    this.state.socket.on('event', resp => {
      this.setState({ [resp.dest]: resp.data });
    });
  }

  startSignal = () => {
    this.state.socket.emit('start', 'start');
    console.log('start signal sent');
  };

  resetSignal = () => {
    console.log('reset signal sent');
  };

  renderImage = image => {
    let imgR = 'data:image/jpg;base64, ' + image;
    if (image === undefined) {
      return <img src={logo} width={30} alt='logo' />;
    }

    return <img src={imgR} style={imageStyle} alt='logo' />;
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
                  <span>Tension condensateur: {this.state.gettension} </span>
                  <span>Statut Robot: {this.state.sequence} </span>
                  <span>Code QR: {this.state.qrcode} </span>
                </div>
              </Paper>
              <Paper elevation={4} style={paperStyle}>
                <Timer
                  startSignal={this.startSignal}
                  resetSignal={this.resetSignal}
                />
              </Paper>
            </div>
            <div style={container}>
              <Paper elevation={4} style={paperStyle}>
                <h4 style={textStyle}>Caméra monde</h4>
                <div> {this.renderImage(this.state.worldcamfeed)} </div>
              </Paper>
              <Paper elevation={4} style={paperStyle}>
                <h4 style={textStyle}>Caméra embarquée</h4>
                <div> {this.renderImage(this.state.embarkedcamfeed)} </div>
              </Paper>
            </div>
            <div style={container}>
              <Paper elevation={4} style={paperStyle}>
                <h4 style={textStyle}>Trajectoire planifiée & réelle</h4>
                <div> {this.renderImage(this.state.paths)} </div>
              </Paper>
              <Paper elevation={4} style={paperStyle}>
                <h4 style={textStyle}>Caméra embarquée (openCV)</h4>
                <div> {this.renderImage(this.state.embarkedopencv)} </div>
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
  height: 'calc(100% - 64px)',
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'center',
  margin: '0px'
};

const mainPaper = {
  marginLeft: '100px',
  height: 'calc(100% - 34px)',
  width: '50%',
  alignItems: 'center',
  marginRight: '100px',
  marginTop: '10px',
  paddingBottom: '10px'
};

const imageStyle = {
  maxWidth: '215px',
  maxHeight: '215px'
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
