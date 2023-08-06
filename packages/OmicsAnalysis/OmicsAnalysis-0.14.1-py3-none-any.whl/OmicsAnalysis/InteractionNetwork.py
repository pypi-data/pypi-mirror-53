import pandas as pd
import numpy as np
from OmicsAnalysis.PyLouvain import PyLouvain, in_order
from scipy.linalg import expm
from scipy.sparse import csgraph
import networkx as nx
import warnings
import copy
from sklearn.cluster import AgglomerativeClustering
from collections import Counter
import random
from networkx import to_dict_of_lists
import matplotlib.pyplot as plt


# TODO: test class and all functions
# complete the class specific functions in Directed and undirected networks
# create a graph sampler that can be used for representation learning

class Graph:
    '''
        Builds a graph from _path.
        _path: a path to a file containing "node_from node_to" edges (one per line)
    '''

    @classmethod
    def from_file(cls, path, colnames, sep=',', header=0, column_index=None, keeplargestcomponent=False):
        network_df = pd.read_csv(path, sep=sep, header=header, low_memory=False, index_col=column_index)

        return cls(network_df, colnames=colnames, keeplargestcomponent=keeplargestcomponent)

    def __init__(self, interaction_df, colnames=None, verbose=True, keeplargestcomponent=False):
        '''
        :param: interaction_df a pandas edgelist consisting of (at least two) columns,
        indicating the two nodes for each edge
        :param: colnames, the names of the columns that contain the nodes and optionally some edge attributes.
        The first two columns must indicate the nodes from the edgelsist
        '''
        self.attr_names = None

        if colnames is not None:
            interaction_df = interaction_df[list(colnames)]
            if len(colnames) > 2:
                self.attr_names = colnames[2:]  # TODO this needs to be done better
        elif interaction_df.shape[1] == 2:
            interaction_df = interaction_df
        else:
            print('Continuing with %s and %s as columns for the nodes' % (interaction_df.columns.values[0],
                                                                          interaction_df.columns.values[1]))

        interaction_df = interaction_df.drop_duplicates()
        self.interactions = interaction_df
        old_col_names = list(self.interactions.columns)
        self.interactions.rename(columns={old_col_names[0]: 'Gene_A', old_col_names[1]: 'Gene_B'}, inplace=True)
        self.interactions = self.interactions.loc[self.interactions.Gene_A != self.interactions.Gene_B]

        self.node_names = pd.unique(self.interactions[['Gene_A', 'Gene_B']].values.flatten()).astype('str')
        self.N_nodes = len(self.node_names)

        self.gene2int = {self.node_names[i]: i for i in range(self.N_nodes)}
        self.int2gene = {v: k for k, v in self.gene2int.items()}

        self.interactions = self.interactions.applymap(lambda x: self.gene2int[x])
        self.nodes = [int(self.gene2int[s]) for s in self.node_names]

        if keeplargestcomponent:
            self.keepLargestComponent(verbose=verbose, inplace=True)

        if verbose:
            print('%d Nodes and %d interactions' % (len(self.nodes), self.interactions.shape[0]))

    def deepcopy(self):
        return copy.deepcopy(self)

    def getInteractionNamed(self):
        return self.interactions.applymap(lambda x: self.int2gene[x])

    def setEqual(self, network):
        '''
        Convenience function for setting the attributes of a network equal to another network
        '''
        self.interactions = network.interactions
        self.node_names = network.node_names
        self.N_nodes = network.N_nodes
        self.nodes = network.nodes

        self.gene2int = network.gene2int
        self.int2gene = network.int2gene
        self.attr_names = network.attr_names

    def mapNodeNames(self, map_dict):
        if len(set(self.node_names).difference(set(list(map_dict.keys())))) > 0:
            warnings.warn('The provided mapping does not convert all ids, for these nodes, old IDs will be kept.')
        self.node_names = [map_dict[x] if x in map_dict.keys() else x for x in self.node_names]
        self.gene2int = dict((map_dict[key], value) if key in map_dict.keys() else (key, value)
                             for (key, value) in self.gene2int.items())

        self.int2gene = {v: k for k, v in self.gene2int.items()}

    def subsetNetwork(self, nodes, inplace=True):
        nodes = set(nodes)
        df = self.getInteractionNamed()
        df = df.loc[df.Gene_A.isin(nodes) &
                    df.Gene_B.isin(nodes)]

        return df
    '''
        merge networks
    '''

    def mergeNetworks(self, network):
        pass

    def mergedf(self, interaction_df, colnames=None):
        pass

    '''
        get adjacency matrix
    '''

    def getAdjMatrix(self, sort='first', as_df=False):

        row_ids = list(self.interactions['Gene_A'])
        col_ids = list(self.interactions['Gene_B'])

        A = np.zeros((self.N_nodes, self.N_nodes), dtype=np.uint8)
        A[(row_ids, col_ids)] = 1

        if as_df:
            return pd.DataFrame(A, index=self.node_names, columns=self.node_names)
        else:
            return A, np.array(self.node_names)

    '''
        perform kernel diffusion
    '''

    def diffuse(self, kernel='LEX', alpha=0.01, as_df=True, scale=True):
        A, nodes = self.getAdjMatrix()
        A = A.astype(np.float)

        if kernel.upper() == 'LEX':   # TODO insert other diffusion techniques
            A = np.diag(np.sum(A, axis=0)) - A
            # for undirected graphs the axis does not matter, for directed graphs use the in-degree
            A = expm(-alpha*A)

        if scale:
            A = A / np.outer(np.sqrt(np.diag(A)), np.sqrt(np.diag(A)))

        if as_df:
            df = pd.DataFrame(A, index=nodes, columns=nodes)
            return df
        else:
            return A, nodes

    '''
        check interactions given a list
        find all interactions between the genes in a list
    '''

    def checkInteraction_list(self, gene_list, attribute_separator=None):

        if attribute_separator is not None:
            gene_list = [s.split(attribute_separator)[0] for s in gene_list]

        df = self.getInteractionNamed()
        interactions_df = df.loc[df.Gene_A.isin(gene_list) &
                                 df.Gene_B.isin(gene_list)]
        return Graph(interactions_df)

    '''
        Get shortest path distance
    '''
    def getGeodesicDistance(self, start_genes, stop_genes):
        pass

    def getAdjDict(self):
        pass

    def getNOrderNeighbors(self, order=2, include_lower_order=True):

        adj_dict = copy.deepcopy(self.getAdjDict())

        for _ in range(order-1):
            adj_dict = getSecondOrderNeighbors(adj_dict, adj_dict0=self.getAdjDict(),
                                               incl_first_order=include_lower_order)
        return adj_dict

    def getDegreeDF(self, return_names=True):
        v, c = np.unique(self.interactions.values.flatten(), return_counts=True)
        if return_names:
            return pd.DataFrame({'Gene': [self.int2gene[i] for i in v],
                                 'Count': c}).sort_values(by='Count', ascending=False, inplace=False)
        else:
            return pd.DataFrame({'Gene': v,
                                 'Count': c}).sort_values(by='Count', ascending=False, inplace=False)

    def removeNodes(self, nodes_tbr, inplace=False):
        nodes_tbr = [self.gene2int[s] for s in nodes_tbr if s in self.gene2int.keys()]
        nodes_tbr = set(nodes_tbr)

        if inplace:
            self.interactions = self.interactions.loc[~(self.interactions.Gene_A.isin(nodes_tbr) |
                                                        self.interactions.Gene_B.isin(nodes_tbr))]
            self.N_nodes = len(self.nodes)

        else:
            new_df = self.interactions.loc[~(self.interactions.Gene_A.isin(nodes_tbr) |
                                             self.interactions.Gene_B.isin(nodes_tbr))]
            new_df = new_df.applymap(lambda x: self.int2gene[x])

            return new_df

    def filterDatasetGenes(self, omicsdatasets, remove_leaves=False, inplace=True):
        '''
        :param: omicsdatasets: datasets that are to be filtered
        :params: should the leaves of the network also be removed?
        :return: the filtered datasets whose genes are all on the network
        '''

        try:
            _ = len(omicsdatasets)

        except TypeError:  # convert to iterable
            omicsdatasets = [omicsdatasets]
            print('converted to iterable')

        if inplace:
            network_genes = set(self.node_names)
            nodes_in_datasets = set()

            for dataset in omicsdatasets:
                intersecting_genes = network_genes.intersection(dataset.genes(as_set=True))

                print('%s: %i genes found on the network.' % (dataset.type, len(intersecting_genes)))
                dataset.subsetGenes(list(intersecting_genes), inplace=True)

                network_genes = nodes_in_datasets.union(network_genes)
                nodes_in_datasets = nodes_in_datasets.union(dataset.genes(as_set=True))

            if remove_leaves:
                self.pruneNetwork(exception_list=nodes_in_datasets, inplace=True)

        else:
            network_genes = set(self.node_names)
            nodes_in_datasets = set()

            datasets_new = []

            for dataset in omicsdatasets:
                intersecting_genes = network_genes.intersection(dataset.genes(as_set=True))

                print('%s: %i genes found on the network.' % (dataset.type, len(intersecting_genes)))
                datasets_new += [dataset.subsetGenes(list(intersecting_genes), inplace=False)]

                network_genes = nodes_in_datasets.union(network_genes)
                nodes_in_datasets = nodes_in_datasets.union(dataset.genes(as_set=True))

            if remove_leaves:
                network = self.pruneNetwork(exception_list=nodes_in_datasets, inplace=False)

            return network, datasets_new

    def filterDataset(self, dataset, remove_leaves=False, inplace=False):

        keeps = list(set(self.node_names).intersection(dataset.genes(as_set=True)))

        if inplace:
            dataset.subsetGenes(keeps, inplace=True)

            if remove_leaves:
                self.pruneNetwork(exception_list=keeps, inplace=True)

        else:
            dataset = dataset.subsetGenes(keeps, inplace=False)
            net = self.deepcopy()
            if remove_leaves:
                net = net.pruneNetwork(exception_list=keeps, inplace=False)

            return net, dataset

    def pruneNetwork(self, exception_list={}, inplace=False):
        '''
        Iteratively prunes the network such that leaves of the network are removed
        '''
        if inplace:
            net = self
        else:
            net = self.deepcopy()

        degreedf = net.getDegreeDF()
        leaves = set(degreedf.Gene[degreedf.Count < 2])
        tbr = leaves.difference(set(exception_list))

        while len(tbr) > 0:

            net.removeNodes(tbr, inplace=True)
            degreedf = net.getDegreeDF()

            leaves = set(degreedf.Gene[degreedf.Count < 2])
            tbr = leaves.difference(exception_list)

        if not inplace:
            return net

    def getComponents(self):
        pass

    def keepLargestComponent(self, verbose=True, inplace=False):
        pass
    
    def subsample(self, n=100, weighted=False):
        if weighted:
            v, c = np.unique(self.getInteractionNamed().values, return_counts=True)
            genes = np.random.choice(v, size=n, replace=False, p=c/np.sum(c)) 
        
        else:
            v = np.unique(self.getInteractionNamed())
            genes = np.random.choice(v, size=n, replace=False)
                
        subset_df = self.subsetNetwork(genes, inplace=False)
        
        return subset_df

    def visualize(self, return_large=False):
        """ Visualize the graph """
        if return_large and (len(self.nodes) > 500 ):
            raise IOError('The graph contains more than 500 nodes, if you want to plot this specify return_large=True.')

        G = nx.from_pandas_edgelist(self.getInteractionNamed(), source='Gene_A', target='Gene_B')

        plt.figure()
        nx.draw(G, with_labels=True,
                node_size=2e2, node_color='lightskyblue', edge_color='gray')
        plt.style.use('ggplot')
        plt.rcParams['figure.figsize'] = [20, 15]
        plt.show()


