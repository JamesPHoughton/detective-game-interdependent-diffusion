import React from "react";

import { StageTimeWrapper } from "meteor/empirica:core";
import Timer from "./Timer.jsx";

class timer extends React.Component {
  render() {
    const { remainingSeconds } = this.props;

    const classes = ["timer"];
    if (remainingSeconds <= 20) {
      classes.push("lessThan5");
    } else if (remainingSeconds <= 60) {
      classes.push("lessThan10");
    }

    return (
      <div className={classes.join(" ")}>
        <h4>Time Remaining:</h4>
        <span className="seconds">{Math.floor(remainingSeconds/60)}:{("0" + remainingSeconds%60).slice(-2)}</span>
      </div>
    );
  }
}

export default (Timer = StageTimeWrapper(timer));
