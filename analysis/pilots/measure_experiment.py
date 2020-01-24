import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import squareform
import pandas as pd
import json
import multiprocessing
import itertools
import numpy as np
import networkx as nx
from datetime import datetime


def mean_adoptions(game):
    return np.mean([len(game['players'][pid]['data.notebooks']['promising_leads']['clueIDs'])
                    for pid in game['playerIds']])


def measure_interpersonal_similarity(game):
    """Jaccard similarity between each pair of individuals"""
    jaccards = dict()
    # for each pair of agents in the simulation
    for a, b in itertools.combinations(game['playerIds'], r=2):
        # identify the edges of each agent
        a_beliefs = set(game['players'][a]['data.notebooks']['promising_leads']['clueIDs'])
        b_beliefs = set(game['players'][b]['data.notebooks']['promising_leads']['clueIDs'])
        # jaccard similarity is the intersection divided by the union
        intersect = len(a_beliefs.intersection(b_beliefs))
        union = len(a_beliefs.union(b_beliefs))
        jaccards[(a, b)] = intersect / union
    return jaccards


def measure_mean_interpersonal_similarity(jaccards, q, above=True):
    if above:
        # find out what index represents the qth percentile individual
        thresh = int(np.ceil(len(jaccards) * (q / 100)))
        # average over all similarities above the qth percentile
        return np.mean(sorted(list(jaccards.values()))[thresh:])
    else:
        thresh = int(np.floor(len(jaccards) * (q / 100)))
        return np.mean(sorted(list(jaccards.values()))[:thresh])


def measure_social_clusters_hierarchy(jaccards, method='average'):
    distances = 1 - np.array(list(jaccards.values()))
    link = sch.linkage(distances, method=method)
    peaks = np.argwhere(link[:, 3] == 2).flatten()

    if len(peaks) > 1:
        sf = squareform(sch.cophenet(link))
        prominences = []
        for node, height in link[peaks, 1:3]:
            distances = []
            for othernode in link[peaks, 1]:
                if node == othernode:
                    continue
                distance = sf[int(node), int(othernode)]
                distances.append(distance)
            prominences.append(min(distances) - height)
        mean_prominence = np.mean(prominences)
        max_prominence = np.max(prominences)
    else:
        mean_prominence = 0
        max_prominence = 0

    return len(peaks), mean_prominence, max_prominence


def postprocess_game(game):
    res = dict()
    jaccards = measure_interpersonal_similarity(game)
    # mean = measure_mean_interpersonal_similarity(jaccards, 0)
    # res['top10'] = measure_mean_interpersonal_similarity(jaccards, 90)
    # res['bottom10'] = measure_mean_interpersonal_similarity(jaccards, 10, above=False)
    # res['jaccard_variance'] = np.var(list(jaccards.values()))

    (res['num_factions'],
     res['mean_prominence'],
     res['max_prominence']) = measure_social_clusters_hierarchy(jaccards)

    res['mean_adoptions'] = mean_adoptions(game)
    res['p_broken'] = game['gameData']['parameters']['pBroken']
    res['panelId'] = game['gameData']['panelId']

    return res