class DirectedInteractionNetwork(Graph):
    def __init__(self, interaction_df, colnames=None, verbose=True, keeplargestcomponent=False):
        super().__init__(interaction_df, colnames, verbose=verbose, keeplargestcomponent=keeplargestcomponent)

    def mergedf(self, interaction_df, colnames=None):
        return self.mergeNetworks(DirectedInteractionNetwork(interaction_df, colnames=colnames, verbose=False))

    def mergeNetworks(self, network):
        return DirectedInteractionNetwork(pd.concat([self.getInteractionNamed(), network.getInteractionNamed()],
                                                    axis=0))
    '''
        get adj_dict
    '''
    def getAdjDict(self):
        ints_ = self.getInteractionNamed()
        sources = set(ints_.Gene_A)
        return {gene: set(ints_.Gene_B.loc[self.interactions.Gene_A == gene]) for gene in sources}

    def getGeodesicDistance(self, start_genes, stop_genes):
        '''
        :param: start_genes genes from which to find paths to stop_genes
        :return: a pandas df containing the pathlengths of shape (start_genes, stop_genes)
        '''

        A = nx.from_pandas_edgelist(self.getInteractionNamed(), source='Gene_A', target='Gene_B', create_using=nx.DiGraph)

        start_genes = list(set(sorted(A)).intersection(set(start_genes)))
        stop_genes = list(set(sorted(A)).intersection(set(stop_genes)))

        paths_lengths = np.array([len(nx.shortest_path(A, start, stop)) - 1 for stop in stop_genes for start in start_genes])
        paths_lengths_df = pd.DataFrame(np.reshape(paths_lengths, (len(start_genes), len(stop_genes))),
                                        index=start_genes, columns=stop_genes)
        return paths_lengths_df

    def findAllTrees(self):
        '''
        :return: A list of all maximum trees, one for each root
        '''
        pass

    def getComponents(self):
        '''
        :return:
            A dataframe containing the component label for every gene
            A boolean indicating whether the the graph is connected (true means connected)
        '''
        A, nodes = self.getAdjMatrix()
        ncomps, labels = csgraph.connected_components(A, directed=True)

        return pd.DataFrame({'Gene': nodes, 'Component': labels}), ncomps == 1

    def keepLargestComponent(self, verbose=True, inplace=False):
        components, connected = self.getComponents()

        if not connected:
            nodes, labels = components.Gene.values, components.Component.values
            v, c = np.unique(labels, return_counts=True)
            c_max = np.max(c)

            tbr_genes = [i for v_ in v[c != c_max] for i in nodes[labels == v_]]

            if verbose:
                print('%i genes from smaller components have been removed.' % len(tbr_genes))

            if inplace:
                self.removeNodes(tbr_genes, inplace=True)
            else:
                return self.removeNodes(tbr_genes, inplace=False)
            
    def subsample(self, n=100, weighted=False):
        return DirectedInteractionNetwork(super().subsample(n=n, weighted=weighted))

