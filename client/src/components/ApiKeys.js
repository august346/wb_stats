import React from 'react';

import { Button, ListGroup } from 'react-bootstrap';

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
        <h2>Мои магазины</h2>
        <br />
        <Button variant="success" className="m-auto">Добавить</Button>{' '}
        <br />
        <br />
        <ListGroup>{apiKeysList}</ListGroup>
      </div>
    )
  }
}

export default ApiKeys;
