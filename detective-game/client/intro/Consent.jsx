import React from "react";

import { Centered, ConsentButton } from "meteor/empirica:core";
import styled from 'styled-components';


const Description = styled.div`
  max-width: 650px;
`

export default class Consent extends React.Component {
  render() {
    return (
      <Description>
        <div className="consent">
          <h1> Consent Form </h1>
          <h2> About the experiment </h2>
          <p>
          The game you will play is an experiment to test team learning.
          The experiment takes about 20 minutes.
          </p>
          <p>
          In order to shorten waiting-room time, more people are invited to
          train for the game than will actually get to play.
          Everyone will be paid for training.
          </p>

          <h2> Risks </h2>
          <p>
          There are no known or anticipated risks to participating.
          As they say in the movies, "All characters and events
          depicted in this [game] are entirely fictitious."
          </p>

          <h2> What you need to do </h2>
          <p>
          You need to use a computer, not a mobile device.
          </p>
          <p>
          Once the game starts, you need to give it your full attention for
          8 minutes.
          </p>
          <p>
          You play the game in real-time (not in rounds). <strong>If you don't play actively, your
          team members may lose part of their bonus.</strong>
          </p>

          <h2> Consent to participate </h2>
          <p>
          If you have any questions, please email detective@mit.edu.
          You may withdraw from this experiment at any time.
          </p>
          <p>
          This HIT is part of an MIT scientific research project. Your decision
          to complete this HIT is voluntary. There is no way for us to identify
          you. The only information we will have, in addition to your responses,
          is the timestamps of your interactions with our site. The results of
          this experiment may be presented at scientific meetings or published
          in scientific journals. Clicking on the 'AGREE' button on the bottom
          of this page indicates that you are at least 18 years of age and agree
          to complete this HIT voluntarily.
          </p>
          <br />
          <ConsentButton text="I AGREE" />
        </div>
      </Description>
    );
  }
}
