import React from "react";

import { Centered } from "meteor/empirica:core";

const Radio = ({ selected, name, value, label, onChange }) => (
  <label>
    <input
      type="radio"
      name={name}
      value={value}
      checked={selected === value}
      onChange={onChange}
    />
    {label}
  </label>
);

export default class ExitSurvey extends React.Component {
  static stepName = "ExitSurvey";
  state = { age: "", gender: "", strength: "", fair: "", feedback: "" };

  handleChange = event => {
    const el = event.currentTarget;
    this.setState({ [el.name]: el.value });
  };

  handleSubmit = event => {
    event.preventDefault();
    this.props.onSubmit(this.state);
  };

  average = (arr) => arr.reduce((p, c) => p + c, 0) / arr.length;

  componentDidMount() {
    const { player, game } = this.props;
    const num_clues = player.data.notebooks.promising_leads.clueIDs.length
    player.set("individualBonus", Math.min(1, num_clues*0.1))

    const num_clue_list = game.players.map(
      player => player.data.notebooks.promising_leads.clueIDs.length)
    const mean_clues = this.average(num_clue_list)
    player.set("teamBonus", Math.min(1, mean_clues*.1))
    player.set("totalPay", 1+player.get("teamBonus")+player.get("individualBonus"))
  }

  formatPrice = num => {
    if (num === undefined) {
      return undefined
    } else {
      return  num.toFixed(2)
    }
  }

  render() {
    const { player } = this.props;
    const { age, gender, strength, fair, feedback, education } = this.state;

    return (
      <Centered>
        <div className="exit-survey">
          <h1> Exit Survey </h1>
          <p>
            Please submit the following code to receive your bonus:{" "}
            <strong>{player._id}</strong>.
          </p>
          <p>
            The game you played was part of an experimental treatment in which
            none of the clues were false, and any could have been helpful in
            solving the mystery.
          </p>
          <p>
            In addition to your <strong>base payment</strong> of $1.00,
            you earned an <strong>individual bonus</strong> of $
            {this.formatPrice(player.get("individualBonus"))},
            and a <strong>team bonus</strong> of $
            {this.formatPrice(player.get("teamBonus"))},
            for a total of ${this.formatPrice(player.get("totalPay"))}.
          </p>
          <br />
          <p>
            Please answer the following short survey. You do not have to provide
            any information you feel uncomfortable with.
          </p>
          <form onSubmit={this.handleSubmit}>
            <div className="form-line">
              <div>
                <label htmlFor="age">Age</label>
                <div>
                  <input
                    id="age"
                    type="number"
                    min="0"
                    max="150"
                    step="1"
                    dir="auto"
                    name="age"
                    value={age}
                    onChange={this.handleChange}
                  />
                </div>
              </div>
              <div>
                <label htmlFor="gender">Gender</label>
                <div>
                  <input
                    id="gender"
                    type="text"
                    dir="auto"
                    name="gender"
                    value={gender}
                    onChange={this.handleChange}
                    autoComplete="off"
                  />
                </div>
              </div>
            </div>

            <div>
              <label>Highest Education Qualification</label>
              <div>
                <Radio
                  selected={education}
                  name="education"
                  value="high-school"
                  label="High School"
                  onChange={this.handleChange}
                />
                <Radio
                  selected={education}
                  name="education"
                  value="bachelor"
                  label="US Bachelor's Degree"
                  onChange={this.handleChange}
                />
                <Radio
                  selected={education}
                  name="education"
                  value="master"
                  label="Master's or higher"
                  onChange={this.handleChange}
                />
                <Radio
                  selected={education}
                  name="education"
                  value="other"
                  label="Other"
                  onChange={this.handleChange}
                />
              </div>
            </div>

            <div className="form-line thirds">
              <div>
                <label htmlFor="strength">
                  What strategy did you use to play the game?
                </label>
                <div>
                  <textarea
                    dir="auto"
                    id="strength"
                    name="strength"
                    value={strength}
                    onChange={this.handleChange}
                  />
                </div>
              </div>
              <div>
                <label htmlFor="fair">Do you feel the pay was fair?</label>
                <div>
                  <textarea
                    dir="auto"
                    id="fair"
                    name="fair"
                    value={fair}
                    onChange={this.handleChange}
                  />
                </div>
              </div>
              <div>
                <label htmlFor="feedback">
                  Did you have any problems?
                  How could the game be improved?
                </label>
                <div>
                  <textarea
                    dir="auto"
                    id="feedback"
                    name="feedback"
                    value={feedback}
                    onChange={this.handleChange}
                  />
                </div>
              </div>
            </div>

            <button type="submit">Submit</button>
          </form>
        </div>
      </Centered>
    );
  }
}
