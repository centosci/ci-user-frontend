import React from 'react';
import axios from 'axios';
import Layout from './Layout';
import { Link } from 'react-router-dom';
import {
    Table,
    TableHeader,
    TableBody,
    TableVariant,
} from '@patternfly/react-table';

class Requests extends React.Component {

    state = {
        logged_in: false,
        requests: []
    }

    componentDidMount() {
        axios.get('http://localhost:5000/requests', { withCredentials: true }
        ).then(res=> {
            if (res.data.message !== 'Please log in to continue.') {
                this.setState({logged_in: true, requests: res.data.requests})
            }
        }).catch(err=>console.log(err))
    }
    render() {
        const {logged_in, requests} = this.state;
        if (requests.length >= 1) {

            var columns = ['Project Name', 'Requested By', 'Approval Status', 'Request ID', 'More Details']

            var rows = [];

            requests.map(req => {
                var row = []
                row.push(req['project_name'])
                row.push(req['requested_by'])
                row.push(req['status'])
                row.push(req['id'])
                const request_url = '/requests/'.concat(req['id'])
                const request_link = { title: <Link to={request_url}>->></Link> }
                row.push(request_link)
                rows.push(row)
                return row
            })
        }

        return (
            <Layout activeItem={2}>
            <div>
            {!logged_in && <div>Please log in to view this page.</div>}
            {logged_in &&
            <div>
                {requests.length < 1 && <div>No Requests Found </div> }
                {requests.length >= 1 && 
                    <div>
                        <div style={{'font-size':'35px'}}>Project Requests</div>
                        <Table variant={TableVariant.compact} cells={columns} rows={rows}>
                            <TableHeader />
                            <TableBody />
                        </Table>
                    </div>
                }
            </div>
            }
            </div>
            </Layout>
        )
    }
}

export default Requests