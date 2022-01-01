import React from 'react';

import { Routes, Route, useParams } from "react-router-dom";

import Home from "./Home";
import Contacts from "./Contacts";
import Shops from "./Shops";
import Shop from "./Shop";
import Fbs from "./Fbs";


class Content extends React.Component {
  render() {
    return (
      <Routes>
        {
          this.props.active ? (
            <>
              <Route path="/" element={<Home />} />
              <Route path="shops" element={<Shops shopApi={this.props.shopApi} />} />
                <Route path="shops/:shopId" element={<Shop keyApi={this.props.keyApi} />} />
              <Route path="fbs" element={<Fbs />} />
              <Route path="contacts" element={<Contacts />} />
            </>
          ) : (
            <>
              <Route path="/" element={<Home />} />
              <Route path="/contacts" element={<Contacts />} />
            </>
          )
        }
      </Routes>
    )
  }
}

export default Content
