import React from 'react';
import axios from 'axios';
import {
    Table,
    TableHeader,
    TableBody,
    TableVariant,
} from '@patternfly/react-table';
import Layout from './Layout';

class Projects extends React.Component {
    
    state = {
        logged_in : false,
        projects: [],
    }

    componentDidMount() {
        axios.get('http://localhost:5000/projects', { withCredentials: true }
        ).then(res=> {
            if (res.data.message !== 'Please log in to continue.') {
                this.setState({logged_in: true, projects: res.data.projects})
            }
        }).catch(err=>console.log(err))
    }
    render() {
        const {logged_in, projects} = this.state;
        if (projects.length >= 1) {

            var columns = ['Project Name', 'Description', 'Created On', 'Build Status', 'Members', 'Project Link']

            var rows = [];

            projects.map(project => {
                var row = []
                row.push(project['project_name'])
                row.push(project['description'])
                row.push(project['created_at'])
                row.push('-')
                var members = ''
                project['members'].map((member, index) => { members = members.concat(member, ', ')})
                row.push(members)
                const project_url = '/projects/'.concat(project['id'])
                const project_page_link = { title: <a href={"http://localhost:3000/"}>Go to Project</a> }
                row.push(project_page_link)
                rows.push(row)
                return row
            })
        }

        return (
            <Layout activeItem={0}>
            <div>
            {!logged_in && <div>Please log in to view this page.</div>}
            {logged_in &&
            <div>
                {projects.length < 1 && <div>No Projects Found </div> }
                {projects.length >= 1 && 
                    <div>
                        <div style={{'font-size':'35px'}}>Projects</div>
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

export default Projects