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

## Feb. 25, 2020 - Pilot
Used updated spur clues from 4th round of pretest.

Decided to add a dimension for investigating the relative effect of network structure. This way we can say - Interdependence gets you $\Delta x$ compared to baseline, clustering and longer path lengths get you $\Delta y$ compared to baseline, and their interaction gets you an additional $\Delta xy$. This makes the rhetorical structure of the paper more symmetric, as I start by saying that we typically look at network structure, but ignore belief structure. Now we can look at both.

### May 5-7 - Pilot
Purpose of this set of 3 quad games (2 levels of belief interaction, 2 levels of clustering in the network) was to estimate the number of games to run in order to get sufficient power to assess the hypothesis.

Reviewing the games, there seems to be lots of noise, so if there is an effect to be seen, it would require more games than I can afford.

There are several possible reasons for this
1. Theory is incorrect
 - Ie, something about actual human belief propagation invalidates the results of the simulation theory. (e.g. complex contagion result breaks down when you allow small amounts of spontaneous transmission)
 - Understood mechanisms are incorrect - i.e. agreement cascades don't lead to polarization even when they happen, but something else was happening in my simulation that I wasn't able to isolate, and which creates the behavior I was seeing in the simulation.
 - It could be that there is always just lots of noise, and the best experiment would still need lots of trials to see an effect. That might mean that the effect itself, even if it exists, is probably of little consequence for actual social contagion, or doesn't give much insight.

2. Technical problems with experiment analysis
 - It may be that the code I'm using to post-process the experiments has a bug, and that if I found the bug, I would see the expected effect
 - It could be that I'm not analyzing on the right variables (ie, just the core clues, vs all clues, and at which times, and what should be the baselines for comparison)
 - The measures themeselves could be poor estimates of the polarization phenomenon (I used them in the simulation partly because they are simple to explain, which is correct for a theory-building paper, but may not be optimal for an empirical one.)
 - It could be that with the small number of beliefs, there is not enough 'resolution' to see the polarization

 To check these, break down the code into testable chunks (should do anyways), list all the various combinations of operationalizations of the outcome measures given the experimental design, and try against existing pilot data or in simulations.

 Bootstrap confidence intervals for each measurement of polarization, drawing from the population of players. Compare the variance in the polarization measure to the total measurement, and the expected effect size. (ie, PC1 may carry 30% of variance, effect size may be 10-15%. If bootstrap variance in 20%, may need a larger population...)

3. Problems with experiment parameters
 - Parameters: number of players, number of starting beliefs each, length of time, number of beliefs total, size of semantic network, redundancy of beliefs
 - In the theoretical work, I have already seen how the effect varies with parameter settings. For example. in parameter regimes where no contagion takes place, there is no difference between treatment and control. When contagion is too complete, all beliefs are adopted, so that there is no difference between treatment and control. In between, there are varying levels of effect that depend on the parameters
 - It could be that with the small number of players, there is not enough network space for camps to form. (Small network is argument for it's presence in larger groups if observed here, though.)

 To check these, simulate experiment as it is implemented, either using triangle closing decision rule, hazard rate model, or neural network model. Vary the parameters to see if a different set would give larger observed effects.


4. Problems with experiment design/conceptualization
 - Perhaps the treatment and control do not replicate conditions of interdependence and independence closely enough.
 - It could be that the control condition doesn't block interdependence well enough, because there is still the familiarity mechanism in play. The more times an individual has seen a rim node, the more likely they are to adopt clues containing rim nodes. This could introduce enough of the agreement cascade mechanism that control conditions are behaving like interdependent conditions. It may be that i'm incorrect in assuming that just analyzing on the spoke clues eliminates the effect of the familiarity mechanism. I haven't actually done simulations including the similarity mechanism. To evaluate,
 - It could be that the interdependent condition doesn't replicate conditions of interdependence as the game is actually played. For example, as we tell individuals in advance where the theft occurred, the spoke clues are preferred over the cross-link clues. If individuals first adopt spoke clues, and then fill in the cross-links that reinforce what they believe, then the spoke clues (diffusing first) would be diffusing essentially independently. (Or, dependently on the prior belief in the object being stolen from the crime scene.)  The cross-link clues might then be diffusing dependently. To evaluate, plot adoption of spokes in 15s interval and also of spurs. plot probability that first mention of rim element is in a spoke adoption…


Explore:
number of beliefs adopted over time (spoke + spur/cross-link)
number of beliefs adopted vs polarization measures (at each timestep?)
polarization measures over time.


### Other outcomes / todos
- The double negative in the intro screens still seems to trip up a lot of people. People in abdullah's class don't think it's necessary.
- put the payout on the thanks screen
