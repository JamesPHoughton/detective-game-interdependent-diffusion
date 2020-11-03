This is a copy of `experiment` which is used with `experiment_chain` to allow
multiple servers to be used. Players first come here and train, and upon completion
of training are redirected to the first game server in the chain.

The changes to make this happen are in `Round_Redirect.jsx` and `client/main.js`
