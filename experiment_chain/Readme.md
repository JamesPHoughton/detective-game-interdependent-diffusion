This folder is a copy of the experiment folder, with a few settings changed to
allow you to run on multiple servers and pass overflow participants to the
next server in the chain.

Changes are in:
- `settings.json` files (one new file for each server)
- `NoBatch_Redirect.jsx` redirects players to the next server in the chain if
the current server is full. Currently set to a four server chain.
- `NoBatch_PayCode.jsx` is the final catchment for people who get redirected
through all servers and there are still no games available.
- `client/main.js` The "chain" servers assume that users have already completed training,
using the `training_server`, and so there are no intro steps here.
