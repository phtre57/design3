import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import openSocket from 'socket.io-client';

class App extends Component {
  state = { main: "", img: "", socket: openSocket('http://localhost:4000?token=UI')}

  componentDidMount() {
    this.state.socket.on('event', data => {
      this.setState({ [data.type]: data.data });
    });
  }
  
  alloSocket = () => {
    this.state.socket.emit("event", "ok");
  }

  render() {
    let imgR = "data:image/png;base64, " + this.state.img 
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> {this.state.main} and save to reload.
          </p>
          
          <button onClick={this.alloSocket}>ALLO</button>
          <img src={imgR} alt="flip flip ok"/>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    );
  }
}

export default App;
