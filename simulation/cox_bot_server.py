"""
Implements a bot using a cox proportional hazards model trained on player data
"""

from flask import Flask, request
from flask_restful import reqparse, Resource, Api
import numpy as np
import networkx as nx
import itertools
import pandas as pd

app = Flask(__name__)
api = Api(app)

frailty_scale= .9

adoption_hazard_curve = pd.read_csv('../analysis/adopt_hazard.csv', index_col=0)['hazard']
forget_hazard_curve = pd.read_csv('../analysis/forget_hazard.csv', index_col=0)['hazard']
adoption_regressors = pd.read_csv('../analysis/adopt_factors.csv', index_col=0)
forget_regressors = pd.read_csv('../analysis/forget_factors.csv', index_col=0)


exposure_times = {}  # {player1: {clue1: t_exposed, clue2: t_exposed}...}
frailties = {}

# create a map from cluenames to edges
edges = {}
spokes = []
spurlinks = []
for edge in itertools.combinations(range(1,14), r=2):
    edges['tclue_%i_%i'%tuple(sorted(edge))] = edge
    if sorted(edge)[0] <= 2:
        edges['cclue_%i_%i'%tuple(sorted(edge))] = edge
    elif sum(edge)%2 == 1:  # sum is odd
        edges['cclue_%i_%i'%tuple(sorted(edge))] = (edge[0], edge[0]*100+edge[1])
    else:
        edges['cclue_%i_%i'%tuple(sorted(edge))] = (edge[1], edge[1]*100+edge[0])

    if len(set(edge).intersection({1,2})) == 0:
        spurlinks.append('tclue_%i_%i'%tuple(sorted(edge)))
        spurlinks.append('cclue_%i_%i'%tuple(sorted(edge)))
    elif len(set(edge).intersection({1,2})) == 1:
        spokes.append('tclue_%i_%i'%tuple(sorted(edge)))
        spokes.append('cclue_%i_%i'%tuple(sorted(edge)))


def fast_n_triangle_paths(M, edge):
    """ Fast check for triangle closing rule"""
    try:
        from_neighbors = set(M[edge[0]])  # if concept 0 not in network, false
        to_neighbors = set(M[edge[1]])  # if concept 1 not in network, false
        return len(from_neighbors & to_neighbors)  # closes number of existing paths
    except:
        return 0


class NaiveStatelessBot(Resource):

    def post(self):
        data = request.json
        factors = {}

        adopt_fudge = 1.7
        forget_fudge = 6
        M = nx.from_edgelist([edges[k] for k in data['leads']])
        #F = nx.from_edgelist([edges[k] for k in data['deads']])

        if not hasattr(frailties, data['pId']):  # first call from this player
            frailties[data['pId']] = np.random.normal(loc=0, scale=frailty_scale)

        for i, notebook in enumerate(data['exposed'] + [data['leads'], data['deads']]):
            for clueId in notebook:
                nodes = set(edges[clueId])

                # multiple notebooks may explose same clue. Process only the first
                if not hasattr(factors, clueId):  # first encounter amongst visible notebooks
                    factors[clueId] = {
                        'n_exposures': 1 if i<3 else 0,  # three neighbors
                        'n_triangle_paths': fast_n_triangle_paths(M, edges[clueId]),
                        'is_link_or_spur': clueId in spurlinks,
                        'is_spoke': clueId in spokes,
                        'is_in_deads': clueId in data['deads'],
                        'is_in_leads': clueId in data['leads'],
                        'n_rim_connections': sum([v for k,v in M.degree(nodes-{1,2})]),
                        'n_existing_leads': len(data['leads'])
                    }

                    if data['pId'] in exposure_times: # seen player before
                        if clueId in exposure_times[data['pId']]:
                            factors[clueId]['seconds_exposed'] = data['t'] - exposure_times[data['pId']][clueId]
                        else:  # first exposure
                            exposure_times[data['pId']][clueId] = data['t']
                            factors[clueId]['seconds_exposed'] = 0
                    else:
                        exposure_times[data['pId']] = {clueId: data['t']}
                        factors[clueId]['seconds_exposed'] = 0

                else:  # exposed by a second or third neighbor or is in one of self notebooks
                    factors[clueId]['exposures'] = factors[clueId]['exposures'] + 1 if i<3 else factors[clueId]['exposures']  # three neighbors


        factors_df = pd.DataFrame(factors).T
        factors_df["in_startup_period"] = data['t'] <= 30

        try:
            adoption_factors = factors_df[(factors_df['is_in_leads']==0) & (factors_df['n_exposures']>0)]
            adoption_factor_log_impacts = (adoption_factors - adoption_regressors['means'])*adoption_regressors['coef']
            adoption_factor_log_impacts['frailty'] = frailties[data['pId']]
            adoption_hazard_ratios = np.exp((adoption_factor_log_impacts).sum(axis=1))
            adoption_hazards = adoption_factors['seconds_exposed'].apply(
                lambda x: adoption_hazard_curve.loc[int(x)]) * adoption_hazard_ratios
            adoption_hazards *= adopt_fudge
            adoption_flags = np.random.binomial(1, p=adoption_hazards, size=len(adoption_hazards))
            adoptions = list(adoption_factors.index[adoption_flags==1])  # indicated adoptions


            forget_factors = factors_df[(factors_df['is_in_leads']==1)]
            forget_factor_log_impacts = (forget_factors - forget_regressors['means'])*forget_regressors['coef']
            forget_factor_log_impacts['frailty'] = frailties[data['pId']]  # todo: should have a separate forget frailty
            forget_hazard_ratios = np.exp((forget_factor_log_impacts).sum(axis=1))
            forget_hazards = forget_factors['seconds_exposed'].apply(
                lambda x: forget_hazard_curve.loc[int(x)]) * forget_hazard_ratios
            forget_hazards *= forget_fudge
            forget_flags = np.random.binomial(1, p=forget_hazards, size=len(forget_hazards))
            forgets = list(forget_factors.index[forget_flags==1])  # indicated adoptions

            n_actions_possible = len(adoptions+forgets)
            if n_actions_possible > 0: # can only do one per time period...
                act = np.random.choice(["adopt", "forget"], p=[len(adoptions)/n_actions_possible, len(forgets)/n_actions_possible])
                if act == "adopt":
                    choice = np.random.choice(adoptions)
                    dest = "promising_leads"
                    index = 0 #np.random.randint(len(data['leads']))
                else:
                    choice = np.random.choice(forgets)
                    dest = "dead_ends"
                    index = 0 #np.random.randint(len(data['deads']))
            else:
                choice = "wait"
                dest = "na"
                index = "na"

            response = {
                "drag": choice != "wait",
                "clueId": choice,
                "dest": dest,
                "index": index,
            }

            return response, 200

        except ValueError:
            print('\n\n')
            print(adoption_factors)
            print('\n')
            print(adoption_hazards)
            print('\n')
            print(forget_hazards)
            print('\n')
            raise


api.add_resource(NaiveStatelessBot, '/')

if __name__ == '__main__':
    app.run(debug=False)
