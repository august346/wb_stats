import React from 'react';

import { Alert, Button, Form, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import FormData from 'form-data';

import API from "../utils/API";


async function signIn(email, password) {
  const form = new FormData();
  form.append("username", email);
  form.append("password", password);

  return API.post('/auth/token', form);
}

class SignInWithoutNavigate extends React.Component {
  constructor(props) {
    super(props);

    this.handleClose = this.handleClose.bind(this);
    this.handleShow = this.handleShow.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.onClick = this.onClick.bind(this);

    this.state = {
      show: false,

      email: null,
      password: null,

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

  async onClick() {
    await signIn(
      this.state.email,
      this.state.password
    ).then(
      (resp) => {
        this.handleClose();
        this.props.onAuth(resp.data, true);
        this.props.navigate('/shops');
      }
    ).catch(
      (err) => {
        let resp = err.response;
        let data = resp.data;
        if (resp.status === 401) {
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
    if (this.state.email && !this.state.email.match(/^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[A-Za-z]+$/)) {
      errors.email = "Невалидный email";
    }

    return (
      <>
        <Button variant="outline-primary" className="btn ml-auto" onClick={this.handleShow}>
          Логин
        </Button>

        <Modal show={this.state.show} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Логин</Modal.Title>
          </Modal.Header>
          <Modal.Body>
          <Form>
            {!!errors.general && (
              <Alert variant="danger">
                {errors.general}
              </Alert>
            )}
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email</Form.Label>
              <Form.Control name="email" type="email" required placeholder="Enter email" onChange={this.handleInputChange} isInvalid={!!errors.email} />
              <Form.Control.Feedback type="invalid">
                {errors.email}
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Пароль</Form.Label>
              <Form.Control name="password" type="password" required placeholder="Password" onChange={this.handleInputChange} />
            </Form.Group>
          </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button className="mx-auto" type="submit" variant="outline-primary" onClick={this.onClick}>
              Логин
            </Button>
          </Modal.Footer>
        </Modal>
      </>
    );
  }
}

function SignIn(props) {
    let navigate = useNavigate();
    return <SignInWithoutNavigate {...props} navigate={navigate} />
}

export default SignIn;
