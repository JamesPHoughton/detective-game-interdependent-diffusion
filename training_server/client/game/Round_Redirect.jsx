import React from "react";
import { Link } from "react-router-dom";
import { Redirect } from 'react-router-dom'


export default class Round extends React.Component {
  componentDidMount(){
    const thisURL = window.location['href'];
    const newURL = thisURL.replace(window.location['origin'], "http://detectivea.meteorapp.com");
    window.location.replace(newURL)
  }

  render() {
    const thisURL = window.location['href'];
    const newURL = thisURL.replace(window.location['origin'], "http://detectivea.meteorapp.com");
    return (
      <div>
        <h3> The primary game server is full, please click below to access overflow server:</h3>
        <p><a href={newURL}>{newURL}</a></p>
      </div>
    );
  }
}
