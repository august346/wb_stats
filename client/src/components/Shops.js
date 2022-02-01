import React from 'react';

import { ListGroup, Tabs, Tab } from 'react-bootstrap';
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
      <Tabs defaultActiveKey="wb" id="uncontrolled-tab-example" className="my-3">
        <Tab eventKey="wb" title="Wildberries">
          <h2>Мои магазины</h2>
          <br />
          <div className="d-flex justify-content-between">
            <p>Здесь можно провести аналитику продаж и прогнозы закупок по отсаткам</p>
            <a className="ml-5" href="/files/api_key_instructions" download="123.txt">
              Как подключить API ключ?
            </a>
          </div>
          <br />
          <NewShop create={this.props.shopApi.aCreateKey} />
          <br />
          <br />
          {apiKeysGroup}
        </Tab>
        <Tab eventKey="ozon" title="OZON">
          <p>Данный функционал в разработке</p>
        </Tab>
        <Tab eventKey="all" title="Общая аналитика по всем магазинам">
          <p>Страница в разработке, здесь можно видеть продажи по всем магазинам</p>
        </Tab>
      </Tabs>
    )
  }
}

export default Shops;
