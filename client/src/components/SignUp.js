import React from 'react';

import { Alert, Button, Form, Modal } from 'react-bootstrap';

import API from "../utils/API";


async function signUp(email, password, password_confirm) {
  if (password !== password_confirm) {
    alert("not equal passwords");
    return ;
  }

  return API.post('/auth/signup', {
    email: email,
    password: password,
  })
}


class SignUp extends React.Component {
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
      password_confirm: null,

      error: null,
    }
  }

  handleClose() {
    this.setState({show: false});
  }

  handleShow() {
    this.setState({show: true});
  }

  handleInputChange(e) {
    this.setState({[e.target.name]: e.target.value});
  }

  async onClick(e) {
    await signUp(
      this.state.email,
      this.state.password,
      this.state.password_confirm,
    ).then(
      (data) => {
        this.handleClose();
        alert("Success. Wait email activation confirm in few hours.")
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
    if (!this.state.email) {
      errors.email = "May not be empty"
    } else if (!this.state.email.match(/^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[A-Za-z]+$/)) {
      errors.email = "Not valid email"
    }
    if (!this.state.password) {
      errors.password = "May not be empty"
    } else if (!this.state.password.match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/)) {
      errors.password = "Not secure"
    }
    if (this.state.password !== this.state.password_confirm) {
      errors.password_confirm = "Not equal with first password"
    }

    return (
      <>
        <Button variant="primary" className="mx-2" onClick={this.handleShow}>
          SignUp
        </Button>

        <Modal show={this.state.show} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Registration</Modal.Title>
          </Modal.Header>
          <Modal.Body>
          <Form>
            {!!errors.general && (
              <Alert variant="danger">
                {errors.general}
              </Alert>
            )}
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control name="email" type="email" required placeholder="Enter email" onChange={this.handleInputChange} isInvalid={!!errors.email} />
              <Form.Text className="text-muted">
                We'll never share your email with anyone else.
              </Form.Text>
              <Form.Control.Feedback type="invalid">
                {errors.email}
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control name="password" type="password" required placeholder="Password" onChange={this.handleInputChange} isInvalid={!!errors.password} />
              <Form.Control.Feedback type="invalid">
                {errors.password}
              </Form.Control.Feedback>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword2">
              <Form.Label>Confirm Password</Form.Label>
              <Form.Control name="password_confirm" type="password" placeholder="Password" onChange={this.handleInputChange} isInvalid={!!errors.password_confirm} />
              <Form.Control.Feedback type="invalid">
                {errors.password_confirm}
              </Form.Control.Feedback>
            </Form.Group>
          </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button className="mx-auto" variant="outline-primary" onClick={this.onClick}>
              Submit
            </Button>
          </Modal.Footer>
        </Modal>
      </>
    )
  }
}

export default SignUp;