class UndirectedInteractionNetwork(Graph):
    def __init__(self, interaction_df, colnames=None, verbose=True, keeplargestcomponent=False):
        super().__init__(interaction_df, colnames, verbose=False,  keeplargestcomponent=keeplargestcomponent)
        self.nodes = pd.unique(self.interactions.values.flatten()).astype('str')
        self.N_nodes = len(self.nodes)
        self.interactions.values.sort(axis=1)
        self.interactions = self.interactions.drop_duplicates(['Gene_A', 'Gene_B'])

        if verbose:
            print('%d Nodes and %d interactions' % (len(self.nodes), self.interactions.shape[0]))

    def mergedf(self, interaction_df, colnames=None):
        return self.mergeNetworks(UndirectedInteractionNetwork(interaction_df, colnames=colnames, verbose=False))

    def subsetNetwork(self, nodes, inplace=False):
        if inplace:
            self.setEqual(UndirectedInteractionNetwork(super().subsetNetwork(nodes)))
        else:
            return UndirectedInteractionNetwork(super().subsetNetwork(nodes), verbose=True)

    def mergeNetworks(self, network):
        return UndirectedInteractionNetwork(pd.concat([self.getInteractionNamed(), network.getInteractionNamed()],
                                                        axis=0, ignore_index=True))

    def subsample(self, n=100, weighted=False):
        return super().subsample(n=n, weighted=weighted) #UndirectedInteractionNetwork(super().subsample(n=n, weighted=weighted))
    
    
    def checkInteractions_df(self, df, colnames=('Gene_A', 'Gene_B')):
        '''
            Checks which interactions from a given df can be found in the interaction network
        '''
        df.values.sort(axis=1)
        named_net_df = self.getInteractionNamed()
        named_net_df.values.sort(axis=1)
        tester_pairs = set(zip(named_net_df.Gene_A, named_net_df.Gene_B))
        df['In Network'] = [pair in tester_pairs for pair in zip(df[colnames[0]], df[colnames[1]])]
        return df

    def removeNodes(self, nodes_tbr, inplace=False):
        if inplace:
            super().removeNodes(nodes_tbr, inplace=inplace)
        else:
            return UndirectedInteractionNetwork(super().removeNodes(nodes_tbr, inplace=False))

    def getAdjMatrix(self, sort='first', as_df=False):
        A, nodes = super().getAdjMatrix(sort=sort)

        if as_df:
            return pd.DataFrame(np.maximum(A, np.transpose(A)), columns=nodes, index=nodes)
        else:
            return np.maximum(A, np.transpose(A)), nodes

    def getComponents(self):
        '''
        :return:
            A dataframe containing the component label for every gene
            A boolean indicating whether the the graph is connected (true means connected)
        '''
        A, nodes = self.getAdjMatrix()
        ncomps, labels = csgraph.connected_components(A, directed=False)

        return pd.DataFrame({'Gene': nodes, 'Component': labels}), ncomps == 1

    def keepLargestComponent(self, verbose=True, inplace=False):
        components, connected = self.getComponents()

        if not connected:
            nodes, labels = components.Gene.values, components.Component.values
            v, c = np.unique(labels, return_counts=True)
            c_max = np.max(c)

            tbr_genes = [i for v_ in v[c != c_max] for i in nodes[labels == v_]]

            if verbose:
                print('%i genes from smaller components have been removed.' % len(tbr_genes))

            if inplace:
                self.removeNodes(tbr_genes, inplace=True)
            else:
                return self.removeNodes(tbr_genes, inplace=False)

    def findcommunities(self, verbose=True):
        df = self.getInteractionNamed()
        nodes = {node: 1 for node in self.node_names}
        edges = [(pair, 1) for pair in zip(df.Gene_A, df.Gene_B)]
        nodes_, edges_ = in_order(nodes, edges)
        PyL_object = PyLouvain(nodes_, edges_)
        PyL_object.apply_method()

        all_genes = np.unique(df[['Gene_A', 'Gene_B']].values.flatten())
        map_dict = {i: all_genes[i] for i in range(len(all_genes))}

        communities = [list(map(lambda x: map_dict[x], comm)) for comm in PyL_object.actual_partition]

        if verbose:
            len_clust = [len(c) for c in communities]

            print('Size of the largest cluster: %i' % max(len_clust))
            print('Size of the smallest cluster: %i' % min(len_clust))
            print('Number of clusters: %i' % len(len_clust))

        return communities

    def clusterbydiffusion(self, kernel='LEX', alpha=0.01, nclusters=150, linkage='average', verbose=True):
        A, nodes = self.diffuse(kernel=kernel, alpha=alpha, as_df=False)
        ag = AgglomerativeClustering(n_clusters=nclusters, affinity='precomputed', linkage=linkage)
        ag.fit_predict(np.max(A)-A)
        clusters = [list(nodes[ag.labels_ == i]) for i in pd.unique(ag.labels_)]

        if verbose:
            len_clust = [len(c) for c in clusters]

            print('Size of the largest cluster: %i' % max(len_clust))
            print('Size of the smallest cluster: %i' % min(len_clust))
            print('Number of clusters: %i' % len(len_clust))

        return clusters

    def getAdjDict(self, return_names=True):
        if return_names:
            df = self.getInteractionNamed()
        else:
            df = self.interactions

        return to_dict_of_lists(nx.from_pandas_edgelist(df, source='Gene_A', target='Gene_B'))

    def getGeodesicDistance(self, start_genes, stop_genes):
        '''
        :param: start_genes genes from which to find paths to stop_genes
        :return: a pandas df containing the pathlengths of shape (start_genes, stop_genes)
        '''

        A = nx.from_pandas_edgelist(self.getInteractionNamed(), source='Gene_A', target='Gene_B')

        start_genes = list(set(sorted(A)).intersection(set(start_genes)))
        stop_genes = list(set(sorted(A)).intersection(set(stop_genes)))

        paths_lengths = np.array([len(nx.shortest_path(A, start, stop)) - 1 for stop in stop_genes for start in start_genes])
        paths_lengths_df = pd.DataFrame(np.reshape(paths_lengths, (len(start_genes), len(stop_genes))),
                                        index=start_genes, columns=stop_genes)
        return paths_lengths_df

    def getMinimmumSpanningTree(self):
        df = self.getInteractionNamed()
        A = nx.from_pandas_edgelist(df, source='Gene_A', target='Gene_B')
        T = nx.minimum_spanning_tree(A)

        return list(T.edges)

    def getTrainTestPairs_MStree(self, train_ratio=0.7, neg_pos_ratio=5, check_training_set=False, random_state=42):
        '''
        :param: train_ratio: The fraction of samples used for training
        :param: neg_pos_ratio: The ratio of negative examples to positive examples
        :param: assumption: Whether we work in the open world or  closed world assumption
        :return: positive and negative pairs for both train and test set (4 lists in total)
        '''
        np.random.seed(random_state)
        # To get the negatives we first build the adjacency matrix
        df = self.interactions
        df.values.sort(axis=1)

        allpos_pairs = set(zip(df.Gene_A, df.Gene_B))
        pos_train, pos_test = positives_split(df, train_ratio)

        N_neg = np.int(neg_pos_ratio * len(allpos_pairs))
        margin = np.int(0.3 * N_neg)

        row_c = np.random.choice(self.N_nodes, N_neg + margin, replace=True)
        col_c = np.random.choice(self.N_nodes, N_neg + margin, replace=True)

        all_pairs = set([tuple(sorted((r_, c_))) for r_, c_ in zip(row_c, col_c) if (c_ != r_)])

        all_neg = np.array(list(all_pairs.difference(allpos_pairs)), dtype=np.uint16)

        if len(all_neg) > N_neg:
            all_neg = all_neg[:N_neg]
        elif len(all_neg) < N_neg:
            print('The ratio of negatives to positives is lower than the asked %f.'
                  '\nReal ratio: %f' % (neg_pos_ratio, len(all_neg) / len(allpos_pairs)))

        train_ids = np.int(len(all_neg) * train_ratio)
        neg_train, neg_test = all_neg[:train_ids], all_neg[train_ids:]

        degrees = self.getDegreeDF(return_names=False)
        degrees.index = degrees.Gene.values

        if check_training_set:
            genes, counts = np.unique(all_neg.flatten(), return_counts=True)
            df = pd.DataFrame({'Gene': [self.int2gene[g] for g in genes], 'Counts': counts,
                               'Expected': degrees['Count'].loc[genes].values * neg_pos_ratio})
            df['Difference'] = df.Expected - df.Counts
            return list(pos_train), list(neg_train), list(pos_test), list(neg_test), df

        else:
            return list(pos_train), list(neg_train), list(pos_test), list(neg_test)

    def getTrainTestPairs_Balanced(self, neg_pos_ratio=5, train_ratio=0.7, check_training_set=False, random_state=42):
        np.random.seed(random_state)
        # Store all positive interactions
        pos_train, pos_test = positives_split(self.interactions, train_ratio=train_ratio)
        # TODO: different implementation, not based on MS tree
        degrees = self.getDegreeDF(return_names=False)
        degrees.index = degrees.Gene.values
        adj_dict = self.getAdjDict(return_names=False)

        counts = degrees.sort_values(by='Gene', ascending=True)['Count'].values * neg_pos_ratio
        sorted_genes = degrees.sort_values(by='Count', ascending=False)['Gene'].values

        all_negatives, genes, genes_train, genes_test, done, neg_train, neg_test = [], [], [], [], [], [], []

        for gene in sorted_genes:
            if counts[gene] > 0:
                neighbors = adj_dict[gene]
                zeros = list(np.where(counts <= 0)[0])
                nzeros = len(zeros)

                draws = np.minimum(self.N_nodes, counts[gene] + len(neighbors) + len(done) + nzeros + 1) # Two last terms?

                candidates = np.random.choice(self.N_nodes, draws, replace=False)

                not_considered = neighbors + [gene] + done + zeros
                negatives = np.setdiff1d(candidates, not_considered)

                max_id = np.minimum(counts[gene], len(negatives))

                if max_id < counts[gene]:
                    print('Not enough negatives available for gene %s' % self.int2gene[gene])

                negatives = random.sample(set(negatives), max_id)
                train_id = np.int(np.round(train_ratio * len(negatives)))

                neg_train += negatives[:train_id]
                neg_test += negatives[train_id:]

                counts[gene] = counts[gene] - len(negatives)
                counts[negatives] = counts[negatives] - 1

                all_negatives += list(negatives)
                genes_test += [gene for _ in range(len(negatives[train_id:]))]
                genes_train += [gene for _ in range(train_id)]
                genes = genes_train + genes_test
                done += [gene]

        neg_train = list(zip(genes_train, neg_train))
        neg_test = list(zip(genes_test, neg_test))

        if check_training_set:
            genes, counts = np.unique(np.concatenate((all_negatives, genes)), return_counts=True)
            df = pd.DataFrame({'Gene': [self.int2gene[g] for g in genes], 'Counts': counts,
                               'Expected': degrees.loc[genes]['Count'].values * neg_pos_ratio})
            df['Difference'] = df.Expected - df.Counts
            return pos_train, neg_train, pos_test, neg_test, df

        else:
            return pos_train, neg_train, pos_test, neg_test

    def getTrainTestData(self, train_ratio=0.7, neg_pos_ratio=5, method='balanced',
                         return_summary=True, random_state=42):
        '''
        :param: train_ratio: The fraction of samples used for training
        :param: neg_pos_ratio: The ratio of negative examples to positive examples
        :param: method: The sampling method used for generating the pairs:
                - ms_tree: uses a minimum spanning tree to find at least one positive pair for each node
                - balanced: draws approximately (neg_pos_ratio * n_positives) negatives for each gene
        :return: positive and negative pairs for both train and test set (4 lists in total)
        '''

        if method.lower() == 'ms_tree':
            pos_train, neg_train, pos_test, neg_test, summary_df = self.getTrainTestPairs_MStree(train_ratio=train_ratio,
                                                                                                 neg_pos_ratio=neg_pos_ratio,
                                                                                                 check_training_set=True,
                                                                                                 random_state=random_state)
        else:
            pos_train, neg_train, pos_test, neg_test, summary_df = self.getTrainTestPairs_Balanced(train_ratio=train_ratio,
                                                                                                   neg_pos_ratio=neg_pos_ratio,
                                                                                                   check_training_set=True,
                                                                                                   random_state=random_state)

        X_train = np.array(pos_train + neg_train)
        X_test = np.array(pos_test + neg_test)

        Y_train = np.array([1 for _ in range(len(pos_train))] + [0 for _ in range(len(neg_train))])
        Y_test = np.array([1 for _ in range(len(pos_test))] + [0 for _ in range(len(neg_test))])
        if return_summary:
            return X_train, X_test, Y_train, Y_test, summary_df
        else:
            return X_train, X_test, Y_train, Y_test

    def getAllTrainData(self, neg_pos_ratio=5, random_state=42):
        np.random.seed(random_state)
        df = self.interactions
        df.values.sort(axis=1)

        X = set(zip(df.Gene_A, df.Gene_B))
        Y_pos = [1 for _ in range(len(X))]

        N_neg = np.int(neg_pos_ratio * len(X))
        all_pairs = set([(i, j) for i in np.arange(self.N_nodes, dtype=np.uint16) for j
                         in np.arange(i + 1, dtype=np.uint16)])

        all_neg = list(all_pairs.difference(X))
        ids = np.random.choice(len(all_neg), np.minimum(N_neg, len(all_neg)), replace=False)

        X = np.array(list(X) + [all_neg[i] for i in ids])
        Y = np.array( Y_pos + [0 for _ in range(len(ids))])

        return X, Y

