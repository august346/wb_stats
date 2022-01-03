import React from 'react';

import { ListGroup } from 'react-bootstrap';
import { Link } from 'react-router-dom';

import NewShop from './NewShop';


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
    await this.props.shopApi.aGetKeys().then(
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
    let apiKeysGroup = this.state.apiKeys.length > 0 ? (
      <ListGroup>{this.state.apiKeys.map(ApiKey)}</ListGroup>
    ) : (
      <pre>Нет магазинов</pre>
    )

    return (
      <div>
        <h2>Мои магазины</h2>
        <br />
        <NewShop create={this.props.shopApi.aCreateKey} />
        <br />
        <br />
        {apiKeysGroup}
      </div>
    )
  }
}

export default Shops;
