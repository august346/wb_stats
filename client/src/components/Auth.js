import React from 'react';

import { Button } from 'react-bootstrap';
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
          >Выйти</Button>{' '}
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
