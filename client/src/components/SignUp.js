import React from 'react';

import { Alert, Button, Form, Modal } from 'react-bootstrap';

import API from "../utils/API";


async function signUp(email, password, password_confirm) {
  if (password !== password_confirm) {
    alert("Пароли не совпадают");
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

      errors: {},
    }
  }

  handleClose() {
    this.setState(
      {
        show: false,

        email: null,
        password: null,
        password_confirm: null,

        errors: {},
      }
    );
  }

  handleShow() {
    this.setState({show: true});
  }

  handleInputChange(e) {
    this.setState({[e.target.name]: e.target.value, errors: {}});
  }

  async onClick(e) {
    let errors = {};
    if (!this.state.email) {
      errors.email = "Не может быть пустым";
    } else if (!this.state.email.match(/^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[A-Za-z]+$/)) {
      errors.email = "Невалидный email";
    }
    if (!this.state.password) {
      errors.password = "Не может быть пустым";
    } else if (!this.state.password.match(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/)) {
      errors.password = "В пароле должны быть цифры и латинские буквы";
    }
    if (this.state.password !== this.state.password_confirm) {
      errors.password_confirm = "Не совпадает";
    }

    if (Object.keys(errors).length !== 0) {
      this.setState({errors})
      return ;
    }

    await signUp(
      this.state.email,
      this.state.password,
      this.state.password_confirm,
    ).then(
      (data) => {
        this.handleClose();
        alert("Успешно. Дождитесь письма на email.")
      }
    ).catch(
      (err) => {
        let resp = err.response;
        let data = resp.data;
        if (resp.status === 400) {
          if (typeof data.detail === 'string') {
            this.setState({errors: {general: data.detail}});
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
    return (
      <>
        <Button variant="primary" className="mx-2" onClick={this.handleShow}>
          Регистрация
        </Button>

        <Modal show={this.state.show} onHide={this.handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>Регистрация</Modal.Title>
          </Modal.Header>
          <Modal.Body>
          <Form>
            {!!this.state.errors.general && (
              <Alert variant="danger">
                {this.state.errors.general}
              </Alert>
            )}
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email</Form.Label>
              <Form.Control
                name="email"
                type="email"
                required
                placeholder="Enter email"
                onChange={this.handleInputChange}
                isInvalid={!!this.state.errors.email} />
              <Form.Text className="text-muted">
                Мы не передаём ваш email сторонним сервисам
              </Form.Text>
              <Form.Control.Feedback type="invalid">
                {this.state.errors.email}
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Пароль</Form.Label>
              <Form.Control
                name="password"
                type="password"
                required placeholder="Password"
                onChange={this.handleInputChange}
                isInvalid={!!this.state.errors.password} />
              <Form.Control.Feedback type="invalid">
                {this.state.errors.password}
              </Form.Control.Feedback>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword2">
              <Form.Label>Подтверждение паролья</Form.Label>
              <Form.Control
                name="password_confirm"
                type="password"
                placeholder="Password"
                onChange={this.handleInputChange}
                isInvalid={!!this.state.errors.password_confirm} />
              <Form.Control.Feedback type="invalid">
                {this.state.errors.password_confirm}
              </Form.Control.Feedback>
            </Form.Group>
          </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button className="mx-auto" variant="outline-primary" onClick={this.onClick}>
              Зарегистрировать
            </Button>
          </Modal.Footer>
        </Modal>
      </>
    )
  }
}

export default SignUp;
