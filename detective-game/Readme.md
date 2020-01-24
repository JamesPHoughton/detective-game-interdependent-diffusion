# Prototype

_This project was generated with [create-empirica-app](https://github.com/empiricaly/create-empirica-app)._

## Running the game server

To run this project locally, run the local server:

```sh
meteor
```

To run with a local version of the empirica core:
```sh
METEOR_PACKAGE_DIRS=/Library/MeteorPackages/ meteor
```

To inspect the server side code, add `meteor --inspect flag`


To deploy to galaxy:
1. uncomment lines in the `client: main.js` to make sure that they see the
production version
2. start the mongodb database

3. deploy
```sh

DEPLOY_HOSTNAME=us-east-1.galaxy-deploy.meteor.com meteor deploy detective.meteorapp.com --settings settings.json
```
4. run games
5. download data
6. shut down galaxy server
7. shut down mongodb database


Set up mongodb atlas with galaxy: https://www.okgrow.com/posts/mongodb-atlas-setup
troubleshooting `authentication fail` involved creating a new user with a simple password and trying again...


## Todo:
- [ ] "I'm done" button (I have a solution)
- [x] log responses
- [x] reconstruct the state in python
- [x] remove 'round' indicator
- [x] inactivity timeout
- [ ] test on firefox, safari, chrome
- [x] $1 participation + $1 individual bonus + $1 group bonus
- [] add "have you played this game or a similar game in the past?"
- [ ] check number of drags per 10s, look for some convergence/slowing
- [x] Add question "What do you think everyone else will say?", "Do you think most people in the group got the same result?"
- [x] add a "you must enter text into the make a case box to submit" button
- [x] add "collaborators' promising leads"
- [x] for pilot: "did you have enough time to play? was the time too long?"
- [ ] case introduction screen
- [x] don't give idle warning on exit material
- [ ] make a separate settings file for the galaxy deploy which changes the header, etc.
- [x] in the teaching screen, make timer have a different number than 0, and make the crime scene and stolen object more obviously fake, not a mistake
- [ ] add some logging so that I can see how games progress when other people are playing them


## questions
- Q: should the social information be displayed as "neighbors", "colleagues", "detectives", "collaborators"? A: Collaborators. Neighbors is a network term, not useful for he task.
- Q: should the numbers on the social information be 1 and 2, or (say), 12 and 7? A:1 and 2
- Q: should the notebook sections be titled 'probably true' 'probably false', or 'leads', or 'shared/private leads'? A: 'promising leads' vs 'dead ends'
- Q: should there be a 'trash'? A:no
- Is it better to overstate how long the experiment will take, in order to get a larger percentage of compliers?

- dragging from a neighbor into 'dead ends' is different from 'forgetting'
- Q: How do we know they are taking it seriously? A: If there is difference between control
and treatment case, then there is attention being paid.

- Q: do I 'break' connections one at a time (ie, one clue gets renamed "fred" instead of "george") or in batches (half of "freds" become "georges"). A: one at a time is simpler.

- Q: If we pay 10c for each correct clue, and cap at $1, are we implicitly saying that they should have at least 10 clues? does this bias the result? A: Probably. Removed explicit price for reward.

- how to do an attention check on the actual game? select at least one of the clues they had in their final answer? Does doing that after "make the case" actually work as an attention check? If we do it before "make the case", what does that do to the validity of the subsequent result?

- if a player picks up a clue from a neighbor, and before they drop it the neighbor changes their promising leads, the player may get the wrong clue put in their notebook...

- Q: how do we know that what we're seeing isn't just the human ability to seen
patterns in randomness? how do we know that social contagion matters to the
outcome?

- Q: what columns do we need to include? If we want different parts of the
social network to be able to come to different conclusions, there need to be
different conclusions present in the code. Different people, with different tools,
with different descriptions, who are seen with the stolen object in different places?

- Q: should we highlight the messages in the collaborator's feeds that the player has already categorized?
 A: yes, it helps reduce information overload and makes the game more playable. Highlight the same color for categorization into the 'dead ends' and the 'promising leads' means that coloration isnt just an indicator of who you agree with...

 - Q: how many clues should an individual initially be exposed to?
  A: 20 is too many. 16 sorta works.

- Q: how many tries should participants get to answer the questions correctly? Ie, should we throw out people who don't get it right in the first three attempts? (to discourage random clicking?) (but still pay them for the qualification..)

- Q: What order are the columns presented in? it should be random, but it ccould be in
increasing numeric order, which might induce artifial correlation.

- Q: I put the training out for 3x the number I needed, and emailed them all. How many HITs do I put out?

## checks
- look at participation for all individuals over the course of the simulation


- looking for some individuals to say it was one person, with one set of tools

### Settings

We generated a basic settings file (`/local.json`), which should originally only contain configuration for admin login. More documentation for settings is coming soon.

You can run the app with the settings like this:

```sh
meteor --settings local.json
```
