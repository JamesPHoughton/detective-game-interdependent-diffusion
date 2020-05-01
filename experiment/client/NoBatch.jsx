import { NonIdealState } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import React from "react";
import { Link } from "react-router-dom";
import { Redirect } from 'react-router-dom'

export default class NoBatch extends React.Component {
  componentDidMount(){
    window.location.replace('http://pilot.meteorapp.com')
  }

  render() {
    return (
      <div>
        <h3> The primary game server is full, please click below to access overflow server:</h3>
        <a href='http://pilot.meteorapp.com'/>
      </div>
    );
  }
}
