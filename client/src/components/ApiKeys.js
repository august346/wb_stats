import React from 'react';

import { Button, ListGroup } from 'react-bootstrap';


function ApiKeyPage(props) {
  return (
    <li className="col-xs-2 col-sm-5 d-flex m-1">
      <Button variant="outline-success">{props.info.name}</Button>{' '}
      <Button variant="primary" className="ml-auto">✎</Button>{' '}
      <Button variant="danger" className="ml-2">✕</Button>{' '}
    </li>
  );
}


class ApiKeys extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      apiKeys: []
    }
  }

  async componentDidMount() {
    await this.props.getter().then(
      (resp) => {
        this.setState({
          apiKeys: resp.data
        })
      }
    ).catch(
      (e) => {
        let resp = e.response;
        let data = resp.data;
        console.log(0, resp.status, data, typeof data.detail, typeof data.detail === 'string');
      }
    )
  }

  render() {
    const apiKeysList = this.state.apiKeys.map((info) =>
      <ListGroup.Item key={info.wb_api_key_id} info={info}><a href="#">{info.name}</a></ListGroup.Item>
    )

    return (
      <div>
        <h2>My Shops</h2>
        <br />
        <Button variant="success" className="m-auto">Add new</Button>{' '}
        <br />
        <br />
        <ListGroup>{apiKeysList}</ListGroup>
      </div>
    )
  }
}

export default ApiKeys;
