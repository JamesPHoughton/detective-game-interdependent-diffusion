# Detective Game Development Journal
James Houghton
houghton@mit.edu

This is a running record of the development and execution of the detective game.

----
## March 1, 2019 - Demo
Demoed drag-and-drop gameplay and basic clue pattern for lab group. Everything breaks, the game doesn't make sense because most of the network positions are empty, and I tell everyone too much about the game before they play it, so they can't make natural decisions. Oh well!



## May 15 - Integration Test
Ran single treatment game as a test of the platform. Asked for a text description of what players thought had happened.

Did a poor job minimizing penetration of outside biases (e.g. "Ramirez" more likely than "Green" to have committed crime). Need to pre-test the clue elements.


## July 10+18th, 2019 - Pilot
Split the game in half, ran a control game on the 10th, and a treatment game on the 18th.

Postgame survey asks for players to select who did it (tool/car/etc) from a dropdown box.

Decided that better to pull a single pool of participants and randomly assign them to treatment vs control, to make sure there are not systematic differences between the samples.


## July 23, 2019 - Pilot Attempt
Game failed to get enough players to launch before the lobby tied out. Remedy: set very long lobby timeout, and sign up players in advance.

## July 26, 2019 - Pilot
Learning about recruitment! See notes [here](https://forum.turkerview.com/threads/launching-multiplayer-games-poor-click-through.2419/).

Set up game as matched pair - sign up 100 players with a $0.05 sign-up (qual?) hit, make 60 hits available at game time, get 40 players to actually play quickly.

Filler clues in control game are still 'floating' - in that they are the same edges as in the treatment game, but both ends have been replaced with random unique values. This is pretty clearly non-interacting, but it's unclear if the task is the same between the treatment and control case, as those clues never get adopted.

Showed results from these pilots at AOM.

Dropdown box survey is not great. It forces diversity, as you can only pick one, and doesn't feel like a legitimate way to ask the question. What if people have equal certainty about two individuals? should be able to capture that. Remedy: sliders.

## Oct. 1, 2019 - Pilot
Matched pair game again, seems to be working. Clues are 'spur' clues, but I didn't do the pretest very well (i.e. the things I asked in the pretest questions didn't correspond carefully to what I actually used in the game.)

Added sliders, which gets much more nuanced picture of players' confidence in each clue element. Sliders have default value, which is right in the middle on maximum uncertainty. But, screen forces you to enter a value on all sliders, so this artificially pushes the answers away from the middle.


## Nov. 27, 2019 - Pilot
Include Abdullah, so he could understand the gameplay.
Sliders are blank (no default value), but error in formatting of "make-the-case" page leaves off a slider label.

Realize I am using client-side time for event logging, means that I can't trust the order in which people make their decisions, and so hazard regressions for this and prior games are not credible.


## Dec. 11, 2019 - Pilot
Test server-side logging, seems to work properly. Have a client side error where a participant sees training and exit screens, but doesn't get to play.


## Jan. 16, 2020 - Pilot
Run again, code same as Dec. 11. Use meteor/galaxy's client side error reporting to see if insight into the Dec. 11 client side error. It doesn't repeat itself. On the plus side, I need two sets of properly formatted timeseries data to test the code that manages the hazard rate regressions and subsequent calculations. Now I have them.

Realize that the control 'spur' clues are so unrelated to the game that they don't get adopted, and so are not a very good control. The language used decreases the salience of the information. For example, where in the treatment game I say "the *clothing* was found with *the tool*" in the treatment I have been saying "someone wearing the *clothing* was seen on *some street*". A more parallel clue could be "the *clothing* was found on *some street*", which is also more salient in the context of a mystery. Making updates. Run another pilot, or ship it?

What we really want is for the average spoke clue to be adopted the same number of times in the treatment and the control condition, so that any effect on polarization or similarity is due to which clues get adopted, not the number of clues that get adopted.

Some issues with the bonusing postprocessor. Got it worked out?