'''
    def fitAllSamples(self, dlmodel, steps_per_epoch=None, n_epochs=5):
        A, genes = self.getAdjMatrix(sort='')
        _generator = (([i, j], A[i,j]) for i in range(len(genes)) for j in range(i + 1))
        print('Starting the training of the model...')

        if steps_per_epoch is None:
            steps_per_epoch = len(genes) * (len(genes)- 1)/2

        dlmodel.model.fit_generator(generator=_generator, steps_per_epoch=steps_per_epoch, epochs=n_epochs)


    def getEmbdding(self, embedding_dim, method='DLembedding', **kwds):
        if method.lower() == 'spectralembedding':
            A, genes = self.getAdjMatrix()
            se = spectral_embedding(A, n_components=embedding_dim)

            return pd.DataFrame(se, index=genes)

        else:
            X, Y = self.getAllTrainData(**kwds)
            dl = DLembedder(self.N_nodes, embed_dim=embedding_dim, **kwds)
            dl.fit(X, Y, **kwds)
            embs = dl.getEmbeddings()

            return pd.DataFrame(embs, index=self.nodes)
'''

def ind2sub(X, nrows):
    X = np.array(X, dtype=np.uint64)
    col_ids, row_ids = np.divmod(X, nrows)

    return row_ids.astype(np.uint16), col_ids.astype(np.uint16)

