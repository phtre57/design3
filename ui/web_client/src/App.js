import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

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
  
  alloSocket = () => {
    this.state.socket.emit("event", "ok");
  }

  render() {
    let imgR = "data:image/png;base64, " + this.state.img;
    if (this.state.img === "") {
      imgR = logo;
    }

    return (
      <div className="App">
        <header className="App-header">
          <button onClick={this.alloSocket}>ALLO</button>
          <img src={imgR} width="200" alt="logo"/>
        </header>
      </div>
    );
  }
}

export default App;
