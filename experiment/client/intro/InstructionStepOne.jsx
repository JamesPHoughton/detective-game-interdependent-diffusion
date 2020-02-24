import React from "react";
import Round from "../game/Round.jsx"
import styled from 'styled-components';
import {GameDummy, solution, clues} from './teaching_game.js'

const Description = styled.div`
  max-width: 650px;
`

const Container = styled.div`
  margin: 3px;
`
const Boxed = styled.div`
  border: 1px solid lightgrey;
  border-radius: 2px;
  margin: 3px;
  max-width: 700px;
`

const Clue = styled.div`
  border: 1px solid lightgrey;
  border-radius: 2px;
  padding: 8px;
  margin-bottom: 8px;
  background-color: white;
  display: inline-block;
`


export default class InstructionStepOne extends React.Component {
  componentDidMount() {
    document.addEventListener("keydown", this.handleKeyDown)
  }

  componentWillUnmount() {
    document.removeEventListener("keydown", this.handleKeyDown)
  }

  handleKeyDown = event => {
    const { hasPrev, hasNext, onNext, onPrev} = this.props;
    if (event.keyCode == 62) {
      onNext()
    }
  }

  render() {
    const { hasPrev, hasNext, onNext, onPrev} = this.props;
    const game = new GameDummy();
    const player = game.players[0]
    const nbs = player.get("notebooks")
    const allow_continue = (
      // all categories have something in them
      nbs['promising_leads'].clueIDs.length > 0 &&
      nbs['dead_ends'].clueIDs.length > 0 &&
      // all the clues in true are correctly categorized
      // the player starts with no true clues, so true clues in the solution
      // imply that they successfully dragged from the neighbor
      nbs['promising_leads'].clueIDs.every(cl => solution['promising_leads'].includes(cl)) &&
      nbs['dead_ends'].clueIDs.every(cl => solution['dead_ends'].includes(cl))
    )


    return (
        <Container>
            <Description>
                <h2> Training: Game Play </h2>
                <p>
                There has been a burglary! The police chief has put all of her best
                detectives - including you - on the case.
                </p>
                <p>
                Each detective has interviewed witnesses, and collected some clues.
                Unfortunately, witnesses make mistakes (and sometimes lie). You don't
                know which of your clues are true and which are false.
                </p>
                <p>
                Compare your notes with some of the other detectives. Work out
                who is the burglar, and how they performed the crime.
                </p>
                <p>
                If you think a clue is true, <strong> drag it into the "Promising Leads"
                section of your notebook</strong>. If you think it is false (or irrelevant),
                <strong> drag it into the "Dead Ends" section</strong>. You can
                rearrange your notebook whenever you like.
                </p>
                <p>
                Your collaborators can see your "leads". If they think you are
                on the right track, they can add your clues to their
                notebooks to share with other team members.
                </p>

                <h3> To practice, correctly categorize
                the clues below as "Promising Leads" or "Dead Ends”.
                </h3>
            </Description>

            <Boxed>
              <Round game={game}
                     //round={game.rounds[0]}
                     round="training"
                     stage={game.rounds[0].stages[0]}
                     player={player} />
            </Boxed>

            <Description>
             <p>
             Before you can go to the next page, <strong>correctly categorize
             the practice clues as "Promising Leads" or "Dead Ends”</strong>.
             (Did you pay attention to the double negative?)
             </p>
             <p>
               <button type="button" onClick={onNext}
                       disabled={!allow_continue}>
                 Continue to Incentives
               </button>
             </p>
          </Description>
        </Container>

    );
  }
}
