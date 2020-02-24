import Empirica from "meteor/empirica:core";

// This is where you add bots, like Bob:

Empirica.bot("bob", {
//   // // NOT SUPPORTED Called at the beginning of each stage (after onRoundStart/onStageStart)
//   // onStageStart(bot, game, round, stage, players) {},

  // Called during each stage at tick interval (~1s at the moment)
  onStageTick(bot, game, round, stage, secondsRemaining) {
    period = 10  // ticks (seconds) btw actions on average
    if (Math.random() < 1/period) {

      // collect exposed clues
      const alterIDs = bot.get("alterIDs");

      var exposed = alterIDs.map((alterID, index) => {
        const alter = _.find(game.players, p=>p._id == alterID);
        const altTrue = alter.get("notebooks")['promising_leads']
        //const clues = altTrue.clueIDs.map(cID => game.get("clues")[cID]);
        return altTrue.clueIDs
        //return clues;
        })

      exposed = exposed.reduce((acc, val) => acc.concat(val), [])

      // choose a clue to move
      var activeClue = exposed[Math.floor(Math.random()*exposed.length)];


      // remove clue from all player notebooks
      // (we know at this point that the clue will be added to the workspace,
      // and we'll need to reorder it anyways)
      const notebookOrder = bot.get("notebookOrder");
      const notebooks = bot.get("notebooks");
      var numNotebooks = notebookOrder.length;
      for (var i = 0; i < numNotebooks; i++) {
        var nb = notebookOrder[i];
        const clueList = notebooks[nb].clueIDs;
        if (clueList.includes(activeClue)) {
          const newClueList = _.filter(clueList, c => c != activeClue);
          notebooks[nb].clueIDs = newClueList;
        }
      }


      var destination = notebookOrder[Math.floor(Math.random()*numNotebooks)];
      var index = Math.floor(Math.random()*notebooks[destination]['clueIDs'].length)

      //console.log(bot['id'] +'_'+ activeClue +'_'+ destination +'_'+ index)

      // add clue to the appropriate place in the workspace
      notebooks[destination].clueIDs.splice(
        index,
        0,
        activeClue
      );
      // update the player's workspace
      bot.set("notebooks", notebooks);

    }


  }

//   // // NOT SUPPORTED A player has changed a value
//   // // This might happen a lot!
//   // onStagePlayerChange(bot, game, round, stage, players, player) {}

//   // // NOT SUPPORTED Called at the end of the stage (after it finished, before onStageEnd/onRoundEnd is called)
//   // onStageEnd(bot, game, round, stage, players) {}
})
