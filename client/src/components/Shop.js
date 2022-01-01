import React, { useEffect, useState } from 'react';

import { Alert, Button, Form, Modal } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import FormData from 'form-data';

import Sales from './reports/Sales';


class RealShop extends React.Component {
    constructor(props) {
      super(props);

      this.rename = this.rename.bind(this);
      this.delete = this.delete.bind(this);
      this.downloadReport = this.downloadReport.bind(this);

      this.state = {
        name: null,
        id: props.shopId,
        report: null,
      }
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
    let result = window.confirm(`Are you sure you want to delete "${this.state.name}" Store?`);
    if (!result) {
      return
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
    let dateFrom = "2021-11-01";
    let dateTo = "2021-12-01";
    let brands = [];

    await this.props.keyApi.aGetReport(this.state.id, dateFrom, dateTo, brands).then(
      (resp) => {
        this.setState({report: {
          title: dateFrom + "___" + dateTo,
          data: resp.data
        }});
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
      <>
        <div>
          <h2 className="m-4">Shop</h2>
          <div>
            <p>
              <b>Name:</b> <i>{this.state.name}</i>
              <Button variant="info" className="m-3" onClick={this.rename}>&#9998;</Button>{' '}
            </p>
            <Form className="d-flex align-items-center">
              <Form.Group className="m-2" controlId="formBasicFrom">
                <Form.Label>Date from</Form.Label>
                <Form.Control name="dateFrom" type="date" />
              </Form.Group>

              <Form.Group className="m-2" controlId="formBasicTo">
                <Form.Label>Date to</Form.Label>
                <Form.Control name="dateTo" type="date" />
              </Form.Group>
            </Form>
            <Button variant="warning" className="m-3" onClick={this.downloadReport}>Build report</Button>{' '}
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
