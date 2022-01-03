import React from 'react'

class Contacts extends React.Component {
  render() {
    let supportEmail = this.props.supportEmail || "example@example.com";
    return (
      <>
        <h2>Контакты</h2>
        <p>
          Email: <a href={"mailto:" + supportEmail}>{supportEmail}</a>
        </p>
      </>
    )
  }
}

export default Contacts
