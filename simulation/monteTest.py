import networkx as nx
import numpy as np
import itertools
import pandas as pd
import copy
from sklearn.decomposition import PCA
from scipy import stats
import multiprocessing

def model_7(args): #a=250, triangle_sensitivity=0.5, familiarity_sensitivity=.975):
    """
    a: a parameter for beta distribution from which base hazards are drawn
    """
    # locally scope all the functions so that in subsequent iterations we can't accidentally
    # use an old version by mistake
    a, triangle_sensitivity, familiarity_sensitivity = args



    def susceptible(g, agent, belief):
        """Assess whether an agent is susceptible to a given belief"""
############ Changes ############
        q = g.nodes[agent]['q'] # probability of not getting adopted
        try:
            if nx.shortest_path_length(g.nodes[agent]['M'], *belief) <= 2:
                q *= triangle_sensitivity
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            # no path exists between the nodes
            pass

        familiarity = sum([v for k,v in g.nodes[agent]['M'].degree(belief)])
        q *= familiarity_sensitivity**familiarity

        adopt =  np.random.binomial(1, p=1-q) == 1
#################
        return adopt


    def adopt(g, agent, belief):
        """Assess whether an agent will adopt a given belief"""
        suscep = susceptible(g, agent, belief)
        exposed = any([belief in g.nodes[nbr]['M'].edges() for nbr in g[agent]])
        return suscep and exposed  # both susceptibility and exposure required to adopt


    def simulate(g, n_steps=10, measure_times=[0,10]):
        """
        Conduct a single run of the simulation with a given network

        g: population network
        measure: "last" or "all"

        """
        # capture a list of all the beliefs in the population
        beliefs = np.unique([tuple(sorted(belief)) for agent in g for belief in g.nodes[agent]['M'].edges()], axis=0)

        m = []  # array to collect measurements at each time step
        ts = []
        for step in range(n_steps):  # perform the simulation
            if step in measure_times:
                m.append(measure(g, beliefs))
                ts.append(step)

            for ego in np.random.permutation(g):  # cycle through agents in random order
                for edge in np.random.permutation(beliefs):  # cycle through all possible beliefs in random order
                    if adopt(g, ego, edge):  # check whether the selected agent adopts the selected belief
                        g.nodes[ego]['M'].add_edges_from([edge])  # add the belief to the agent's semantic network

        if step+1 in measure_times:
            m.append(measure(g, beliefs))
            ts.append(step+1)

        df = pd.DataFrame(m, index=ts)
        return df


    def measure(g, beliefs):
        """Take measurements of the state of the system (for creating figures)"""
#################CHANGES###############
        #measure a specific subset of beliefs
        beliefs = [(0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12)]
########################################

        res = {}  # dictionary to collect measurements

        # build a matrix of who (rows) is susceptible to what beliefs (columns)
        suscep = pd.DataFrame(index=g.nodes(), columns=[tuple(b) for b in beliefs])
        for agent in g:
            for belief in suscep.columns:
                suscep.at[agent, belief] = susceptible(g, agent, belief)
        res['% susceptible'] = suscep.mean().mean()  # average susceptible fraction across all beliefs

        # build a matrix of who (rows) holds what beliefs (columns)
        adopt = pd.DataFrame(index=g.nodes(), columns=[tuple(b) for b in beliefs])
        for agent in g:
            for belief in adopt.columns:
                adopt.at[agent, belief] = g.nodes[agent]['M'].has_edge(*belief)
        res['% adopted'] = adopt.mean().mean()  # average adopting fraction across all beliefs

        n_agents = len(adopt.index)
        corrs = adopt.astype(float).T.corr().mask(np.tri(n_agents, n_agents, 0, dtype='bool')).stack()
        res['95% similarity'] = np.percentile(corrs, 95)
        res['5% similarity'] = np.percentile(corrs, 5)
        res['90% similarity'] = np.percentile(corrs, 90)
        res['10% similarity'] = np.percentile(corrs, 10)
        res['85% similarity'] = np.percentile(corrs, 85)
        res['15% similarity'] = np.percentile(corrs, 15)
        res['80% similarity'] = np.percentile(corrs, 80)
        res['20% similarity'] = np.percentile(corrs, 20)
        res['75% similarity'] = np.percentile(corrs, 75)
        res['25% similarity'] = np.percentile(corrs, 25)
        res['std similarity'] = np.std(corrs)

        pca = PCA(n_components=1)
        pca.fit(adopt)
        res['PC1 percent of variance'] = pca.explained_variance_ratio_[0] * 100

