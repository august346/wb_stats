import React from 'react'

import Auth from "./Auth"
import { Container, Nav, Navbar } from 'react-bootstrap';
import { Link } from 'react-router-dom';


class Header extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isOpen: false
    };

    this.toggle = this.toggle.bind(this);
  }

  toggle() {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }

  render() {
    let auth = this.props.auth;
    return (
      <Navbar bg="dark" variant="dark" expand="md">
        <Container>
          <Navbar.Brand as={Link} to="/">WB Stats</Navbar.Brand>
          <Navbar.Toggle className="navbar-expand-sm" aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link as={Link} to="/">Главная</Nav.Link>
              {
                auth.active && (
                  <>
                    <Nav.Link as={Link} to="/shops">Магазины</Nav.Link>
                    <Nav.Link as={Link} to="/fbs">FBS</Nav.Link>
                  </>
                )
              }
              <Nav.Link as={Link} to="/contacts">Контакты</Nav.Link>
            </Nav>
            <Auth auth={auth} />
          </Navbar.Collapse>
        </Container>
      </Navbar>
    )
  }
}

export default Header
