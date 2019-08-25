import React from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import Requests from './Requests';
import Projects from './Projects';
import Home from './Home';
import RequestForm from './RequestForm';
import RequestPage from './RequestPage';
import Login from './Login';

class App extends React.Component {

  render() {
    return (

      <Router>
          <Route path="/" exact component={Home}/>
          <Route path="/requests" exact component={Requests} />
          <Route path="/projects" component={Projects} />
          <Route path="/new-request" exact component={RequestForm} />
          <Route path="/requests/:requestid" component={RequestPage} />
          <Route path="/_flask_fas_openid_handler/" component={Login} />
      </Router>

    )
  }
}

export default App;
