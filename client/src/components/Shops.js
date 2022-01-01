import React from 'react';

import { Button, ListGroup } from 'react-bootstrap';
import { Link } from 'react-router-dom';


function ApiKey(info) {
  return (
    <ListGroup.Item
      as={Link}
      key={info.wb_api_key_id}
      to={`/shops/${info.wb_api_key_id}`}
    >
      {info.name}
    </ListGroup.Item>
  );
}


class Shops extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      apiKeys: []
    }
  }

  async componentDidMount() {
    await this.props.getKeys().then(
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
    return (
      <div>
        <h2>My Shops</h2>
        <br />
        <Button variant="success" className="m-auto">Add</Button>{' '}
        <br />
        <br />
        <ListGroup>{this.state.apiKeys.map(ApiKey)}</ListGroup>
      </div>
    )
  }
}

export default Shops;
