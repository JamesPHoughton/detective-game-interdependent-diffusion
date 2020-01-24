import React from "react";

import { Centered, AlertToaster } from "meteor/empirica:core";
import { Radio, RadioGroup } from "@blueprintjs/core";
import styled from 'styled-components';

const Container = styled.div`
  margin: 3px;
  max-width: 650px;
`


export default class InstructionStepTwo extends React.Component {

  componentDidMount() {
    document.addEventListener("keydown", this.handleKeyDown)
  }

  componentWillUnmount() {
    document.removeEventListener("keydown", this.handleKeyDown)
  }

  handleKeyDown = event => {
    if (event.keyCode == 62) {
      this.props.onNext();
    }
  }

  state = { moreClues: "", moreCorrect: "",
           morePay: "", moreContribution: ""};

  handleRadioChange = event => {
    const el = event.currentTarget;
    console.log("el", el);
    console.log("ev", event);
    this.setState({ [el.name]: el.value });
  };

  handleSubmit = event => {
    event.preventDefault();

    if (this.state.moreClues !== "bob" || this.state.moreCorrect !== "jane" ||
        this.state.morePay != "jane" || this.state.moreContribution != "c1") {
          AlertToaster.show({
            message:
              "Sorry, you have one or more mistakes. Please re-read the instructions, and ensure that you have answered the questions correctly."
          });
    } else {
      this.props.onNext();
    }
  };

  render() {
    const { hasPrev, hasNext, onNext, onPrev } = this.props;
    const { min_pay, max_pay } = this.state;
    return (
      <Container>
        <div className="instructions">
          <form onSubmit={this.handleSubmit}>
          <h2> Training: Incentives </h2>
          <p>
          You earn $1.00 for training.
          If you get a spot in the game, you earn $1.00 for
          your time, plus individual and team bonuses up to $1.00 each.
          </p>

          <h3>Individual Bonus</h3>
          <p>
          When you categorize a clue as a "Promising Lead", you earn
          $0.10 if it is true, but <strong>lose</strong> $0.10 if it is false.
          You find out what you got right after the game is over.
          </p>
          <p>
          For example: Bob and Jane organize their clues like this:
          </p>
          <img src="bobjane_notebook.png" height="300px"/>

          <p>
          Jane gets +$0.10 for one correct clue. Bob earns +$0.20 for two
          correct clues, but loses $0.20 for two mistakes. He gets no bonus.
          </p>
          <RadioGroup
            layout="row"
            label="Who had more 'Promising Leads' overall?"
            onChange={this.handleRadioChange}
            selectedValue={this.state.moreClues}
            name="moreClues"
            required
            inline
          >
              <Radio
                label="Jane"
                value="jane"
              />
              <Radio
                label="Bob"
                value="bob"
              />

          </RadioGroup>

          <p></p>
          <RadioGroup
            label="Whose 'Promising Leads' were more accurate?"
            onChange={this.handleRadioChange}
            selectedValue={this.state.moreCorrect}
            name="moreCorrect"
            required
            inline
          >
            <Radio
              label="Jane"
              value="jane"
            />
            <Radio
              label="Bob"
              value="bob"
            />
          </RadioGroup>

          <p></p>
          <RadioGroup
            label="Who earned a higher individual bonus?"
            onChange={this.handleRadioChange}
            selectedValue={this.state.morePay}
            name="morePay"
            required
            inline
          >
            <Radio
              label="Jane"
              value="jane"
            />
            <Radio
              label="Bob"
              value="bob"
            />
          </RadioGroup>

          <h3>Team bonus</h3>
          <p>
          Your team bonus is the average of all players' individual bonuses. You
          earn more by helping your team be correct and avoid mistakes.
          </p>
          <img src="collaborators.png" height="260px"/>

          <RadioGroup
            label="Which of these two collaborators contributes more to the overall team score?"
            onChange={this.handleRadioChange}
            selectedValue={this.state.moreContribution}
            name="moreContribution"
            required
            inline
          >
            <Radio
              label="Collaborator 1"
              value="c1"
            />
            <Radio
              label="Collaborator 2"
              value="c2"
            />

          </RadioGroup>
          <p>
          Before you can go to the game, you must <strong>correctly answer all
          of the above questions.</strong>
          </p>
            <p>
              <button type="button" onClick={onPrev} disabled={!hasPrev}>
                Back to Game Play
              </button>
              <button type="submit">Submit</button>
            </p>
          </form>
        </div>
      </Container>
    );
  }
}
