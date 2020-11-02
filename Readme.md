# Interdependent Diffusion: The social contagion of interacting beliefs

This repository contains code for running and analyzing the Detective Game
experiment, which forms a part of ongoing research into the effect of
interdependence between diffusants on the outcomes of social contagion.

- `setup` contains the code used to design the experiment's parameters and
content

- `simulation` contains code that simulates the experiment with agents

- `results-anonymized` contains the anonymized outcomes of the experiment, along
with processed results

- `analysis` contains code that transforms the raw experiment data dump into
the actual outcomes of the experiment that we care about

- `experiment` contains the actual Empirica project that serves the experiment
to participants.

- `experiment-chain` and `training_server` split `experiment` into code that
can run on a training server, and then a chain of game servers, in order to run
4 simultaneous blocks of games, without overloading servers. It is a substitute
to the code in `experiment` if you are doing lots of games at once, otherwise
is not used.

# Preregistration

The experiment described in this repository was preregistered at https://osf.io/239ns
