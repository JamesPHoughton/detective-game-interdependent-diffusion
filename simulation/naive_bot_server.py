from flask import Flask, request
from flask_restful import reqparse, Resource, Api
import numpy as np
import networkx as nx
import itertools

app = Flask(__name__)
api = Api(app)

# parser = reqparse.RequestParser()
# parser.add_argument('data')

# create a map from cluenames to edges
edges = {}
for edge in itertools.combinations(range(1,14), r=2):
    edges['tclue_%i_%i'%tuple(sorted(edge))] = edge
    if sorted(edge)[0] <= 2:
        edges['cclue_%i_%i'%tuple(sorted(edge))] = edge
    elif sum(edge)%2 == 1:  # sum is odd
        edges['cclue_%i_%i'%tuple(sorted(edge))] = (edge[0], edge[0]*100+edge[1])
    else:
        edges['cclue_%i_%i'%tuple(sorted(edge))] = (edge[1], edge[1]*100+edge[0])



def fast_n_triangle_paths(M, edge):
    """ Fast check for triangle closing rule"""
    try:
        from_neighbors = set(M[edge[0]])  # if concept 0 not in network, false
        if edge[1] in from_neighbors:  # edge already exists
            return -1
        to_neighbors = set(M[edge[1]])  # if concept 1 not in network, false
        return len(from_neighbors & to_neighbors)  # closes number of existing paths
    except:
        return 0


class NaiveStatelessBot(Resource):

    def post(self):
        data = request.json

        likelihoods = {k:0 for k,v in edges.items()}
        likelihoods['wait'] = 20

        M = nx.from_edgelist([edges[k] for k in data['leads']])

        for neighbor_notebook in data['exposed']:
            for clueId in neighbor_notebook:
                if likelihoods[clueId] == 0:  # first exposure
                    triangle_paths = fast_n_triangle_paths(M, edges[clueId])
                    if triangle_paths > 0:
                        likelihoods[clueId] += .07 * triangle_paths

                    familiarity = sum([v for k,v in M.degree(edges[clueId])])
                    likelihoods[clueId] += .01 * familiarity

                likelihoods[clueId] += .01  # for each exposure


        ps = np.array(list(likelihoods.values()))/np.array(list(likelihoods.values())).sum()
        choice = np.random.choice(list(likelihoods), p=ps)

        response = {
            "drag": choice != "wait",
            "clueId": choice,
            "dest": "promising_leads",
            "index": np.random.randint(len(data['leads'])),
        }
        #print(data)
        #print(",", end="")
        return response, 200


api.add_resource(NaiveStatelessBot, '/')

if __name__ == '__main__':
    app.run(debug=False)
