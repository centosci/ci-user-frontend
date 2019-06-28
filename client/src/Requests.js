import React from 'react';
import axios from 'axios'

class Requests extends React.Component {

    componentDidMount() {
        axios.get('http://localhost:5000/requests'
        ).then(res=> {console.log(res)}
        ).catch(err=>console.log(err))
    }
    render() {
        return (
            <div>REQUESTS</div>
        )
    }
}

export default Requests