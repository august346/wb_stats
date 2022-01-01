import React from 'react';

import { Alert, Button, Form, Modal } from 'react-bootstrap';
import { Link } from 'react-router-dom';

import SignUp from "./SignUp";
import SignIn from "./SignIn";



class Auth extends React.Component {
  render() {
    if (this.props.auth.active) {
      return (
        <div >
          <Button
            as={Link}
            to="/"
            variant="outline-primary"
            className="btn me-2"
            onClick={() => this.props.auth.onAuth({}, false)}
          >LogOut</Button>{' '}
        </div>
      )
    }

    return (
      <div >
        <SignIn onAuth={this.props.auth.onAuth} />
        <SignUp />
      </div>
    );
  }
}

export default Auth;
