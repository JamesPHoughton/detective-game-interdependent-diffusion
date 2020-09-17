import { NonIdealState } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import React from "react";
import { Link } from "react-router-dom";
import { Redirect } from 'react-router-dom'
import NoBatch_PayCode from "./NoBatch_PayCode"

export default class NoBatch extends React.Component {
  componentDidMount(){
    const thisURL = window.location['href'];
    var newURL = "";
    if (window.location['origin'] == 'http://detectivea.meteorapp.com') {
      newURL = thisURL.replace(window.location['origin'], "http://detectiveb.meteorapp.com");
      window.location.replace(newURL)
    } else if (window.location['origin'] == 'http://detectiveb.meteorapp.com') {
      newURL = thisURL.replace(window.location['origin'], "http://detectivec.meteorapp.com");
      window.location.replace(newURL)
    } else if (window.location['origin'] == 'http://detectivec.meteorapp.com') {
      newURL = thisURL.replace(window.location['origin'], "http://detectived.meteorapp.com");
      window.location.replace(newURL)
    }

  }

  render_redirect_notice(newURL) {
    return(
      <div>
        <h3> The primary game server is full, you are being redirected to an overflow server.</h3>
        <p> If you see this message after 5 seconds, please click:</p>
        <p><a href={newURL}>{newURL}</a></p>
      </div>
    )
  }

  render() {
    const thisURL = window.location['href'];
    var newURL = "";
    if (window.location['origin'] == 'http://detectivea.meteorapp.com') {
      newURL = thisURL.replace(window.location['origin'], "http://detectiveb.meteorapp.com");
    } else if (window.location['origin'] == 'http://detectiveb.meteorapp.com') {
      newURL = thisURL.replace(window.location['origin'], "http://detectivec.meteorapp.com");
    } else if (window.location['origin'] == 'http://detectivec.meteorapp.com') {
      newURL = thisURL.replace(window.location['origin'], "http://detectived.meteorapp.com");
    }
    if (newURL != ""){
      return render_redirect_notice(newURL)
    }
    return (
      <NoBatch_PayCode/>
    );
  }
}
