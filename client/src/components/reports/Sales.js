import React from 'react';

import { Button, Table } from 'react-bootstrap';
import CsvDownloader from 'react-csv-downloader';

import * as utils from '../../utils/utils.js';

function CSV(props) {
  return (
    <CsvDownloader
      filename={props.title}
      columns={props.headers.map(h => ({id: h, displayName: h}))}
      datas={props.data}
    >
      <Button variant="dark">СКАЧАТЬ</Button>
    </CsvDownloader>
  )
}

function TotalMiniTable(props) {
  let total = props.total;
  return (
    <Table className="mx-auto" variant="dark" size="sm" style={{fontSize: 10}}>
      <tbody>
        <tr>
          <td>Перечислено от WB в руб.</td>
          <td>{utils.commaNumber(total.sum_sale)}</td>
        </tr>
        <tr>
          <td>Удержано WB за услуги в руб.</td>
          <td>...</td>
        </tr>
        <tr>
          <td>Продано шт.</td>
          <td>{utils.commaNumber(total.count_sale)}</td>
        </tr>
        <tr>
          <td>Возвраты шт.</td>
          <td>{utils.commaNumber(total.count_refund)}</td>
        </tr>
      </tbody>
    </Table>
  )
}

function Sales(props) {
  let data = props.table.data;

  data = data.map((row, ind) => ({id: ind+1, ...row}));

  if (data.length === 0) {
    return (<p>No data</p>)
  }

  let total_row = data[0];

  let headers = Object.keys(data[data.length - 1]);
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
    <div>
      <h3>Отчёт:</h3>
      <TotalMiniTable total={total_row} />
      <small className="text-size-small">Первая покупка в рамках отчёта: <pre>{props.dates.min}</pre></small>
      <small className="text-size-small">Последняя покупка в рамках отчёта: <pre>{props.dates.max}</pre></small>
      <CSV title={props.table.title} headers={headers} data={data}/>
      <Table striped bordered hover size="sm" responsive="lg" style={{fontSize: 10}}>
        <caption style={{captionSide: "top"}}>{props.table.title + ".csv"}</caption>
        {thead}
        {tbody}
      </Table>
    </div>
  );
}

export default Sales;