def sub2ind(X, nrows):
    X = np.array(X)
    ind = X[:, 0] + X[:, 1] * nrows

    return ind

def positives_split(interaction_df, train_ratio=0.7):
    # First start with the positives
    all_pos_pairs = set(zip(interaction_df.Gene_A, interaction_df.Gene_B))
    N_edges = len(all_pos_pairs)
    min_tree = nx.minimum_spanning_tree(nx.from_pandas_edgelist(interaction_df, source='Gene_A', target='Gene_B')).edges

    pos_samples_train = set([tuple(sorted(tup)) for tup in list(min_tree)])
    all_pos_pairs = list(all_pos_pairs.difference(pos_samples_train))

    # determine how much samples need to drawn from the remaining positive pairs to achieve the train_test ratio
    still_needed_samples = np.maximum(0, np.round(train_ratio*N_edges - len(pos_samples_train)).astype(np.int))

    if still_needed_samples == 0:
        print('The train ratio has been increased to include every node in the training set.')

    ids_train = np.random.choice(len(all_pos_pairs), still_needed_samples, replace=False)
    ids_test = np.setdiff1d(np.arange(len(all_pos_pairs)), ids_train)

    pos_samples_train = list(pos_samples_train) + [all_pos_pairs[i] for i in ids_train]
    pos_samples_test = [all_pos_pairs[i] for i in ids_test]

    return pos_samples_train, pos_samples_test


