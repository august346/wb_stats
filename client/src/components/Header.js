import React from 'react'

import Auth from "./Auth"
import { Container, Nav, Navbar, NavDropdown } from 'react-bootstrap';
import { Link } from 'react-router-dom';


class Header extends React.Component {
  render() {
    let auth = this.props.auth;
    return (
      <Navbar bg="dark" variant="dark">
        <Container>
        <Navbar.Brand as={Link} to="/">WB Stats</Navbar.Brand>
        <Nav className="mr-auto">
          <Nav.Link as={Link} to="/">Home</Nav.Link>
          {
            auth.active && (
              <>
                <NavDropdown title="Analytic" id="basic-nav-dropdown">
                  <NavDropdown.Item as={Link} to="/shops">Shops</NavDropdown.Item>
                  <NavDropdown.Item as={Link} to="/fbs">FBS</NavDropdown.Item>
                </NavDropdown>
              </>
            )
          }
          <Nav.Link as={Link} to="/contacts">Contacts</Nav.Link>
        </Nav>
        <Auth auth={auth} />
        </Container>
      </Navbar>
    )
  }
}

export default Header
