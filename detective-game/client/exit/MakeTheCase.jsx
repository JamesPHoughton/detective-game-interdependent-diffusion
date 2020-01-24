import React from "react";

import Slider from "meteor/empirica:slider";
import styled from 'styled-components';
import Workspace from "../game/Workspace";
import { DragDropContext } from 'react-beautiful-dnd';

const Container = styled.div`
  margin: 4px;
  border: 2px solid lightgrey;
  border-radius: 2px;
  padding: 15px;
  max-width: 600px;

`
const Panels = styled.div`
  margin: 3px;
  display: flex;
  flex-direction: row;
`

const SliderBox = styled.div`
  margin: 10px;
  padding: 10px;
`


export default class MakeTheCase extends React.Component {
  static stepName = "MakeTheCase";
  state = { statement: "", confidence: "", consensus: ""};

  handleSubmit = event => {
    event.preventDefault();
    const { player } = this.props;
    player.set('caseMade', this.state);
    this.props.onSubmit(this.state);
  };


  handleTextChange = event => {
    this.setState({ "statement": event.currentTarget.value});
  }


  getSliderHandler = key => {
        return value => {
          this.setState({[key]: Math.round(value * 100) / 100 });
          this.forceUpdate();
        }
  }

  render() {
    const { player, game } = this.props;
    const { statement, confidence, consensus } = this.state;

    const submit_enabled = this.state["statement"]!="" && this.state["confidence"]!=""

    return (
        <Panels>
          <DragDropContext onDragEnd={res => {}}>
            <Workspace game={game} player={player} />
          </DragDropContext>
          <Container>
            <h1> Make the case </h1>

            <form onSubmit={this.handleSubmit}>
            <p>
              What do you think happened in this mystery?
              (Use your own words to describe what happened in the box below.)
            </p>

            <SliderBox>
            <textarea
              id="statement"
              rows="5"
              cols="60"
              placeholder="Enter Text Here (Required)"
              value={statement}
              onChange={this.handleTextChange}
              required
            />
            </SliderBox>


            <p> How confident are you in your solution to the mystery?
            (Click the slider below to enter a value. 0% implies no confidence,
            100% implies complete confidence.) </p>

            <SliderBox>
              <Slider
                  min={0}
                  max={100}
                  stepSize={1}
                  labelStepSize={25}
                  onChange={this.getSliderHandler("confidence")}
                  value={confidence == "" ? undefined : confidence || 0}
                  labelRenderer={val => val+"%"}
                  disabled={false}
                  hideHandleOnEmpty
                />
              </SliderBox>

              <p> What fraction of your team do you think shares your solution?
              (Click the slider below to enter a value. 0% implies that no other
                members of your team agree, 100% implies that all other members
                of your team agree with you.) </p>

              <SliderBox>
                <Slider
                    min={0}
                    max={100}
                    stepSize={1}
                    labelStepSize={25}
                    onChange={this.getSliderHandler("consensus")}
                    value={consensus == "" ? undefined : consensus || 0}
                    labelRenderer={val => val+"%"}
                    disabled={false}
                    hideHandleOnEmpty
                  />
                </SliderBox>

              <button
                type="submit"
                disabled={!submit_enabled}>
              Submit
              </button>
            </form>

          </Container>
      </Panels>
    );
  }
}
