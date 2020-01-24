"""
This design simplifies the multiple different treatment conditions to just two: fully interdependent, and as
close to independent as possible.

This design puts the treatment and control in the same empirica "game", so that individuals are properly randomized
between the treatment and control conditions.

Also explicitly includes which options are presented to players after the game finishes.
"""



import numpy as np
import pandas as pd
import itertools
import copy
import networkx as nx
import random
import string
import json
import yaml
import datetime

root_dir = "games/"


def make_matched_pair(clue_edges, clue_nodes, dont_break):
    n_beliefs = 4


    # make social network
    np.random.seed()
    g = nx.complete_graph(4)
    n_players = nx.number_of_nodes(g)

    neighbors = {}
    player_positions = []
    for n in g:
        neighbors['t' + str(n)] = ['t' + str(nb) for nb in g.neighbors(n)]  # nodes in treatment
        player_positions.append('t' + str(n))
        neighbors['c' + str(n)] = ['c' + str(nb) for nb in g.neighbors(n)]  # nodes in control
        player_positions.append('c' + str(n))

    np.random.shuffle(player_positions)

    # make clues
    core_nodes = {}  # the nodes that are linked directly to the crime scene and stolen object in both conditions
    for col in clue_edges.columns:
        core_nodes[col] = np.random.choice(list(clue_nodes[col].dropna()), 1)[0]

    peripheral_nodes = {}  # the nodes that are used to replace core nodes in the 'rim' edges of the control condition
    for col in clue_nodes.columns:
        col_vals = [s for s in list(clue_nodes[col].dropna()) if s not in list(core_nodes.values())]
        peripheral_nodes[col] = list(np.random.permutation(col_vals))

    treatment_clues = dict()
    control_clues = dict()
    for row_num, (row, series) in enumerate(clue_edges.iterrows()):
        for col_num, (col, edge) in enumerate(series.iteritems()):
            if row_num < col_num and isinstance(edge, str) and edge != "-":
                # treatment clues
                row_node = str(core_nodes[row])  # use the same node each time we hit 'row'
                col_node = str(core_nodes[col])
                clue_content = format_content(edge, col_node, row_node)
                clue_id = "tclue_%i_%i" % (row_num + 1, col_num + 1)
                treatment_clues[clue_id] = {
                    "id": clue_id,
                    "nodeNames": [col, row],
                    "nodes": [col_node, row_node],
                    "edge": edge,
                    "content": clue_content,
                }

                # control clues
                if set([row, col]).intersection(set(dont_break)):  # if in the core, keep
                    row_node = str(core_nodes[row])
                    col_node = str(core_nodes[col])
                else:  # otherwise use dummy ends
                    row_node = str(peripheral_nodes[row].pop())  # each time, take a new node
                    col_node = str(peripheral_nodes[col].pop())  # each time, take a new node
                clue_content = format_content(edge, col_node, row_node)
                clue_id = "cclue_%i_%i" % (row_num + 1, col_num + 1)
                control_clues[clue_id] = {
                    "id": clue_id,
                    "nodeNames": [col, row],
                    "nodes": [col_node, row_node],
                    "edge": edge,
                    "content": clue_content,
                }


    # distribute clues randomly, but make sure that all clues are included
    beliefs_needed = n_players * n_beliefs
    clues_available = len(treatment_clues)

    treatment_clue_list = list(treatment_clues.keys()) + ['tclue_1_2']*(beliefs_needed-clues_available)
    treatment_clue_list = [cl for cl in np.random.permutation(treatment_clue_list)]
    #n_sets = int(np.ceil(n_players * n_beliefs / len(treatment_clues)))  # how many sets of the total clues will we need?
    beliefs = {}
    #treatment_clue_list = [i for _ in range(n_sets) for i in np.random.permutation(list(treatment_clues.keys()))]
    for n in np.random.permutation(list(range(n_players))):
        treatment_player_clue_keys = treatment_clue_list[:n_beliefs]
        treatment_clue_list = treatment_clue_list[n_beliefs:]
        beliefs['t'+str(n)] = treatment_player_clue_keys
        beliefs['c'+str(n)] = ['c'+s[1:] for s in treatment_player_clue_keys]

    clues = {**treatment_clues, **control_clues}  # merge into one clue dict

    choice_nodes = {"suspect": sorted([core_nodes['Suspect 1'],
                                       core_nodes['Suspect 2'],
                                       core_nodes['Suspect 3']]),
                    "clothing": sorted([core_nodes['Clothing 1'], core_nodes['Clothing 2']],
                                       key=lambda x: x.split(" ")[1:]),
                    "appearance": sorted([core_nodes['Appearance 1'], core_nodes['Appearance 2']],
                                         key=lambda x: x.split(" ")[1:]),
                    "tool": sorted([core_nodes['Tool 1'], core_nodes['Tool 2']],
                                   key=lambda x: x.split(" ")[1:]),
                    "vehicle": sorted([core_nodes['Getaway Vehicle 1'], core_nodes['Getaway Vehicle 2']],
                                      key=lambda x: x.split(" ")[1:])
                 }

    return neighbors, clues, beliefs, core_nodes, choice_nodes, player_positions


def format_content(edge, col_node, row_node):
    content = edge.replace('{row}', row_node).replace('{col}', col_node)
    return content[0].upper() + content[1:] + '.'


play_1_min_factor_id = ''.join(random.choices('23456789ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnopqrstuvwxyz', k=17))
playerCount_factor_id = ''.join(random.choices('23456789ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnopqrstuvwxyz', k=17))
duration_factor_id = ''.join(random.choices('23456789ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnopqrstuvwxyz', k=17))
gameSetupId_factor_id = ''.join(random.choices('23456789ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnopqrstuvwxyz', k=17))
experimentDataFile_factor_id = ''.join(random.choices('23456789ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnopqrstuvwxyz', k=17))
playerCount_id = ''.join(random.choices('23456789ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnopqrstuvwxyz', k=17))