###### Changes
        # Measure difference from expected value
        e95 = []
        e5 = []
        e10 = []
        e15 = []
        e20 = []
        e25 = []
        e75 = []
        e80 = []
        e85 = []
        e90 = []
        estd = []
        ePC1 = []
        for _ in range(100):
            shuffle_adopt = pd.DataFrame()
            for col in adopt.columns:
                shuffle_adopt[col] = np.random.permutation(adopt[col].values)

            n_agents = len(shuffle_adopt.index)
            corrs = shuffle_adopt.astype(float).T.corr().mask(np.tri(n_agents, n_agents, 0, dtype='bool')).stack()
            e95.append(np.percentile(corrs, 95))
            e5.append(np.percentile(corrs, 5))

            e10.append(np.percentile(corrs, 10))
            e15.append(np.percentile(corrs, 15))
            e20.append(np.percentile(corrs, 20))
            e25.append(np.percentile(corrs, 25))
            e75.append(np.percentile(corrs, 75))
            e80.append(np.percentile(corrs, 80))
            e85.append(np.percentile(corrs, 85))
            e90.append(np.percentile(corrs, 90))
            estd.append(np.std(corrs))

            pca = PCA(n_components=1)
            pca.fit(shuffle_adopt)
            ePC1.append(pca.explained_variance_ratio_[0] * 100)

        res['expected PC1 percent of variance'] = np.mean(ePC1)
        res['expected 95% similarity'] = np.mean(e95)
        res['expected 5% similarity'] = np.mean(e5)

        res['expected 10% similarity'] = np.mean(e10)
        res['expected 15% similarity'] = np.mean(e15)
        res['expected 20% similarity'] = np.mean(e20)
        res['expected 25% similarity'] = np.mean(e25)
        res['expected 75% similarity'] = np.mean(e75)
        res['expected 80% similarity'] = np.mean(e80)
        res['expected 85% similarity'] = np.mean(e85)
        res['expected 90% similarity'] = np.mean(e90)
        res['expected std similarity'] = np.mean(estd)

        res['net PC1 percent of variance'] = res['PC1 percent of variance'] - res['expected PC1 percent of variance']
        res['net 95% similarity'] = res['95% similarity'] - res['expected 95% similarity']
        res['net 5% similarity'] = res['5% similarity'] - res['expected 5% similarity']

        res['net 10% similarity'] = res['10% similarity'] - res['expected 10% similarity']
        res['net 15% similarity'] = res['15% similarity'] - res['expected 15% similarity']
        res['net 20% similarity'] = res['20% similarity'] - res['expected 20% similarity']
        res['net 25% similarity'] = res['25% similarity'] - res['expected 25% similarity']
        res['net 75% similarity'] = res['75% similarity'] - res['expected 75% similarity']
        res['net 80% similarity'] = res['90% similarity'] - res['expected 80% similarity']
        res['net 85% similarity'] = res['85% similarity'] - res['expected 85% similarity']
        res['net 90% similarity'] = res['90% similarity'] - res['expected 90% similarity']
        res['net std similarity'] = res['std similarity'] - res['expected std similarity']
#########
        return res


    def random_connected_graph(n_agents, deg):
        # create a random connected social network g
        connected = False
        while not connected:
            g = nx.gnm_random_graph(n=n_agents, m=int(n_agents * deg / 2))
            connected = nx.is_connected(g)

        return g


    def run_pair(g0, belief_assignments, beliefs, n_steps=10):
        t_match_susceptibility = n_steps  # the model time step at which the interdependent susceptibility will be matched

        # Interdependent simulation
        # -------------------------
        g1 = copy.deepcopy(g0)  # create copy, to preserve initial conditions for other case
        nx.set_node_attributes(g1, name='M', values=copy.deepcopy(belief_assignments))
        nx.set_node_attributes(g1, name='q', values={n: np.random.beta(a, 5) for n in g1.nodes()})  # mean: .9804, std:.0087
        res1 = simulate(g1, n_steps)

        # Independent simulation
        # ----------------------
        g2 = copy.deepcopy(g0)  # copy from original starting conditions
        nx.set_node_attributes(g2, name='M', values=copy.deepcopy(belief_assignments))
        nx.set_node_attributes(g2, name='q', values={n: np.random.beta(a, 5) for n in g2.nodes()})  # mean: .9804, std:.0087


