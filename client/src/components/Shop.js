import React, { useEffect, useState } from 'react';

import { Alert, Button, Form, Modal } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import FormData from 'form-data';


class RealShop extends React.Component {
    constructor(props) {
      super(props);

      this.rename = this.rename.bind(this);
      this.delete = this.delete.bind(this);

      this.state = {
        name: null,
        id: props.shopId
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
            <div>
              <Button variant="danger" onClick={this.delete}>Delete</Button>{' '}
            </div>
          </div>
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
