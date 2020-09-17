import { NonIdealState } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import React from "react";
import { Link } from "react-router-dom";

export default class NoBatch extends React.Component {
  render() {
    // Not sure what icon works best:
    // - SMALL_CROSS
    // - BAN_CIRCLE
    // - ERROR
    // - DISABLE
    // - WARNING_SIGN
    return (
      <NonIdealState
        icon={IconNames.ISSUE}
        title="No experiments available"
        description={
          <>
            <p>
              I'm sorry you did not get to play today.
            </p>
            <p>
              This is a multiplayer experiment, and to ensure that games have
              enough players to launch, participants need to begin the HIT
              immediately upon accepting.
            </p>
            <p>
              If you would like to be notified of the start times of future
              games, please enter <strong> NB-SUBSCRIBE </strong> as the completion
              code.
            </p>
            <p>
              Otherwise, please enter the code <strong> NB1246 </strong>.
            </p>
            <p>
              I will be running experiments throughout the week. I hope you can
              join us again.
            </p>
          </>
        }
      />
    );
  }
}
