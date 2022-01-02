import React, { useEffect, useState } from 'react';

import { Alert, Button, Form, Modal, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import FormData from 'form-data';

import Sales from './reports/Sales';

function RdyButton(props) {
  return (
      <Button
        id="buildReport"
        variant="warning"
        className="m-3"
        disabled={props.isReady ? false : true }
        onClick={props.download}
      >
        Build report
      </Button>
  );
}

function ReportButton(props) {
  return props.isReady ? <RdyButton {...props} /> : (
    <OverlayTrigger
      placement="right"
      overlay={<Tooltip id="tooltip-disabled">Select dates for build report</Tooltip>}>
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

      this.state = {
        id: props.shopId,
        name: null,

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
          id: resp.data.wb_api_key_id
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
    let dateFrom = this.state.dateFrom;
    let dateTo = this.state.dateTo;
    let brands = [];

    if (dateFrom > dateTo) {
      alert("\"Date From\" may not be lower \"Date To\"");
    }

    await this.props.keyApi.aGetReport(this.state.id, dateFrom, dateTo, brands).then(
      (resp) => {
        console.log(resp);
        this.setState({report: {
          title: dateFrom + "___" + dateTo,
          data: resp.data
        }});
      }
    ).catch(
      (e) => {
        let resp = e.response;
        console.log(resp);
        let data = resp.data;
        console.log(0, resp.status, data, typeof data.detail, typeof data.detail === 'string');
      }
    )
  }

  render() {
    return (
      <>
        <div>
          <h2 className="m-4">{this.state.name}</h2>
          <Button variant="info" className="m-3" onClick={this.rename}>Change shop name</Button>{' '}
          <Button variant="danger" className="m-3" onClick={this.delete}>Delete shop</Button>{' '}
          <div>
            <Form className="d-flex align-items-center">
              <Form.Group className="m-2" controlId="formBasicFrom">
                <Form.Label>Date from</Form.Label>
                <Form.Control name="dateFrom" type="date" onChange={this.handleInputChange} />
              </Form.Group>

              <Form.Group className="m-2" controlId="formBasicTo">
                <Form.Label>Date to</Form.Label>
                <Form.Control name="dateTo" type="date" onChange={this.handleInputChange} />
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