default_config = {
    "treatments": [
        #         {
        #             "name": "",
        #             "factorIds": []
        #         }
    ],
    "factorTypes": [
        {
            "_id": playerCount_factor_id,
            "name": "playerCount",
            "description": "The number of players in a given game.",
            "required": "true",
            "type": "Integer",
            "min": 1
        },
        {
            "_id": duration_factor_id,
            "name": "duration",
            "description": "The length of the game in minutes.",
            "required": "true",
            "type": "Integer",
            "min": 0
        },
        {
            "_id": gameSetupId_factor_id,
            "name": "gameSetupId",
            "description": "Which game setup to use for the game.",
            "required": "false",
            "type": "String"
        },
        {
            "_id": experimentDataFile_factor_id,
            "name": "experimentDataFile",
            "description": "which json file to load the experiment data from",
            "required": "false",
            "type": "String"
        }
    ],
    "factors": [
        {
            "_id": playerCount_id,
            "name": "debug4player",
            "value": 4,
            "factorTypeId": playerCount_factor_id
        },
        {
            "_id": play_1_min_factor_id,
            "name": "playOneMin",
            "value": 1,
            "factorTypeId": duration_factor_id
        }
    ],
    "lobbyConfigs": [
        {
            "timeoutType": "lobby",
            "timeoutInSeconds": 1500000,
            "timeoutStrategy": "fail",
            "gameLobbyIds": []
        }
    ],
}


def generate_experiment_data_file():
    """ Args: n_players, deg, n_beliefs, n_concepts, target, replications"""
    n_players = 4  # tetrahedral graph
    deg = 3  # tetrahedral graph
    n_beliefs = 4  # max manageable for cognitive load

    config = copy.deepcopy(default_config)

    clue_filename = "Clues.xlsx"

    concept_order = [
        "Crime Scene", "Stolen Object",
        "Suspect 1", "Suspect 2", "Suspect 3",
        "Clothing 1", "Clothing 2", "Appearance 1", "Appearance 2",
        "Tool 1", "Tool 2", "Getaway Vehicle 1", "Getaway Vehicle 2"
    ]
    use_columns = concept_order

    dont_break = ["Crime Scene", "Stolen Object"]

    clue_nodes = pd.read_excel(clue_filename, sheet_name="Backup Nodes 2")
    clue_nodes.columns = [col.strip() for col in clue_nodes.columns]

    clue_edges = pd.read_excel(clue_filename, sheet_name="Edges")
    clue_edges.set_index("index", inplace=True, drop=True)
    clue_edges.columns = [col.strip() for col in clue_edges.columns]
    clue_edges = clue_edges.loc[pd.notnull(clue_edges.index)]  # drop null rows
    clue_edges = clue_edges[use_columns].loc[use_columns]

    # identify the name of the overall experiment package.
    # experiment_setup_id = 'exp_setup_' +''.join(random.choices(string.ascii_letters + string.digits, k=16))
    experiment_setup_name = 'tiny_pair_game' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    experiment = {'experiment_setup_id': experiment_setup_name,
                  "games": {},
                  "clue_filename": clue_filename,
                  "dont_break": dont_break,
                  "p_broken_list": 'matched inter/indep pair',
                  "n_players": n_players,
                  "deg": deg,
                  "n_beliefs": n_beliefs,
                  "n_concepts": len(use_columns),
                  "replications": 1
                  }


    game_setup_id = 'panel_%i_matched_pair_%s' % (1, experiment_setup_name)
    game_data = {
        'panelId': 'panel_%i_%s' % (1, experiment_setup_name),
        'gameSetupId': game_setup_id,
        "panel": 1,
        "pBroken": "matched pair 0, 1",
        "nPlayers": n_players,
        "rep_number": 1,
        "deg": deg,
        "n_concepts": len(use_columns),
        'experiment': experiment_setup_name,
    }

    (game_data['neighbors'], game_data['clues'],
     game_data['beliefs'], game_data['coreNodes'], game_data['choiceNodes'], game_data['playerPositions']
     ) = make_matched_pair(clue_edges, clue_nodes, dont_break)

    # log it
    experiment["games"][game_setup_id] = game_data

    # add to the config
    game_setup_id = ''.join(random.choices('23456789ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnopqrstuvwxyz', k=17))
    config['factors'].append({
        "_id": game_setup_id,
        "name": "testgame_setup_id",
        "value": game_setup_id,
        "factorTypeId": gameSetupId_factor_id
    })

    # save the experiment file
    experiment_filename = "%s.json" % experiment_setup_name
    with open(root_dir + experiment_filename, 'w') as outfile:
        json.dump(experiment, outfile)

    experimentDataFile_id = ''.join(random.choices('23456789ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnopqrstuvwxyz', k=17))
    config["factors"].append({
        "_id": experimentDataFile_id,
        "name": "testgame_datafile",
        "value": experiment_filename,
        "factorTypeId": experimentDataFile_factor_id
    })

    config['treatments'].append({
        "name": "testGame",
        "factorIds": [game_setup_id, playerCount_id, experimentDataFile_id, play_1_min_factor_id]
    })

    # save an empirica config file for the experiment
    config_filename = root_dir + "%s.yaml" % experiment_setup_name
    with open(config_filename, 'w') as config_file:
        yaml.dump(config, config_file)

    return experiment_filename


generate_experiment_data_file()