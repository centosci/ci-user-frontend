import React from 'react';
import axios from 'axios';

class Requests extends React.Component {

    componentDidMount() {

        const login_params = window.location.search
        // const new_login_params = login_params.replace('openid.return_to=http://localhost:3000/logging_in/', 'openid.return_to=http://localhost:5000/_flask_fas_openid_handler/')
        const login_handler = 'http://localhost:5000/_flask_fas_openid_handler/'
        // var login_url = login_handler.concat(new_login_params)
        var login_url = login_handler.concat(login_params)
        console.log(login_url)
        axios.get(login_url
        ).then(res=> {console.log(res)}
        ).catch(err=>console.log(err))
    }
    render() {
        return (
            <div>LOGGING IN</div>
        )
    }
}

export default Requests