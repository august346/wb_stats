import React from 'react'

class Home extends React.Component {
  render() {
    return (
      <>
        <h2>Главная</h2>
        <div>
          <p>
            Добро пожаловать в систему упрощения работы с маркетплейсами.<br />
            На данный момент работает только система отчетов по продажам Вайлдбериз. <br />
            В будущем ожидается подключения функционала: складского учета, прогнозирования продаж и закупок, адекватная работа с FBS. 
          </p>
        </div>
      </>
    )
  }
}

export default Home
