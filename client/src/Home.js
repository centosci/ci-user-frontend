import React from 'react';
import {  TextContent, Text } from '@patternfly/react-core';
import largeLogo from './centos-logo-png-transparent.png';
import Layout from './Layout';

function Home () {
    return (
      <Layout>
      <div style={{'height':'100%'}}>
        <TextContent style={{'margin-left':'40px', 'margin-top':'20px'}}>
        <Text component="h1" style={{'font-size':'35px'}}>Welcome to CentOS CI</Text>
        <Text component="p">
        <div>
            <h3>To onboard a Project, please log in with your ACO account or 
              <u><a target="_blank"href="https://accounts.centos.org/user/new"> Sign up </a></u> for one!
            </h3>
        </div>
        </Text>
      </TextContent>
      <img src={largeLogo} style={{'padding': '25px 25px 25px 0px'}}/>
      </div>
      </Layout>
    )
}

export default Home