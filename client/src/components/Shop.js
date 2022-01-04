import React from 'react';

import { Button, Form, OverlayTrigger, Tooltip } from 'react-bootstrap';
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


class RealShop extends React.Component {
    constructor(props) {
      super(props);

      this.rename = this.rename.bind(this);
      this.delete = this.delete.bind(this);
      this.downloadReport = this.downloadReport.bind(this);
      this.handleInputChange = this.handleInputChange.bind(this);
      this.setBrands = this.setBrands.bind(this);

      this.state = {
        id: props.shopId,
        name: null,
        brands: [],
        selectedBrands: [],

        dateFrom: null,
        dateTo: null,
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
          brands: resp.data.brands.map(b => ({name: b}))
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
    let newName = window.prompt("Enter new shop name");

    if (!newName) {
      alert("Name may not be empty!\nAborted");
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
    let result = window.prompt(`Enter shop name "${this.state.name}" to delete?`);
    if (result !== this.state.name) {
      alert("Not deleted: incorrect name entered")
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
    let nowDate = (new Date()).toISOString().split("T")[0];
    let dateFrom = this.state.dateFrom;
    let dateTo = this.state.dateTo;
    let brands = this.state.selectedBrands.map(b => (b.name));

    if (dateFrom > dateTo) {
      alert("\"Date From\" may not be lower \"Date To\"");
      return
    } else if (nowDate < dateFrom) {
      alert(`"Date From" may not be lower now (${nowDate})`)
      return
    }


    await this.props.keyApi.aGetReport(this.state.id, dateFrom, dateTo, brands).then(
      (resp) => {
        this.setState({report: {
          dates: {
            min: resp.headers["x-min-created"],
            max: resp.headers["x-max-created"],
          },
          table: {
            title: dateFrom + "___" + dateTo,
            data: resp.data
          }
        }});
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
      <>
        <div>
          <h2 className="m-4">{this.state.name}</h2>
          <Button variant="info" className="m-3" onClick={this.rename}>Переименовать</Button>{' '}
          <Button variant="danger" className="m-3" onClick={this.delete}>Удалить магазин</Button>{' '}
          <div>
            <Form>
              <div className="d-flex align-items-center">
                <Form.Group className="m-2" controlId="formBasicFrom">
                  <Form.Label>С</Form.Label>
                  <Form.Control name="dateFrom" type="date" onChange={this.handleInputChange} />
                </Form.Group>

                <Form.Group className="m-2" controlId="formBasicTo">
                  <Form.Label>По</Form.Label>
                  <Form.Control name="dateTo" type="date" onChange={this.handleInputChange} />
                </Form.Group>
              </div>

              <Form.Group className="m-2" controlId="formBasicBrands">
                <Form.Label>Select brands for separated sums (multi)</Form.Label>
                <Multiselect
                  options={this.state.brands}
                  selectedValues={this.state.selectedBrands}
                  showCheckbox="true"
                  showArrow="true"
                  closeOnSelect="false"
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
        </div>
      </>
    )
  }
}

function Shop(props) {
    let { shopId } = useParams();
    let navigate = useNavigate();
    return <RealShop {...props} shopId={shopId} navigate={navigate} />
}

export default Shop;
