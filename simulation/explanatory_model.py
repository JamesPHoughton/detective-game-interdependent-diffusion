# %% codecell
%pylab inline
import networkx as nx
import json

# %% codecell
experiment_filename = 'setup/games/exp_design6_matched_20200319_134546.json'

# %% codecell
with open(experiment_filename, 'r') as infile:
        experiment = json.load(infile)

# %% codecell
experiment['games']['panel_0_matched_pair_exp_design6_matched_20200319_134546'].keys()


# %% codecell
def setup_game(game_data):
        # set up agents
        g = nx.from_dict_of_lists(game_data['neighbors'])

        # give starting information
        nx.set_node_attributes(
            g,
            name='M',  # M for mind/memory
            values={i: nx.from_edgelist([game_data['clues'][bf]['nodes'] for bf in game_data['beliefs'][str(i)]])
                    for i in g}
        )

        nx.set_node_attributes(
            g,
            name='F',  # F for forgetory
            values={i: nx.Graph() for i in g}
        )

        ### this stuff is just for generating data that mirrors the experiment
        # save initial state
        nx.set_node_attributes(
            g,
            name="initialState",
            values={i: {"promising_leads": {"clueIDs": game_data['beliefs'][str(i)]},
                        "dead_ends": {"clueIDs": []}
                        }
                    for i in g}
        )

        # assign random identifiers
        nx.set_node_attributes(
            g,
            name="_id",
            values={i: ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                    for i in g}
        )

        # initialize logs
        nx.set_node_attributes(
            g,
            name='data.log',  # M for mind
            values={i: list() for i in g}
        )

        return g

    def adopt(g, ego, edge, t, target):

        if g.node[ego]['M'].has_edge(*edge):
            return False

        M = g.node[ego]['M']

        exposers = [nb for nb in g[ego] if edge in g.node[nb]['M'].edges()]
        exposure = len(exposers)
        if exposure == 0:
            return False

        ends_present = len(set(edge).intersection(set(M.nodes())))

        if M.has_node(edge[0]) and M.has_node(edge[1]):
            #path_list = nx.all_simple_paths(M, *edge, cutoff=4)
            path_list = nx.all_simple_paths(M, *edge, cutoff=2)
        else:
            path_list = []

        path_counts = {i: 0 for i in range(6)}
        for path in path_list:
            path_counts[len(path)] += 1

        n_beliefs = len(M.edges())

        baseline = .01 / (100)
        c_exposure = np.log(3)  # for each exposure multiply the likelihood by 1.5
        c_ends_present = np.log(5)
        c_len2paths = np.log(10)
        c_len3paths = np.log(3)
        c_len4paths = np.log(2)
        c_offtarget = np.log(.6)

        likelihood = baseline * np.exp(
             c_exposure * exposure +
            c_ends_present * ends_present +
            c_len2paths * path_counts[2] +
            c_len3paths * path_counts[3] +
            c_len4paths * path_counts[4] +
            c_offtarget * np.sign(n_beliefs - target)*(n_beliefs-target)**2
        )

        #adoption = path_counts[2] > 0

        adoption = np.random.binomial(1, np.min([likelihood, .9999])) == 1

        if adoption:
            source = g.node[np.random.choice(exposers)]["_id"]
            g.node[ego]['data.log'].append({
                "event": "drop",
                "data": {
                    "clue": lookup_cluename(edge),
                    "source": source,
                    "dest": "promising_leads",
                    "destIndex": 0
                },
                "at": t  # str(datetime.datetime.now()) # t + np.random.rand()  # unique timestamp within the second
            })

        return adoption

    def forget(g, ego, edge, t, target):
        if not g.node[ego]['M'].has_edge(*edge):
            return False

        M = g.node[ego]['M']

        exposers = [nb for nb in g[ego] if edge in g.node[nb]['M'].edges()]
        exposure = len(exposers)
        if exposure == 0:
            return False

        ends_present = len(set(edge).intersection(set(M.nodes())))

        if M.has_node(edge[0]) and M.has_node(edge[1]):
            path_list = nx.all_simple_paths(M, *edge, cutoff=4)
        else:
            path_list = []

        path_counts = {i: 0 for i in range(6)}
        for path in path_list:
            path_counts[len(path)] += 1

        # path_counts = pd.Series(pd.Series([len(pth) - 1 for pth in path_list]).value_counts(),
        #                         index=range(2, 5)).fillna(0)

        n_beliefs = len(M.edges())

        baseline = 10 / 100
        c_exposure = np.log(1/3)  # for each exposure multiply the likelihood by 1.5
        c_ends_present = np.log(1/5)
        c_len2paths = np.log(1/10)
        c_len3paths = np.log(1/3)
        c_len4paths = np.log(1/2)
        c_offtarget = np.log(1/.6)

        likelihood = baseline * np.exp(
            c_exposure * exposure +
            c_ends_present * ends_present +
            c_len2paths * path_counts[2] +
            c_len3paths * path_counts[3] +
            c_len4paths * path_counts[4] +
            c_offtarget * np.sign(n_beliefs - target)*(n_beliefs-target)**2
        )

        forgetion = np.random.binomial(1, np.min([likelihood, .99])) == 1

        if forgetion:
            g.node[ego]['data.log'].append({
                "event": "drop",
                "data": {
                    "clue": lookup_cluename(edge),
                    "source": "promising_leads",
                    "dest": "dead_ends",
                    "destIndex": 0
                },
                "at": t  # + np.random.rand()  # unique timestamp within the second
            })

        return forgetion

    target = game_data['parameters']['target']
    g = setup_game(game_data)

    # useful helper functions
    beliefs = [cl["nodes"] for _, cl in game_data["clues"].items()]
    hashtable = {hash(tuple(sorted(clue["nodes"]))): key for key, clue in game_data["clues"].items()}

    def lookup_cluename(edge):
        return hashtable[hash(tuple(sorted(edge)))]

    # play the game
    for step in range(n_steps):
        substep = 0
        for ego in np.random.permutation(g):  # select ego in random order
            for edge in np.random.permutation(beliefs):  # select a belief in random order to propagate
                substep += .000001  # ensure proper ordering
                if adopt(g, ego, edge, step + substep, target):
                    g.node[ego]['M'].add_edges_from([edge])
                    if g.node[ego]['F'].has_edge(*edge):
                        g.node[ego]['F'].remove_edges_from([edge])
                substep += .000001  # so you can't have a forget event at the same time as an adopt event
                if forget(g, ego, edge, step + substep, target):
                    g.node[ego]['M'].remove_edges_from([edge])
                    g.node[ego]['F'].add_edges_from([edge])

    # save to json for postprocessing (keep as string here)
    player_json = []
    for n in g:
        player_object = {
            "_id": str(g.node[n]["_id"]),
            "initialState": g.node[n]["initialState"],
            "log": g.node[n]["log"],
            "alterIDs": [g.node[nb]["_id"] for nb in g.neighbors(n)],
            "notebooks": {
                "promising_leads": {"clueIDs": [lookup_cluename(edge) for edge in g.node[n]['M'].edges()]},
                "dead_ends": {"clueIDs": [lookup_cluename(edge) for edge in g.node[n]['F'].edges()]}
            }
        }
        json_string = json.dumps(player_object)
        player_json.append(json_string)

    game_object = {"_id": ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
                   "playerIds": [g.node[n]['_id'] for n in g],
                   "treatmentId": treatment_id,
                   "gameSetupId": game_data["gameSetupId"],
                   "createdAt": 0,
                   "finishedAt": n_steps}

    game_json = [json.dumps(game_object)]

    return game_json, player_json
