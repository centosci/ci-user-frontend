import React from 'react';
import axios from 'axios';
import {
    Table,
    TableHeader,
    TableBody,
    TableVariant,
} from '@patternfly/react-table';

class Projects extends React.Component {
    
    state = {
        projects: [],
    }

    componentDidMount() {
        axios.get('http://ci-backend-ci-selfserv.apps.ci.centos.org'.concat('/projects'), { withCredentials: true }
        ).then(res=> {
            this.setState({projects: res.data.projects})
        }).catch(err=>console.log(err))
    }
    render() {
        const {projects} = this.state;

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
                project['members'].map((member, index) => {
                    members = members.concat(member, ', ')
                    return member
                })
                row.push(members)

                const project_url = '/projects/'.concat(project['id'])
                const project_page_link = { title: <a href={window.location.href}>Go to Project</a> }
                row.push(project_page_link)

                rows.push(row)

                return row
            })
        }

        return (
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
        )
    }

}

export default Projects