import React from 'react';
import axios from 'axios';
import Layout from './Layout';
import { Card, CardBody, TextContent, Label, Button, FormGroup, TextInput } from '@patternfly/react-core';

class RequestPage extends React.Component {

    state = {
        logged_in: false,
        user: '',
        request: '',
        comments: [],
        reject_reason: '',
        new_comment: ''
    };

    componentDidMount() {

        axios.get('http://ci-backend-new-ci-selfserv.apps.ci.centos.org/user', { withCredentials: true }
        ).then(response => {
            
            if (response.data.message !== 'Please log in to continue.') {
                this.setState({logged_in: true, user: response.data})
            }

            else this.setState({logged_in: false, user: ''});
            
            return response.data
        
        }).then((response) => {
            if (response.message !== 'Please log in to continue.') {
                const url = 'http://ci-backend-new-ci-selfserv.apps.ci.centos.org/requests/'.concat(this.props.match.params.requestid)

                axios.get(url, { withCredentials: true }
                ).then(response => {
                    
                    this.setState({request: response.data.current_request, comments: response.data.comments})
                
                }).catch(err => console.log(err))
            }

            else console.log(response.message)
        
        }).catch(err=>console.log(err))
        
    }

    editRequest = (action) => {

        // var bodyFormData = new FormData();
        // if (action === 'declined' && this.state.user['role'] === 'admin') {
        //     bodyFormData.set('reject_reason', this.state.reject_reason);
        // }

        axios({
            method: 'post',
            url: 'http://ci-backend-new-ci-selfserv.apps.ci.centos.org/edit-request/',
            withCredentials: true,
            params: 
                {
                    'action': action,
                    'request_id': this.props.match.params.requestid,
                    'reject_reason': this.state.reject_reason
                },
            // formData: bodyFormData
            
        }).then(response => {

            const url = 'http://ci-backend-new-ci-selfserv.apps.ci.centos.org/requests/'.concat(this.props.match.params.requestid)

            axios.get(url, { withCredentials: true }
            ).then(response => {
                
                this.setState({request: response.data.current_request, comments: response.data.comments})
            
            }).catch(err => console.log(err))

        }).catch(err => console.log(err))

        if (action === 'approved') {
            this.downloadFile()
        }
    }

    downloadFile = () => {
        
        var FileSaver = require('file-saver');
        var projectIsNew = this.state.request['project_desc'] === '' ? false : true;
        var fileData = {
            'project_name': this.state.request['project_name'],
            'project_description': this.state.request['project_desc'],
            'new_project': projectIsNew,
            'request_id': this.state.request['id'],
            'requested_on': this.state.request['created_at'],
            'last_updated_on': this.state.request['updated_at']
        }
        var blob = new Blob([JSON.stringify(fileData)], {type: 'application/json'});
        var fileName = this.state.request['project_name'].concat('.yaml')
        FileSaver.saveAs(blob, fileName);

    }

    setRejectReason = value => {
        this.setState({reject_reason: value});
    }


    setNewComment = value => {
        this.setState({new_comment: value});
    }


    addComment = () => {

        var bodyFormData = new FormData();
        bodyFormData.set('comment', this.state.new_comment);
        bodyFormData.set('request_id', this.props.match.params.requestid);

        axios({
            method: 'post',
            url: 'http://ci-backend-new-ci-selfserv.apps.ci.centos.org/comment',
            withCredentials: true,
            data: bodyFormData
        
        }).then(response => {

            this.setState({new_comment: ''})
            console.log(response)
            const url = 'http://ci-backend-new-ci-selfserv.apps.ci.centos.org/requests/'.concat(this.props.match.params.requestid)

            axios.get(url, { withCredentials: true }
            ).then(response => {
                
                this.setState({comments: response.data.comments})
            
            }).catch(err => console.log(err))


        }).catch(err => console.log(err))
    
    }


