import React from 'react';

import { Alert, Button, Form, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';


class RealNewShop extends React.Component {
  constructor(props) {
    super(props);

    this.handleClose = this.handleClose.bind(this);
    this.handleShow = this.handleShow.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.create = this.create.bind(this);

    this.state = {
      show: false,

      key: null,
      name: null,

      error: null,
    }
  }

  handleClose() {
    this.setState({show: false});
  }

  handleShow() {
    this.setState({show: true, error: null});
  }

  handleInputChange(e) {
    this.setState({[e.target.name]: e.target.value});
  }

  async create() {
    await this.props.create(
      this.state.key.toString(),
      this.state.name.toString()
    ).then(
      (resp) => {
        this.handleClose();
        window.location.reload();
      }
    ).catch(
      (err) => {
        let resp = err.response;
        let data = resp.data;
        if (resp.status === 400) {
          if (typeof data.detail === 'string') {
            this.setState({error: data.detail})
          } else {
            console.log(0, resp.status, data, typeof data.detail, typeof data.detail === 'string');
          }
        } else {
          console.log(0, resp.status, data, typeof data.detail, typeof data.detail === 'string');
        }
        return
      }
    )
  }

  render() {
    let errors = {};
    if (!!this.state.error) {
      errors.general = this.state.error;
    }

    return (
      <>
        <Button variant="success" className="btn ml-auto" onClick={this.handleShow}>
          Создать
        </Button>

        <Modal show={this.state.show} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Создать</Modal.Title>
          </Modal.Header>
          <Modal.Body>
          <Form>
            {!!errors.general && (
              <Alert variant="danger">
                {errors.general}
              </Alert>
            )}
            <Form.Group className="mb-3" controlId="formBasicKey">
              <Form.Label>WB API KEY</Form.Label>
              <Form.Control name="key" required placeholder="Enter WB API key" onChange={this.handleInputChange} />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicName">
              <Form.Label>Название магазина</Form.Label>
              <Form.Control name="name" required placeholder="Enter Shop name" onChange={this.handleInputChange} />
            </Form.Group>
          </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button className="mx-auto" type="submit" variant="outline-primary" onClick={this.create}>
              Создать
            </Button>
          </Modal.Footer>
        </Modal>
      </>
    );
  }
}

function NewShop(props) {
    let navigate = useNavigate();
    return <RealNewShop {...props} navigate={navigate} />
}

export default NewShop;