def retrace(game):
    """
    A generator that returns (player_id, g, event) at each event in the game,

    *player_id* is the player logging the event,
    *g* is the state of the game following the event,
    *event* is what is logged, timestamp modified to be in seconds since game start

    """
    game_data = game['gameData']
    clues = game_data['clues']

    #assert game_data['parameters']['nPlayers'] == len(game['players'].items())
    assert game_data['nPlayers'] == len(game['players'].items()) / 2
    #assert game_data['parameters']['nPlayers'] == len(game['playerIds'])
    assert game_data['nPlayers'] == len(game['playerIds']) /2

    # create trace network
    edge_list = []
    for player_id, player_data in game['players'].items():
        for alter_id in player_data['data.alterIDs']:
            edge_list.append([player_id, alter_id])
    g = nx.from_edgelist(edge_list)

    # give starting information

    nx.set_node_attributes(
        g,
        name='pos',  # M for mind/memory
        values={a: game['players'][a]['data.position'] for a in g}
    )

    nx.set_node_attributes(
        g,
        name='M',  # M for mind/memory
        values={a: nx.from_edgelist([
            clues[bf]['nodes'] for bf in
            #game['players'][a]['data.intialState']['promising_leads']['clueIDs']
            game['players'][a]['data.initialState']['promising_leads']['clueIDs']
        ]) for a in g}
    )


    nx.set_node_attributes(
        g,
        name='F',  # F for forgetory
        values={i: nx.Graph() for i in g}
    )

    # yield the initial state of the experiment
    event = {'at': game['createdAt'],
             't': 0}
    yield (None, g, event)

    # collect the log of the entire experiment
    game_log = pd.DataFrame()
    for player_id, player_data in game['players'].items():
        player_log = pd.DataFrame(player_data['data.log'])
        player_log['player'] = player_id
        game_log = game_log.append(player_log)

    game_log.sort_values('at', inplace=True)

    # trace game
    t_start = datetime.strptime(game['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

    for _, event in game_log[game_log['event'] == "drop"].iterrows():
        player_id = event["player"]
        source = event['data']['source']
        dest = event['data']['dest']
        if 'clue' in event['data']:
            if event['data']['clue'] != None:
                edge = clues[event['data']['clue']]['nodes']
            else:
                print('Missing clueID for player %s from source %s at time %s' % (player_id, source, event['at']))
        else:
            print('player %s is missing a clue' % player_id)
            continue
        M = g.node[player_id]['M']
        F = g.node[player_id]['F']
        update = False

        if source == "promising_leads":
            # check that clue is still in promising leads
            assert g.node[event['player']]['M'].has_edge(*edge)
            if dest == "dead_ends":
                M.remove_edge(*edge)
                F.add_edge(*edge)
                update = True

        elif source == "dead_ends":
            assert g.node[event['player']]['F'].has_edge(*edge)
            if dest == "promising_leads":
                F.remove_edge(*edge)
                M.add_edge(*edge)
                update = True

        else:
            assert source in game['playerIds']  # check that source is another player
            #assert g.node[source]['M'].has_edge(*edge)  # check that clue is in source
            if not g.node[source]['M'].has_edge(*edge):  # check that clue is in source
                print("%s no longer in source %s" % (str(edge), str(source)))
            if dest == "promising_leads":
                M.add_edge(*edge)
                if F.has_edge(*edge):
                    F.remove_edge(*edge)
                update = True
            elif dest == "dead_ends":
                F.add_edge(*edge)
                if M.has_edge(*edge):
                    M.remove_edge(*edge)
                update = True
            assert not (F.has_edge(*edge) and  # not in both memory and forgetery
                        M.has_edge(*edge))

        if update:
            t_current = datetime.strptime(event['at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            event['t'] = (t_current - t_start).total_seconds()
            yield (player_id, g, event)

    # double check the final state
    for player_id in g:
        leads = game['players'][player_id]['data.notebooks']['promising_leads']['clueIDs']
        should_have = set([tuple(sorted(clues[clue]['nodes'])) for clue in leads if clue != None])
        has = set([tuple(sorted(edge)) for edge in g.node[player_id]['M'].edges()])
        assert should_have == has
        # for clue in leads:  # final notebook
        #     edge = clues[clue]['nodes']
        #     assert g.node[player_id]['M'].has_edge(*edge)
        # not_leads = set(clues.keys()) - set(leads)
        # for clue in not_leads:  # final notebook
        #     edge = clues[clue]['nodes']
        #     if g.node[player_id]['M'].has_edge(*edge):
        #         print('failed to drop %s, %s from mind of player %s'%(clue, edge, player_id))

        deads = game['players'][player_id]['data.notebooks']['dead_ends']['clueIDs']
        should_have = set([tuple(sorted(clues[clue]['nodes'])) for clue in deads if clue != None])
        has = set([tuple(sorted(edge)) for edge in g.node[player_id]['F'].edges()])
        assert should_have == has
        # for clue in deads:  # final notebook
        #     edge = clues[clue]['nodes']
        #     assert g.node[player_id]['F'].has_edge(*edge)
        # not_deads = set(clues.keys()) - set(deads)
        # for clue in not_deads:  # final notebook
        #     edge = clues[clue]['nodes']
        #     if g.node[player_id]['F'].has_edge(*edge):
        #         print('failed to remove %s from forgettory of player %s' % (edge, player_id))


def increase_similarity_factors(game, g, event):
    """
    Given the state of the system, what are the factors influencing the likelihood
    of a change in similarity between

    Parameters
    ----------
    game
    g
    event

    Returns
    -------
    list of dictionaries that can be combined into a DataFrame

    """
    # factors that contribute to an increase in similarity between two individuals
    rows = []
    for player_id, alter_id in itertools.combinations(game['players'], r=2):
        row = {
            'player_ids': "%s_%s" % tuple(sorted([player_id, alter_id])),
            'start': event['t'],
        }
        player_edges = set(g.node[player_id]['M'].edges())
        alter_edges = set(g.node[alter_id]['M'].edges())
        intersect = len(player_edges.intersection(alter_edges))
        union = len(player_edges.union(alter_edges))
        row['similarity'] = intersect / union

        rows.append(row)
    return rows


def adopt_factors(game, g, event):
    """
    given the state of the game, what are the factors that lead to adoption?

    Parameters
    ----------
    game
    g
    event

    Returns
    -------
    list of dictionaries that can be combined into a DataFrame
    """

    rows = []
    for player_id, clue_id in itertools.product(game['players'], game['gameData']['clues']):
        edge = game['gameData']['clues'][clue_id]['nodes']
        M = g.node[player_id]['M']

        row = {'player_clue_id': "%s_%s" % (player_id, clue_id),
               'start': event['t']}

        # number of people exposing player to clue
        exposers = [nb for nb in g.neighbors(player_id) if g.node[nb]['M'].has_edge(*edge)]
        row['exposures'] = len(exposers)

        # similarity to exposers
        similarities = []
        for alter_id in exposers:
            player_edges = set(g.node[player_id]['M'].edges())
            alter_edges = set(g.node[alter_id]['M'].edges())
            intersect = len(player_edges.intersection(alter_edges))
            union = len(player_edges.union(alter_edges))
            similarities.append(intersect / union)
        row['similarities'] = tuple(similarities)


        # number of times each end of the clue is present in player's existing beliefs
        row['end_counts'] = tuple([M.degree[end] if M.has_node(end) else 0 for end in edge])

        # count of paths player has connecting ends of clue
        path_list = nx.all_simple_paths(M, *edge, cutoff=4) if all(row['end_counts']) else []
        path_counts = pd.Series(pd.Series([len(pth) - 1 for pth in path_list]).value_counts(),
                                index=range(1, 5)).fillna(0)
        row['have_belief'] = path_counts[1]
        row['pl2'] = path_counts[2]
        row['pl3'] = path_counts[3]
        row['pl4'] = path_counts[4]

        rows.append(row)

    return rows


def analyze_experiment(experiment_filename, player_json_list, game_json_list):
    with open(experiment_filename, 'r') as infile:
        experiment = json.load(infile)

    players = []
    f = player_json_list
    for line in f:
        players.append(json.loads(line))

    games = []
    f = game_json_list
    for line in f:
        games.append(json.loads(line))

    # find the games in the data dump that are associated with this experiment
    experiment_games = [g for g in games if g['gameSetupId'] in experiment['games'].keys()]

    for game in experiment_games:
        game['players'] = {pl['_id']: pl for pl in players if pl['_id'] in game['playerIds']}
        game['gameData'] = experiment['games'][game['gameSetupId']]

    with multiprocessing.Pool() as p:
        res = p.map(postprocess_game, experiment_games)

    res_df = pd.DataFrame(res)
    return res_df
