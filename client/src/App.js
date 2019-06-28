import React from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Requests from './Requests';
import Projects from './Projects';
import Home from './Home';
import LogIn from './LogIn';
import axios from 'axios';

class App extends React.Component {

  state = {
    user: '',
  }

  login = () => {
    var self = this;
    axios.get('http://localhost:5000/login').then(response => {
      window.location.replace(response.data)
    })
  }

  render() {
    return (
    <div>

      <Router>
          <nav>
            <Link to="/"><h3 style={{display:"inline"}}>Home</h3></Link>
            <button onClick={this.login} style={{display:"inline", margin:"10px"}}>LOGIN</button>

            <ul>
              <li>
                <Link to="/requests/">Requests</Link>
              </li>
              <li>
                <Link to="/projects/">Projects</Link>
              </li>
            </ul>
          </nav>
          <Route path="/" exact component={Home} />
          <Route path="/logging_in/" component={LogIn} />
          <Route path="/requests/" component={Requests} />
          <Route path="/projects/" component={Projects} />
      </Router>

    </div>
    )
  }
}

export default App;
