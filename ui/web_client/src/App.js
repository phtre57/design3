import React, { Component } from 'react';
import logo from './logo.png';
import './App.css';

import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Paper from '@material-ui/core/Paper';
import MenuIcon from '@material-ui/icons/Menu';
import IconButton from '@material-ui/core/IconButton';

import openSocket from 'socket.io-client';

import Timer from './Timer';
import LogPanel from './LogPanel';

class App extends Component {
  state = { 
    main: "",
    img: "",
    showLogs: true,
    socket: openSocket('http://localhost:4000?token=UI')
  }

  componentDidMount() {
    this.state.socket.on('event', resp => {
      this.setState({ [resp.dest]: resp.data });
    });
  }
  
  startSignal = () => {
    this.state.socket.emit("start", "start");
    console.log("start signal sent");
  }

  resetSignal = () => {
    console.log("reset signal sent");
  }

  renderImage = (image) => {
    let imgR = "data:image/png;base64, " + image;
    if (image === undefined) {
      return <img src={logo} width={30} alt="logo"/>;
    }

    return <img src={imgR} style={imageStyle} alt="logo"/>;
  }

  openLogPanel = () => {
    document.getElementById('log-panel').style.display = "block";
    document.getElementsByClassName('main-container')[0].style.justifyContent = "space-between";
  }

  closeLogPanel = () => {
    document.getElementById('log-panel').style.display = "none";
    document.getElementsByClassName('main-container')[0].style.justifyContent = "center";
  }

  toggleLogPanel = () => {
    this.state.showLogs ? this.openLogPanel() : this.closeLogPanel();
    this.setState({showLogs: !this.state.showLogs});
  }

  render() {
    return (
      <div style={app}>
          <AppBar position="static" color="primary">
              <Toolbar style={toolbar}>
                  <Typography variant="h6" color="inherit">
                      Station de base
                  </Typography>
                  <IconButton color="inherit">
                  <MenuIcon onClick={this.toggleLogPanel}/>
                  </IconButton>
              </Toolbar>
          </AppBar>

          <div className='main-container' id="main-container" style={mainContainer}>
            <Paper elevation={15} style={mainPaper}>
            <div style={container}>
                <Paper elevation={4} style={paperStyle}>
                    <h4 style={textZone}>Informations QR</h4>
                    <p>{this.state.qrcode}</p>
                </Paper>
                <Paper elevation={4} style={paperStyle}>
                    <Timer startSignal={this.startSignal} resetSignal={this.resetSignal}/>
                </Paper>
            </div>
            <div style={container}>
                <Paper elevation={4} style={paperStyle}>
                    <h4 style={textZone}>Tension Condensateur</h4>
                </Paper>
                <Paper elevation={4} style={paperStyle}>
                    <h4 style={textZone}>Statut Robot</h4>
                     {/* Waiting for start signnal... */}
                    <span style={textZone}>{this.state.phase}</span>
                </Paper>
            </div>
            <div style={container}>
                <Paper elevation={4} style={paperStyle}>
                    <h4>Trajectoire planifiée & réelle</h4>
                    <div> {this.renderImage(this.state.optpath)} </div>
                </Paper>
                <Paper elevation={4} style={paperStyle}>
                    <h4>Caméra embarquée</h4>
                    <div> {this.renderImage(this.state.actualimg)} </div>
                </Paper>
            </div>
            </Paper>
            <LogPanel socket={this.state.socket}/>
          </div>
      </div>
    );
  }
}

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
  margin: '0px',
};

const mainContainer = {
  height: 'calc(100% - 64px)',
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'center',
  margin: '0px',
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

const textZone = {
  margin: '10px 50px 10px 50px'
};

const imageStyle = {
  maxWidth: '300px',
  maxHeight: '300px'
};

const toolbar = {
  alignItems: 'center',
  justifyContent: 'space-between',
};

export default App;
