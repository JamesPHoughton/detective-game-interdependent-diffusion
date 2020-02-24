import React from "react";

import Slider from "meteor/empirica:slider";
import styled from 'styled-components';
import Workspace from "../game/Workspace";
import { DragDropContext } from 'react-beautiful-dnd';
import { HTMLSelect } from "@blueprintjs/core";

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
  state = { suspect: "", appearance: "", clothing: "",
            tool: "", vehicle: "",
            confidence: "", consensus: ""};

  handleSubmit = event => {
    event.preventDefault();
    const { player } = this.props;
    player.set('caseMade', this.state);
    this.props.onSubmit(this.state);
  };


  handleSelectChange = event => {
    this.setState({[event.currentTarget.id]: event.currentTarget.value});
  }


  getSliderHandler = key => {
        return value => {
          this.setState({[key]: Math.round(value * 100) / 100 });
          this.forceUpdate();
        }
  }

  render() {
    const { player, game } = this.props;
    const choiceNodes = game.get("choiceNodes")


    const submit_enabled = (this.state["suspect"]!="" &&
                            this.state["appearance"]!="" &&
                            this.state["clothing"]!="" &&
                            this.state["tool"]!="" &&
                            this.state["vehicle"]!="" &&
                            this.state["consensus"]!="" &&
                            this.state["confidence"]!="")

    return (
        <Panels>
          <DragDropContext onDragEnd={res => {}}>
            <Workspace game={game} player={player} />
          </DragDropContext>
          <Container>
            <h1> Make the case </h1>
            <p>
              Your team has narrowed down the clues to just a few
              suspects and burglary methods. Based upon what you saw in the
              game, choose the most likely of each of the options below:
            </p>


            <form onSubmit={this.handleSubmit}>
            <p>
              Which of these suspects is more likely to have committed the burglary?
            </p>

            <SliderBox>
              <select
                id="suspect"
                onChange={this.handleSelectChange}
                value={this.state['suspect']}
                required
              >
                <option key="hidden" hidden="true">Choose suspect</option>
                <option key="disabled" disabled="true">Choose suspect</option>
                {choiceNodes['suspect'].map( (node) => (
                  <option key={node} value={node}>{node}</option>
                ))}
                <option key="none" value="none">None of these</option>
              </select>
            </SliderBox>

            <p>
              Which of these descriptions is more likely to fit the burglar?
            </p>
            <SliderBox>
              <select
                id="appearance"
                onChange={this.handleSelectChange}
                value={this.state['appearance']}
                required
              >
                <option key="hidden" hidden="true">Choose appearance</option>
                <option key="disabled" disabled="true">Choose appearance</option>
                {choiceNodes['appearance'].map( (node) => (
                  <option key={node} value={node}>{node}</option>
                ))}
                <option key="none" value="none">neither of these</option>
              </select>
            </SliderBox>

            <p>
              Which of these articles of clothing is the burglar more likely to have worn?
            </p>
            <SliderBox>
              <select
                id="clothing"
                onChange={this.handleSelectChange}
                value={this.state['clothing']}
                required
              >
                <option key="hidden" hidden="true">Choose clothing</option>
                <option key="disabled" disabled="true">Choose clothing</option>
                {choiceNodes['clothing'].map( (node) => (
                  <option key={node} value={node}>{node}</option>
                ))}
                <option key="none" value="none">neither of these</option>
              </select>
            </SliderBox>

            <p>
              Which of these tools is more likely to have been used in the burglary?
            </p>
            <SliderBox>
              <select
                id="tool"
                onChange={this.handleSelectChange}
                value={this.state['tool']}
                required
              >
                <option key="hidden" hidden="true">Choose tool</option>
                <option key="disabled" disabled="true">Choose tool</option>
                {choiceNodes['tool'].map( (node) => (
                  <option key={node} value={node}>{node}</option>
                ))}
                <option key="none" value="none">neither of these</option>
              </select>
            </SliderBox>

            <p>
              Which of these vehicles is more likely to have been the getaway car?
            </p>
            <SliderBox>
              <select
                id="vehicle"
                onChange={this.handleSelectChange}
                value={this.state['vehicle']}
                required
              >
                <option key="hidden" hidden="true">Choose vehicle</option>
                <option key="disabled" disabled="true">Choose vehicle</option>
                {choiceNodes['vehicle'].map( (node) => (
                  <option key={node} value={node}>{node}</option>
                ))}
                <option key="none" value="none">neither of these</option>
              </select>
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
                  value={this.state['confidence'] == "" ? undefined : this.state['confidence'] || 0}
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
                    value={this.state['consensus'] == "" ? undefined : this.state['consensus'] || 0}
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
