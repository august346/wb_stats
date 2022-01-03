/* eslint-disable no-unused-expressions */
/* eslint-disable no-restricted-globals */
import React, { Component } from 'react';
import jwt_decode from "jwt-decode";

import './App.css';
import API from "./utils/API";
import Header from "./components/Header"
import Content from "./components/Content"


const JWT_STORAGE_KEY = "JWT";


function isLoggedIn() {
  let jwt = getJWT();
  if (!jwt) {
    return false;
  }
  let now = ~~(new Date().getTime() / 1000)
  try {
    return jwt_decode(jwt.access_token).exp > now;
  } catch (e) {
    console.log(e, jwt);
    return false
  }
}


function getJWT() {
  let jwtString = localStorage.getItem(JWT_STORAGE_KEY);
  if (!jwtString) {
    return false;
  }

  return JSON.parse(jwtString);
}

function getRequestConfig() {
  var jwt = getJWT();
  return {
    headers: {
      'Authorization': capitalizeFirstLetter(jwt.token_type) + " " + jwt.access_token
    }
  }
}

let shopApi = {
  aGetKeys: async function() {
    return API.get('/wb/wb_api_keys/', getRequestConfig())
  },
  aCreateKey: async function(key, name) {
    return API.post('/wb/wb_api_keys/', {key: key, name: name}, getRequestConfig())
  },
}

let keyApi = {
  aGetKey: async function(id) {
    return API.get('/wb/wb_api_keys/' + id, getRequestConfig())
  },
  aPatchKey: async function(id, name) {
    return API.patch('/wb/wb_api_keys/' + id, name, getRequestConfig())
  },
  aDeleteKey: async function(id) {
    return API.delete('/wb/wb_api_keys/' + id, getRequestConfig())
  },
  aGetReport: async function(id, dateFrom, dateTo, brands) {
    return API.post(
      `/wb/wb_api_keys/${id}/report`,
      {date_from: dateFrom, date_to: dateTo, brands: brands},
      getRequestConfig()
    )
  }
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

async function getInfo() {
  return API.get('/');
}


class App extends Component {
  constructor(props) {
    super(props);
    this.onAuth = this.onAuth.bind(this);
    this.state = {
      isLoggedIn: isLoggedIn()
    };
  }

  onAuth(data, isLoggedIn) {
    if (isLoggedIn) {
      localStorage.setItem(JWT_STORAGE_KEY, JSON.stringify(data));
    } else {
      localStorage.removeItem(JWT_STORAGE_KEY);
    }

    this.setState({
      isLoggedIn: isLoggedIn,
    });
  }

  async componentDidMount() {
    await getInfo().then(
      (resp) => {
        console.log(resp.data);
        this.setState({
          supportEmail: resp.data.support_email
        })
      }
    ).catch(
      (e) => {
        let resp = e.response;
        let data = resp.data;
        console.log(0, resp.status, data, typeof data.detail, typeof data.detail === 'string');
      }
    );
  }

  render() {
    return (
      <div className='App'>
        <Header auth={{active: this.state.isLoggedIn, onAuth: this.onAuth}}/>
        <Content
          supportEmail={this.state.supportEmail}
          active={this.state.isLoggedIn}
          shopApi={shopApi}
          keyApi={keyApi}
        />
      </div>
    );
  }
}
export default App;
