import React from 'react';
import axios from 'axios';

class App extends React.Component {

    componentDidMount() {
        var data = document.location.search.substring(1)
        axios({
            method: 'post',
            url: 'http://ci-backend-ci-selfserv.apps.ci.centos.org'.concat('/_flask_fas_openid_handler/'),
            withCredentials: true,
            data: data
            })
            .then(response => {
                console.log(response.data)
                window.location.href = response.data.redirect_url
            })
            .catch(response => {
                console.log(response.status)
                console.log(response.data)
            });
    }

    render() {
        return (
        <div style={{'text-align':'center', 'padding':'70px'}}>Loading..</div>
        )
    }
}

export default App;
