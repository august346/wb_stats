import React from 'react';

import { Button, Table } from 'react-bootstrap';
import CsvDownloader from 'react-csv-downloader';

function CSV(props) {
  return (
    <CsvDownloader
      filename={props.title}
      columns={props.headers.map(h => ({id: h, displayName: h}))}
      datas={props.data}
    >
      <Button variant="dark">DOWNLOAD</Button>
    </CsvDownloader>
  )
}

function Sales(props) {
  let data = props.table.data;

  data = data.map((row, ind) => ({id: ind+1, ...row}));

  if (data.length === 0) {
    return (<p>No data</p>)
  }

  let headers = Object.keys(data[0]);
  let thead = (
    <thead>
      <tr key={"header"}>
        {headers.map((key) => (
          <th key={"header" + key}>{key === "id"? "#" : key}</th>
        ))}
      </tr>
    </thead>
  );
  let tbody = (
    <tbody>
      {data.map((item, ind) => {
        let rowKey = item.wb_id + item.brand + item.barcode;
        return (
          <tr key={ind}>
            {headers.map((key) => (
              <td key={rowKey + key}>{item[key]}</td>
            ))}
          </tr>
        )
      })}
    </tbody>
  );


  return (
    <>
      <h3>Report:</h3>
      <small className="text-size-small">First sale: <pre>{props.dates.min}</pre></small>
      <small className="text-size-small">Last sale: <pre>{props.dates.max}</pre></small>
      <CSV title={props.table.title} headers={headers} data={data}/>
      <Table striped bordered hover size="sm" style={{fontSize: 10}}>
        <caption style={{captionSide: "top"}}>{props.table.title + ".csv"}</caption>
        {thead}
        {tbody}
      </Table>
    </>
  );
}

export default Sales;