######Changes
        core_edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12)]
        i = 13
        control_edges = copy.deepcopy(core_edges)
        for n in range (2, 13):
            for s in range(5):
                control_edges.append((n,i))
                i += 1

        control_beliefs = nx.from_edgelist(control_edges)
        core_network = nx.from_edgelist(core_edges)

        for agent in g2:
            new_edges = []
            for edge in g2.nodes[agent]['M'].edges():
                if control_beliefs.has_edge(*edge):
                    new_edges.append(edge)
                else:
                    end = np.random.choice(edge)
                    options = [ne for ne in control_beliefs.edges(end) if not core_network.has_edge(*ne)]
                    new_edges.append(options[np.random.randint(len(options))])

            g2.nodes[agent]['M'] = nx.from_edgelist(new_edges)
########
        res2 = simulate(g2, n_steps)  # perform simulation

        return pd.merge(res1, res2, left_index=True, right_index=True,
                        suffixes=(' (inter)', ' (indep)'))  # format as single pandas DataFrame

    try:
        # Parameters
        # ----------
        g0 = nx.dodecahedral_graph()
        n_concepts = 13  # How many nodes are in the complete semantic network that beliefs are drawn from
    ####### Changes
        n_beliefs = 4
    #######
        beliefs = nx.complete_graph(n_concepts)
        belief_assignments = {agent: nx.gnm_random_graph(n_concepts, n_beliefs) for agent in g0}

        # dodecahedral graph
        res = run_pair(g0, belief_assignments, beliefs)
        res.columns = [col + ' (dodec)' for col in res.columns]

        # Connected Caveman
        caveman_edgelist = [(0,1), (0,2), (0,3),
                (1,2), (1,3),
                (2,7),
                (4,5), (4,6), (4,7),
                (5,6), (5,7),
                (6,11),
                (8,9), (8,10), (8,11),
                (9,10), (9,11),
                (10,15),
                (12,13), (12,14), (12,15),
                (13,14), (13,15),
                (14,19),
                (16,17), (16,18), (16,19),
                (17,18), (17,19),
                (18,3)]
        g0c = nx.from_edgelist(caveman_edgelist)
        resc = run_pair(g0c, belief_assignments, beliefs)
        resc.columns = [col + ' (caveman)' for col in resc.columns]

        # cube/ladder
        linear_edgelist = [(0,1), (1,2), (2,3), (3,0),
                    (0,4), (1,5), (2,6), (3,7),
                    (4,5), (5,6), (4,7),
                    (6,8), (7,9), (8,9),
                    (8,10), (9,11), (10,11),
                    (10,12), (11,13),
                    (12,14), (14,15), (15,13),
                    (12,16), (14,17), (15,18), (13,19),
                    (16,19), (16,17), (17,18), (18,19)
        ]
        g0l = nx.from_edgelist(linear_edgelist)
        resl = run_pair(g0l, belief_assignments, beliefs)
        resl.columns = [col + ' (linear)' for col in resl.columns]

        return pd.concat((res, resc, resl), axis=1)

    except:
        return None


argslist = [(np.random.normal(loc=250, scale=50),  # a
           np.random.beta(4,4),  # "triangle_sensitivity":
           np.random.beta(250, 5)  # "familiarity_sensitivity"
          ) for _ in range(1000)]

rand_key = np.random.randint(100000)

for i in range(100000):
    print(i, end=', ')
    with multiprocessing.Pool() as pool:
        res = pool.map(model_7, argslist)

    runs7 = pd.concat(res, axis=0)
    runs7.to_csv('experiment_monte_carlo_%i_%s.csv' % (rand_key, str(i).zfill(4)))
