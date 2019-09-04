import React from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import Requests from './Requests';
import Projects from './Projects';
import Home from './Home';
import RequestForm from './RequestForm';
import RequestPage from './RequestPage';
import Login from './Login';
import Layout from './Layout';

class App extends React.Component {

  render() {
    return (
      <Router>
          <Route path="/" exact render={ (props) => <Layout {...props} child={<Home/>}/> } />
          <Route path="/requests" exact render={ (props) => <Layout {...props} child={<Requests/>}/> } />
          <Route path="/projects" exact render={ (props) => <Layout {...props} child={<Projects/>}/> } />
          <Route path="/new-request" exact render={ (props) => <Layout {...props} child={<RequestForm/>}/> } />
          <Route path="/requests/:requestid" render={ (props) => <Layout {...props} child={<RequestPage/>}/> } />
          <Route path="/_flask_fas_openid_handler/" render={ (props) => <Layout {...props} child={<Login/>}/> } />
      </Router>
    )
  }
}

export default App;