    render() {
        const {request, comments, new_comment, logged_in, user, reject_reason} = this.state;
        return (
            <Layout>
                {!logged_in && <div>Please log in to view this page.</div>}
                {logged_in &&
                <div>

                    {/* Request Label */}
                    <TextContent>
                        {
                            request['project_desc'] !== ''
                            ?
                             <a download href="./logo.png">
                             <Label style={{'background-color':'#C9F8FF', 'margin':'0px 0px 10px 0px', 'padding':'8px'}}>New Project</Label>
                             </a>
                            :
                             <Label style={{'background-color':'#C9F8FF', 'margin':'0px 0px 10px 0px', 'padding':'5px'}}>Member Request</Label>
                        }
                    </TextContent>

                    {/* Request Description Card */}
                    <Card style={{'padding': '0px 0px 30px 30px'}}>
                        <CardBody style={{'margin':'10px'}}><b>Project Name :</b> <div>{request['project_name']}</div></CardBody>
                        {request['project_desc'] !== '' && 
                        <CardBody style={{'margin':'10px'}}><b>Project Description :</b> <div>{request['project_desc']}</div></CardBody>
                        }
                        <CardBody style={{'margin':'10px'}}><b>Requested By :</b> <div>{request['requested_by']}</div></CardBody>
                        <CardBody style={{'margin':'10px'}}><b>Request ID :</b> <div>{request['id']}</div></CardBody>
                        <CardBody style={{'margin':'10px'}}><b>Approval Status :</b> <div>{request['status']}</div></CardBody>
                    </Card>

                    {/* Cancel Request Button for user */}
                    {user['username'] === request['requested_by'] && request['status'] === 'pending' &&
                    <div>
                        <Button
                            style={{'margin':'10px 5px 0px 5px', 'padding':'7px', 'float':'right'}} 
                            onClick={()=>{this.editRequest('declined')}}
                            variant="danger"
                        >
                        Cancel Request
                        </Button>
                        <br/><br/><br/>
                    </div>
                    }
                    
                    {/* Approve or Reject Request */}
                    {user['role'] === 'admin' && request['status'] === 'pending' &&
                    <div>
                    <Button
                        style={{'margin':'20px 5px 20px 5px', 'padding':'8px', 'float':'left'}}
                        onClick={()=>this.editRequest('approved')}
                    >
                    Approve Request
                    </Button>
                    <br/><br/>
                    <FormGroup helperText="Please provide a reason to reject this project">
                        <TextInput
                            value={reject_reason}
                            onChange={this.setRejectReason}
                            type="text"
                        />
                        <Button
                            style={{'margin':'10px 5px 10px 5px', 'padding':'7px', 'float':'right'}} 
                            onClick={()=>this.editRequest('declined')}
                            variant="danger"
                            isDisabled={reject_reason === '' ? true : false}
                        >
                        Reject Request
                        </Button>
                    </FormGroup>
                    </div>
                    }

                    {/* Download YAML button */}
                    {user['role'] === 'admin' && request['status'] === 'approved' &&
                    <div>
                    <Button
                        style={{'margin':'20px 5px 20px 5px', 'padding':'8px', 'float':'left'}}
                        onClick={this.downloadFile}
                        variant="primary"
                    >
                    Download File
                    </Button>
                    <br/>
                    </div>
                    }

                    {/* Comments Card */}
                    <Card style={{'padding': '0px 30px 20px 30px', 'margin-top':'60px'}}>
                        {comments.length < 1 
                            ? <CardBody>Looks like there are no comments for this request! <br/><br/></CardBody>
                            :   comments.map(comment => {
                                return <div>
                                        <Label style={{'background-color':'#C9F8FF', 'margin':'10px 10px 10px 0px', 'padding':'5px'}}>{comment['commented_by']} -</Label>
                                        <Label>{comment['comment']}</Label>
                                    </div>
                                })
                        }

                        <FormGroup>
                        <TextInput
                            value={new_comment}
                            onChange={this.setNewComment}
                            type="text"
                        />
                        <Button
                            style={{'float':'right', 'padding':'5px', 'margin':'5px 0px 5px 0px'}}
                            isDisabled={new_comment === '' ? true : false}
                            variant="secondary"
                            onClick={this.addComment}
                        >
                        Add Comment
                        </Button>
                        </FormGroup>
                    </Card>
                    
                </div>
                }
            </Layout>
        )
    }
}

export default RequestPage