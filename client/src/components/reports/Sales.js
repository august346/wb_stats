import React from 'react';

import { Table } from 'react-bootstrap';

function Sales(props) {
  let data = props.data;

  if (data.length === 0) {
    return (<p>No data</p>)
  }

  let headers = Object.keys(data[0]);
  let thead = (
    <thead>
      <tr key={"header"}>
        <th>#</th>
        {headers.map((key) => (
          <th key={"header" + key}>{key}</th>
        ))}
      </tr>
    </thead>
  );
  let tbody = (
    <tbody>
      {data.map((item, ind) => {
        let rowKey = item.wb_id + item.barcode;
        return (
          <tr key={rowKey}>
            <td>{ind + 1}</td>
            {headers.map((key) => (
              <td key={rowKey + key}>{item[key]}</td>
            ))}
          </tr>
        )
      })}
    </tbody>
  );

  return (
    <Table striped bordered hover size="sm" style={{fontSize: 10}}>
      <caption style={{captionSide: "top"}}>{props.title + ".csv"}</caption>
      {thead}
      {tbody}
    </Table>
  );
}

export default Sales;