def checkTrainingSetsPairs(X_train, Y_train, X_test, Y_test):
    '''
    :param X_train: a (train_samples, 2) np array
    :param Y_train: a (train_samples, ) np array
    :param X_test: a (test_samples, 2) np array
    :param Y_test: a (test_samples, ) np array
    :return: some statistics on the test and train set
    '''

    # First we check whether every pair in the training and the testing set is unique
    X_train_pairs = set(zip(X_train[:, 0], X_train[:, 1]))
    assert X_train.shape[0] == len(X_train_pairs), 'The training set contains non-unique entries.'
    X_test_pairs = set(zip(X_test[:, 0], X_test[:, 1]))
    assert X_test.shape[0] == len(X_test_pairs), 'The test set contains non-unique entries.'

    # Then we check for data leakage
    assert len(X_train_pairs.intersection(X_test_pairs)) == 0, 'Some gene pairs occur in both training and testing set.'

    # We also check if the ratio of the labels is comparable
    print('Positive-Negtative ratio for the training set: %f' % (sum(Y_train)/len(Y_train)))
    print('Positive-Negtative ratio for the test set: %f' % (sum(Y_test)/len(Y_test)))

class NBDInet(UndirectedInteractionNetwork):

    def __init__(self, interaction_df, omicsdatasets, colnames_interactiondf=None):

        temp = Graph(interaction_df, colnames=colnames_interactiondf, verbose=False)
        gene_names_net = temp.nodes

        ids_dict = {node: node + ' NET' for node in temp.nodes}
        temp.changeIDs(ids_dict=ids_dict)

        datatypes, samples = ['NET'], []
        dfs = [temp.interactions]

        for dataset in omicsdatasets:
            genes_in_network = set(gene_names_net).intersection(dataset.genes(as_set=True))
            datadf = dataset.get_all_pairs(include_type=True, colnames=('Gene_A', 'Gene_B'))

            dfs += [datadf]  # Add the Sample to status node interactions
            dfs += [pd.DataFrame({'Gene_A': [gene + ' NET' for gene in genes_in_network],
                                  'Gene_B': [gene + ' ' + dataset.type for gene in genes_in_network]})]
            datatypes.append(dataset.type)

            if (len(set(samples).intersection(dataset.samples(as_set=True))) < 1) & (len(samples) > 0):
                warnings.warn('No overlap with samples from %s dataset, be sure to use the correct identifiers' % dataset.type, UserWarning)

            samples += list(set([s.split(' ')[0] for s in datadf.Gene_A]))

        # Connect the status node to the node in the network

        super().__init__(pd.concat(dfs, axis=0), verbose=True)
        self.datatypes = datatypes
        self.samples = list(set(samples))
        self.diffused = None

        print('Integrated %i datatypes and %i samples.' % (len(self.datatypes), len(self.samples)))

    def extractSubmatrix(self, Suffix, diffused_mat=False):
        '''
        :param Suffix: A suffix  tuple(' EXP', ' MUT', ' NET', ...) which has to be selected  from the matrix
        :return: The submatrix containing all nodes suffix[0] x all nodes suffix[1]
        '''
        Suffix_A, Suffix_B = set([Suffix[0]]), set([Suffix[1]])

        if diffused_mat:
            if self.diffused is not None:
                mask_A = np.array([gene.split(' ')[-1] in Suffix_A for gene in self.nodes])  #TODO: get rid of these magic numbers
                mask_B = np.array([gene.split(' ')[-1] in Suffix_B for gene in self.nodes])

                return pd.DataFrame(self.diffused[mask_A, :][:, mask_B],
                                    index=np.array(self.nodes)[mask_A],
                                    columns=np.array(self.nodes)[mask_B])
            else:
                raise ValueError('The matrix is not yet diffused')

        else:  # return a subset of the adjacency matrix,
            mask = np.array(self.interactions.Gene_A.apply(lambda x: x[-4:]).isin(set(Suffix_A))) | \
                   np.array(self.interactions.Gene_B.apply(lambda x: x[-4:]).isin(set(Suffix_B)))

            return UndirectedInteractionNetwork(self.interactions.loc[mask]).getAdjMatrix(sort='last', as_df=True)

    def diffuse(self, kernel='LEX', alpha=0.01, as_df=False):
        self.diffused, self.nodes = super().diffuse(kernel=kernel, alpha=alpha, as_df=False)

    def getTopFeatures(self, data_types=None, topn=10, return_values=False, sample_groups=None, dist_measure='mean'):
        '''
        :param data_type: indicates the data types that need to be considered (EXP, MUT, DEL, AMP)
        :param topn: the number of top features considered for each data type
        :return: a list of len(data_types) x topn elements
        '''

        if data_types is None:
            data_types = self.datatypes
        else:
            data_types = set(data_types).intersection(set(self.datatypes))
            if len(data_types) < 1:
                warnings.warn('Types do not overlap with the datatypes in the NBDI network.', UserWarning)

        topfeatures = {}
        values = []

        for data_type in data_types:
            Dist = self.extractSubmatrix(('PAT', data_type), diffused_mat=True)
            features_ = Dist.columns.values

            if (dist_measure.lower() == 'mean_pos_neg') & (sample_groups is not None):
                # for now we assume two classes only
                sample_groups = sample_groups.loc[[s.split(' ')[0] for s in list(Dist.index)]]
                classes = pd.unique(sample_groups)

                if len(classes) != 2:
                    raise NotImplementedError('Feature selection can only happen for 2 classes.')

                mean_dist1 = Dist.loc[sample_groups.values == classes[0]].mean(axis=0)
                mean_dist2 = Dist.loc[sample_groups.values == classes[1]].mean(axis=0)

                dist = 2*(mean_dist1 - mean_dist2).abs()/(mean_dist1 + mean_dist2)
                mean_ids = dist.values.argsort()[-topn:][::-1]

            else:
                dist = Dist.mean(axis=0)
                mean_ids = dist.values.argsort()[-topn:][::-1]

            topfeatures[data_type] = [s[:s.rfind(' ')] for s in features_[mean_ids]]
            values += [dist]

        values_df = pd.concat(values, axis=0)
        if return_values:
            return topfeatures, values_df
        else:
            return topfeatures

## Helper functions
def getSecondOrderNeighbors(adj_dict, adj_dict0=None, incl_first_order=True):
    # slwo
    if adj_dict0 is None:
        adj_dict0 = adj_dict

    if incl_first_order:
        return {k: set([l for v_i in list(v) + [k] for l in adj_dict0[v_i]]) for k, v in adj_dict.items()}
    else:
        return {k: set([l for v_i in v for l in adj_dict0[v_i]]) for k, v in adj_dict.items()}
