import React, { Component } from 'react';
import logo from './logo.png';
import './App.css';

import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Paper from '@material-ui/core/Paper';

import openSocket from 'socket.io-client';

import Timer from './Timer';

class App extends Component {
  state = { 
    main: "",
    img: "",
    socket: openSocket('http://localhost:4000?token=UI')
  }

  componentDidMount() {
    this.state.socket.on('event', resp => {
      console.log(resp);
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

  render() {
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
          <div style={{...container, ...morePadding}}>
              <Paper elevation={4} style={paperStyle}>
                  <h4 style={textZone}>Informations QR</h4>
                  <p>{this.state.qrcode}</p>
                  <div> {this.renderImage(this.state.actualimg)} </div>
              </Paper>
              <Paper elevation={4} style={paperStyle}>
                  <Timer startSignal={this.startSignal} resetSignal={this.resetSignal}/>
              </Paper>
          </div>
          <div style={container}>
              <Paper elevation={4} style={paperStyle}>
                  <span style={textZone}>Courant et</span>
                  <span style={textZone}>tension condensateur</span>
              </Paper>
              <Paper elevation={4} style={paperStyle}>
                  <span style={textZone}>États présent du robot</span>
                  <span style={textZone}>{this.state.phase}</span>
              </Paper>
          </div>
          <div style={container}>
              <Paper elevation={4} style={paperStyle}>
                  <h4>Trajectoire planifiée</h4>
                  <div> {this.renderImage(this.state.optpath)} </div>
              </Paper>
              <Paper elevation={4} style={paperStyle}>
                  <h4>Trajectoire réelle</h4>
                  <div> {this.renderImage(this.state.actualpath)} </div>
              </Paper>
          </div>
          </Paper>
          </div>
      </div>
    );
  }
}

const paperStyle = {
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

const morePadding = {
  padding: '10px'
};

const textZone = {
  margin: '10px 50px 10px 50px'
};

const imageStyle = {
  maxWidth: '300px',
  maxHeight: '300px'
};

export default App;
