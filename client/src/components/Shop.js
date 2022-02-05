import React from 'react';

import { Button, Form, OverlayTrigger, Tabs, Tab, Tooltip } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import Multiselect from 'multiselect-react-dropdown';

import Sales from './reports/Sales';

function RdyButton(props) {
  return (
      <Button
        variant="warning"
        className="m-3"
        disabled={props.isReady ? false : true }
        onClick={props.download}
      >
        Построить отчёт
      </Button>
  );
}

function ReportButton(props) {
  return props.isReady ? <RdyButton {...props} /> : (
    <OverlayTrigger
      placement="right"
      overlay={<Tooltip id="tooltip-disabled">Выбрете даты чтобы построить отчёт</Tooltip>}>
      <span className="d-inline-block">
        <RdyButton {...props} />
      </span>
    </OverlayTrigger>
  )
}

function History(props) {
  return props.history && props.history.sale_reports && (
    <div>
      <h5>История запрошенных отчётов:</h5>
      <ul>
        {props.history.sale_reports.length > 0 ? props.history.sale_reports.map((row, ind) => (
          <li
            className="wb-link"
            key={ind}
            onClick={() => props.buildSaleReport(row.date_from, row.date_to, row.brands)}
            >
            {row.date_from} - {row.date_to} [{row.brands.length > 0 ? row.brands.join(' | ') : '...'}]
          </li>
        )) : <li> --- </li>}
      </ul>
    </div>
  )
}


class RealShop extends React.Component {
    constructor(props) {
      super(props);

      let now = new Date();
      now.setDate(0);
      let prevMonthEnd = now.toISOString().split("T")[0];
      now.setDate(1);
      let prevMonthStart = now.toISOString().split("T")[0];

      this.rename = this.rename.bind(this);
      this.delete = this.delete.bind(this);
      this.downloadReport = this.downloadReport.bind(this);
      this.buildReport = this.buildReport.bind(this);
      this.handleInputChange = this.handleInputChange.bind(this);
      this.setBrands = this.setBrands.bind(this);

      this.state = {
        id: props.shopId,
        name: null,
        brands: [],
        selectedBrands: [],

        dateFrom: prevMonthStart,
        dateTo: prevMonthEnd,
        history: {sale_reports: null},
        report: null,
      }
    }

  handleInputChange(e) {
    this.setState({[e.target.name]: e.target.value});
  }

  async componentDidMount() {
    await this.props.keyApi.aGetKey(this.props.shopId).then(
      (resp) => {
        this.setState({
          name: resp.data.name,
          id: resp.data.id,
          brands: resp.data.brands.map(b => ({name: b})),
          history: resp.data.history
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

  async rename() {
    let newName = window.prompt("Введите новое имя магазина");

    if (!newName) {
      alert("Отмена! Имя не может быть пустым.");
      return ;
    }

    await this.props.keyApi.aPatchKey(this.props.shopId, newName).then(
      (resp) => {
        this.setState({
          name: newName
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

  async delete() {
    let result = window.prompt(`Введите имя магазина "${this.state.name}" чтобы удалить`);
    if (result !== this.state.name) {
      alert("Не удалено: введено некорректное имя")
      return ;
    }

    await this.props.keyApi.aDeleteKey(this.props.shopId).then(
      (resp) => {
        this.props.navigate('/shops');
      }
    ).catch(
      (e) => {
        let resp = e.response;
        let data = resp.data;
        console.log(0, resp.status, data, typeof data.detail, typeof data.detail === 'string');
      }
    )
  }

  async downloadReport() {
    let dateFrom = this.state.dateFrom;
    let dateTo = this.state.dateTo;
    let brands = this.state.selectedBrands.map(b => (b.name));

    await this.buildReport(dateFrom, dateTo, brands)
  }

  async buildReport(dateFrom, dateTo, brands) {
    let nowDate = (new Date()).toISOString().split("T")[0];

    if (dateFrom > dateTo) {
      alert("Дата начала не может быть больше Даты окончания");
      return
    } else if (nowDate < dateFrom) {
      alert(`Дата начала не может быть больше сегодняшней (${nowDate})`)
      return
    }

    await this.props.keyApi.aGetReport(this.state.id, dateFrom, dateTo, brands).then(
      (resp) => {
        this.setState({
          history: {sale_reports: resp.data.history},
          dateFrom: dateFrom,
          dateTo: dateTo,
          selectedBrands: brands.map(b => ({name: b})),
          report: {
            dates: {
              min: resp.headers["x-min-created"],
              max: resp.headers["x-max-created"],
            },
            table: {
              title: dateFrom + "___" + dateTo,
              data: resp.data.data
            }
          }
        });
      }
    ).catch(
      (error) => {
        if (error.response) {
          // Request made and server responded
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
        } else if (error.request) {
          // The request was made but no response was received
          console.log(error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log('Error', error.message);
        }
      }
    )
  }

  setBrands(options) {
    this.setState({
      selectedBrands: options
    })
  }

  render() {
    return (
      <Tabs defaultActiveKey="sales-analitics" id="uncontrolled-tab-example" className="my-3">
        <Tab eventKey="sales-analitics" title="Аналитика продаж">
          <h2 className="m-4">{this.state.name}</h2>
          <Button variant="info" className="m-3" onClick={this.rename}>Переименовать</Button>{' '}
          <Button variant="danger" className="m-3" onClick={this.delete}>Удалить магазин</Button>{' '}
          <History history={this.state.history} buildSaleReport={this.buildReport} />
          <div>
            <Form>
              <div className="d-flex align-items-center">
                <Form.Group className="m-2" controlId="formBasicFrom">
                  <Form.Label>С</Form.Label>
                  <Form.Control name="dateFrom" type="date" value={this.state.dateFrom} onChange={this.handleInputChange} />
                </Form.Group>

                <Form.Group className="m-2" controlId="formBasicTo">
                  <Form.Label>По</Form.Label>
                  <Form.Control name="dateTo" type="date" value={this.state.dateTo} onChange={this.handleInputChange} />
                </Form.Group>
              </div>

              <Form.Group className="m-2" controlId="formBasicBrands">
                <Form.Label>Выберите бренды или оставьте пустым для общего отчёта</Form.Label>
                <Multiselect
                  options={this.state.brands}
                  selectedValues={this.state.selectedBrands}
                  showCheckbox="true"
                  showArrow="true"
                  closeOnSelect="true"
                  displayValue="name"
                  onSelect={this.setBrands}
                  onRemove={this.setBrands}
                  />
              </Form.Group>
            </Form>
            <ReportButton isReady={!!this.state.dateFrom && !!this.state.dateTo} download={this.downloadReport} />
          </div>
          {
            !!this.state.report && (
              <div>
                <Sales {...this.state.report} />
              </div>
            )
          }
        </Tab>
        <Tab eventKey="buy-prognosis" title="Прогноз закупок согласно остатков">
          <p>Данный функционал в разработке и будет скоро доступен</p>
        </Tab>
      </Tabs>
    )
  }
}

function Shop(props) {
    let { shopId } = useParams();
    let navigate = useNavigate();
    return <RealShop {...props} shopId={shopId} navigate={navigate} />
}

export default Shop;
