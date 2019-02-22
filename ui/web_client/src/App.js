import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import Button from '@material-ui/core/Button';
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Paper from '@material-ui/core/Paper';

import openSocket from 'socket.io-client';

class App extends Component {
  state = { 
    main: "",
    img: "",
    socket: openSocket('http://localhost:4000?token=UI')
  }

  componentDidMount() {
    this.state.socket.on('event', resp => {
      this.setState({ [resp.dest]: resp.data });
    });
  }
  
  startSignal = () => {
    this.state.socket.emit("start", "start");
  }

  render() {
    let imgR = "data:image/png;base64, " + this.state.img;
    if (this.state.img === "") {
      imgR = logo;
    }

    return (
      <div className="App">
          <AppBar position="static" color="primary">
              <Toolbar>
                  <Typography variant="h6" color="inherit">
                      Station de base
                  </Typography>
              </Toolbar>
          </AppBar>
          <div style={mainPaper}>
          <Paper elevation={15}>
          <div style={mainDock}>
              <Paper elevation={4}>
                  <span style={textZone}>Info Code QR</span>
                  <Button variant="contained" color="primary" style={buttonStyle} onClick={this.startSignal}>
                      Start
                  </Button>
                  <span style={textZone}>Chronographe</span>
              </Paper>
          </div>
          <div style={container}>
              <Paper elevation={4} style={imageStyle}>
                  <span style={textZone}>Courant et</span>
                  <span style={textZone}>tension condensateur</span>
              </Paper>
              <Paper elevation={4} style={imageStyle}>
                  <span style={textZone}>États présent du robot</span>
              </Paper>
          </div>
          <div style={container}>
              <Paper elevation={4} style={imageStyle}>
                  <img src={imgR} width="200" alt="logo"/>
              </Paper>
              <Paper elevation={4} style={imageStyle}>
                  <img src={imgR} width="200" alt="logo"/>
              </Paper>
          </div>
          </Paper>
          </div>
      </div>
    );
  }
}

const imageStyle = {
  display: 'flex',
  flexDirection: 'column',
  margin: '10px',
  padding: '10px'
};

const container = {
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'center'
};

const mainPaper = {
  marginLeft: '100px',
  marginRight: '100px',
  marginTop: '10px',
};

const mainDock = {
  display: 'flex',
  justifyContent: 'center',
  padding: '10px'
};

const buttonStyle = {
  margin: '10px'
};

const textZone = {
  margin: '10px 50px 10px 50px'
};

export default App;
