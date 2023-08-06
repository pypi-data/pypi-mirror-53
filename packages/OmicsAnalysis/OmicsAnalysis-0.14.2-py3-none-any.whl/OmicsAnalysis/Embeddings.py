import pandas as pd
import numpy as np
import copy
import warnings
from sklearn.manifold import TSNE, LocallyLinearEmbedding, Isomap, SpectralEmbedding, MDS
from sklearn.decomposition import PCA, KernelPCA, NMF
from sklearn.metrics import pairwise_distances, pairwise_kernels
import matplotlib.pyplot as plt
from OmicsAnalysis.DiscreteOmicsDataSet import DiscreteOmicsDataSet
import umap
from sklearn.cluster import Birch, KMeans, AffinityPropagation, DBSCAN, AgglomerativeClustering, SpectralClustering
from OmicsAnalysis.rcc import RccCluster
from OmicsAnalysis.InteractionNetwork import UndirectedInteractionNetwork
import matplotlib as mpl

MANIFOLD_PARAMS = {
    "nmf": (),
    "mds": (),
    "pca": (),
    "kernel pca": frozenset(["kernel", "gamma", "degree", "coef0"]),
    "lle": frozenset(["n_neighbors", "method"]),
    "isomap": frozenset(["n_neighbors"]),
    "spectralembedding": frozenset(["gamma", "affinity", "n_neighbors"]),
    "tsne": frozenset(["perplexity", "early_exaggeration", "learning_rate", "n_iter", "metric=’euclidean"]),
}

KERNEL_PARAMS = {
    "additive_chi2": (),
    "chi2": frozenset(["gamma"]),
    "cosine": (),
    "linear": (),
    "poly": frozenset(["gamma", "degree", "coef0"]),
    "polynomial": frozenset(["gamma", "degree", "coef0"]),
    "rbf": frozenset(["gamma"]),
    "laplacian": frozenset(["gamma"]),
    "sigmoid": frozenset(["gamma", "coef0"]),
}


class Embeddings:
    def __init__(self, np_mat, gene_names):
        try:
            shape_ = np.array(np_mat.shape)
        except:
            raise UserWarning('The input is not a valid numpy array.')

        assert np.any(shape_ == len(gene_names)), 'The number of gene names is not consistent with the matrix shape.'
        assert len(shape_) == 2, 'Please provide a 2-dimensional numpy array.'

        try:
            self.values = np_mat.astype(np.float)
        except:
            raise UserWarning('Please provide a numeric matrix.')

        self.genes = np.array(gene_names).astype('str')

        self.Dimension = shape_[shape_ != len(self.genes)][0].astype(np.int)

        if shape_[1] != self.Dimension:
            self.values = np.transpose(self.values)

        print('Initialized embeddings for %i genes and a dimension of %i' % self.values.shape)

    @classmethod
    def from_df(cls, df, axis_embeddings='auto'):
        if axis_embeddings == 'auto':
            if df.shape[0] < df.shape[1]:
                df = df.transpose()
        elif axis_embeddings == 0:
            df = df.transpose()
        genes = list(df.index)
        return cls(df.values, genes)

    def df(self):
        return pd.DataFrame(self.values, index=self.genes)

    def subsetGenes(self, gene_list):
        gene_list = set(gene_list)
        mask = [g in gene_list for g in self.genes]

        if sum(mask) < len(gene_list):
            raise UserWarning('%i genes did not have an embedding.' % (len(gene_list) - sum(mask)))
        else:
            self.genes = self.genes[mask]
            self.values = self.values[mask, :]

    def getGeneSubset(self, gene_list):
        gene_list = set(gene_list)
        mask = np.array([g in gene_list for g in self.genes])

        return Embeddings.from_df(pd.DataFrame(self.values[mask, :], index=self.genes[mask]))

    def reduceDimensions(self, method='umap', n_comp=2, **kwds):

        np.random.seed(42)
        kwds = {k: v for k, v in kwds.items() if ((k in MANIFOLD_PARAMS.keys()) and (v is not None))}

        if method.lower() == 'nmf':
            self.values -= np.transpose(np.min(self.values, axis=0)[..., None])
            red_data = NMF(n_components=n_comp).fit_transform(self.values)
        elif method.lower() == 'pca':
            red_data = PCA(n_components=n_comp).fit_transform(self.values)
        elif method.lower() == 'kernel pca':
            red_data = KernelPCA(n_components=n_comp, **kwds).fit_transform(self.values)
        elif method.lower() == 'lle':
            red_data = LocallyLinearEmbedding(n_components=n_comp, **kwds).fit_transform(self.values)
        elif method.lower() == 'isomap':
            red_data = Isomap(n_components=n_comp, **kwds).fit_transform(self.values)
        elif method.lower() == 'spectralembedding':
            red_data = SpectralEmbedding(n_components=n_comp).fit_transform(self.values)
        elif method.lower() == 'mds':
            red_data = MDS(n_components=n_comp).fit_transform(self.values)
        elif method.lower() == 'tsne':
            red_data = TSNE(n_components=n_comp, verbose=1, random_state=3, init="pca").fit_transform(self.values)
        else:
            red_data = umap.UMAP(**kwds).fit_transform(self.values)

        return red_data

    def plotClasses(self, labels, reduction_method='umap', apply_pca=False, plot_title=None,
                    class2color=None, class2size=None, classnames=None):

        # Check if the provided labels are ints from 0 to n_classes - 1
        # zero denotes the unknown class
        classes = pd.unique(labels)
        N = len(classes)

        if len(np.setdiff1d(classes, np.arange(N))) > 0:
            print('Reformatting the labels from 0 to %i' % N)
            map_dict = {classes[i]: i for i in range(N)}
            labels = [map_dict[l] for l in labels]

        assert self.Dimension > 1, print('1D Embeddings cannot be plotted in 2D.')
        plot_data = 0

        if self.Dimension > 2:
            plot_data = self.reduceDimensions(n_comp=2, method=reduction_method)
        elif self.Dimension == 2:
            if apply_pca:
                plot_data = PCA.fit_transform(self.values)
            else:
                plot_data = self.values

        fig, ax = plt.subplots(1, 1, figsize=(6, 6))

        if class2color is not None:
            print('Plotting a custom plot')

            if class2size is None:
                class2size = {class_: 7 for class_ in classes}

            if classnames is not None:
                class_names = [classnames[l] for l in labels]
            else:
                class_names = None

            ax.scatter(plot_data[:, 0], plot_data[:, 1], c=class2color, s=class2size, label=classnames, alpha=0.5)

            if classnames is not None:
                plt.legend()

        else:
            # define the colormap
            cmap = plt.cm.jet
            # extract all colors from the .jet map
            cmaplist = [cmap(i) for i in range(cmap.N)]
            # create the new map
            cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

            # define the bins and normalize
            bounds = np.linspace(0, N, N + 1)
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

            # make the scatter
            scat = ax.scatter(plot_data[:, 0], plot_data[:, 1], alpha=0.7, s=20, c=labels, cmap=cmap, norm=norm)

        if plot_title is not None:
            ax.set_title(plot_title)

        plt.xlabel('First dimension', fontsize=14)
        plt.ylabel('Second Dimension', fontsize=14)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.show()

    def clusterEmbeddings(self, method='rcc', metric='euclidean', dim_red=None, dims=2, **kwds):
        '''
        :param method: the name of the cluster algorithm, implemented are
        [Birch, KMeans, AffinityPropagation, DBSCAN, AgglomerativeClustering, SpectralClustering]
        :param metric:
        :param dim_red: indicates whether dimensionality reduction needs to be done before clustering.
        Generally not recommended (default is None).
        :param kwds:
        :return:
        '''

        if dim_red is not None:
            cluster_data = self.reduceDimensions(method=dim_red, n_comp=dims, **kwds)

        else:
            cluster_data = self.values

        if method.lower() == 'birch':
            cl = Birch(**kwds)
            clusters = cl.fit_predict(cluster_data)
        elif method.lower() == 'kmeans':
            cl = KMeans(**kwds)
            clusters = cl.fit_predict(cluster_data)
        elif method.lower() == 'agglomerative':
            cl = AgglomerativeClustering(**kwds)
            clusters = cl.fit_predict(cluster_data)
        elif method.lower() == 'dbscan':
            cl = DBSCAN(**kwds)
            clusters = cl.fit_predict(cluster_data)
        elif method.lower() == 'affinityprop':
            cl = AffinityPropagation(**kwds)
            clusters = cl.fit_predict(cluster_data)
        elif method.lower() == 'spectralclustering':
            cl = SpectralClustering(**kwds)
            clusters = cl.fit_predict(cluster_data)
        else:
            cl = RccCluster(**kwds)
            clusters = cl.fit(cluster_data)

        return pd.DataFrame(clusters, index=self.genes)

    def plotDimension(self, dimension_axis=1, apply_PCA=False, gene_list=None):
        if apply_PCA:
            plot_data = PCA(n_components=self.Dimension).fit_transform(self.values)[:, dimension_axis]
        else:
            plot_data = self.values[:, dimension_axis]

        plot_max, plot_min = np.max(plot_data), np.min(plot_data)

        if gene_list is not None:
            mask = np.array([gene in gene_list for gene in self.genes])
            plot_data2 = plot_data[mask]
            plot_data = plot_data[~mask]

        plt.hold(True)
        bin_seq = np.linspace(plot_min, plot_max, num=200)
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.hist(plot_data, bins=bin_seq, alpha=0.5, label='Genes', normed=True)

        if gene_list is not None:
            plt.hist(plot_data2, bins=bin_seq, alpha=0.5, label='Genes in list', normed=True)

        plt.legend(loc='upper right')

        plt.legend(fontsize=14)
        plt.xlabel('Dimension ' + str(dimension_axis), fontsize=20)
        plt.ylabel('Frequency', fontsize=20)
        ax.tick_params(axis='both', which='major', labelsize=18)
        ax.tick_params(axis='both', which='minor', labelsize=18)
        ax.grid(False)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    def PlotScatter2D(self, gene_list=None, reduction_method='umap', fig_title='', apply_pca=False):
        assert self.Dimension > 1, print('1D Embeddings cannot be plotted in 2D.')
        plot_data = 0

        if self.Dimension > 2:
            plot_data = self.reduceDimensions(n_comp=2, method=reduction_method)
        elif self.Dimension == 2:
            if apply_pca:
                plot_data = PCA.fit_transform(self.values)
            else:
                plot_data = self.values

        if gene_list is None:
            gene_list = [None]

        gene_list = set(gene_list)

        colors = np.array(['tab:orange' if g in gene_list else 'tab:blue' for g in self.genes])
        sizes = np.array([10 if g in gene_list else 3 for g in self.genes])

        plt.figure()
        plt.scatter(plot_data[:, 0], plot_data[:, 1], c=colors, s=sizes, alpha=0.5)
        plt.xlabel('First dimension', fontsize=14)
        plt.ylabel('Second Dimension', fontsize=14)
        plt.title(fig_title)
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.show()

    def getDistances(self, metric='euclidean', gene_list=None):
        '''
        :param metric: Can be one of [cityblock’, ‘cosine’, ‘euclidean’, ‘l1’, ‘l2’, ‘manhattan’,
        ‘braycurtis’, ‘canberra’, ‘chebyshev’, ‘correlation’, ‘dice’, ‘hamming’, ‘jaccard’,
         ‘kulsinski’, ‘mahalanobis’, ‘minkowski’, ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’, ‘sokalmichener’,
         ‘sokalsneath’, ‘sqeuclidean’, ‘yule’]
        :param gene_list: optional, a list of genes that are to be compared to other genes
        :return: a distance matrix
        '''

        if gene_list is None:
            Dist = pairwise_distances(self.values, metric=metric)

        else:
            gene_list = set(gene_list)
            mask_a = np.array([g in gene_list for g in self.genes])

            Dist = pairwise_distances(self.values, self.values[mask_a])

        return Dist

    def getAffinities(self, metric='cosine', gene_list=None, **kwds):
        '''
        :param metric: Can be one of [‘rbf’, ‘sigmoid’, ‘polynomial’, ‘poly’, ‘linear’, ‘cosine’]
        :param gene_list: optional, a list of genes that are to be compared to other genes
        :return: a distance matrix
        '''

        kwds = {k:v for k, v in kwds.items() if ((k in KERNEL_PARAMS.keys()) and (v is not None))}

        if gene_list is None:
            Affinity = pairwise_kernels(self.values, metric=metric, **kwds)

        else:
            gene_list = set(gene_list)
            mask_a = np.array([g in gene_list for g in self.genes])

            Affinity = pairwise_kernels(self.values, self.values[mask_a], **kwds)

        return Affinity

    def calculateAffinities(self, discrete_dataset, metric='cosine', **kwds):
        '''
        :param dataset: A Discrete omics Dataset that contains mutation data
        :param method:
        :param kwds:
        :return:
        '''

        gene_df = discrete_dataset.sum(axis=0)
        gene_df = gene_df[gene_df > 0]

        genes = list(gene_df.index)
        affinities = self.getAffinities(metric=metric, gene_list=genes)

        affinities *= gene_df.values[..., None] # Does this broadcasting work?

        return affinities/len(discrete_dataset.samples)

    def diffuseAffinities(self, discrete_dataset, metric='cosine', **kwds):
        '''
        :param discrete_dataset:
        :param metric: kernel used for applying diffusion
        :param kwds: keywords passed directly  to the kernel function
        :return:
        '''

        genes = set(self.genes).intersection(discrete_dataset.genes(as_set=True))
        mask_emb = np.array([g in genes for g in self.genes])

        embd = self.values[mask_emb]

        data = discrete_dataset.getGeneSubset(list(genes)).df.values

        diffusion = np.matmul(data, embd)

        return pd.DataFrame(diffusion, index=discrete_dataset.samples(), columns=list(genes))


    def getMinDist(self, gene_list, metric='euclidean'):
        '''
        :param discrete_dataset:
        :param metric:
        :return: The minimum distance between the genes in the embedding and the genes in gene list
        '''

        dist = self.getDistances(metric=metric, gene_list=gene_list)
        return np.min(dist, axis=1)


    def getIndirectDistances(self, discrete_dataset, metric='euclidean', samples=None):
        nonzero_dicts = discrete_dataset.getNonzeroSampleDict()

        if samples is None:
            cohort_avg = 0
            for k, v in nonzero_dicts.items():
                min_dist = self.getMinDist(v, metric=metric)
                cohort_avg += np.sqrt(np.outer(min_dist, min_dist))
            return cohort_avg

        else:
            if isinstance(samples, str):
                samples = [samples]

            try:
                min_dist = 0
                for sample in samples:
                    min_dist += self.getMinDist(nonzero_dicts[sample], metric=metric)

            except KeyError:
                raise KeyError('The provided sample ID is not in the dataset.')

            return min_dist


    def compareDimensionReductions(self, methods=None, gene_list=None, **kwds):
        if methods is None:
            methods = ["nmf", "mds", "pca", "kernel pca", "lle", "isomap", "spectralembedding", "tsne", 'umap']
            labels = ["NMF", "MDS", "PCA", "Kernel PCA", "LLE", "Isomap", "Spectral Embedding", "TSNE", 'UMAP']
        else:
            labels = methods

        fig = plt.figure(figsize=(15, 8))

        if gene_list is None:
            gene_list = [None]

        gene_list = set(gene_list)

        colors = np.array(['tab:orange' if g in gene_list else 'tab:blue' for g in self.genes])
        sizes = np.array([10 if g in gene_list else 3 for g in self.genes])

        for i, method in enumerate(methods):
            Y = self.reduceDimensions(method=method, **kwds)

            ax = fig.add_subplot(241 + i)
            plt.scatter(Y[:, 0], Y[:, 1], c=colors, s=sizes)
            plt.title(labels[i])
            plt.axis('tight')

        plt.show()


    def plotDiscreteDataset(self, dataset, reduction_method='umap', fig_title='', apply_pca=False):
        #TODO implement this such that several datasets can be plotted at once

        assert self.Dimension > 1, print('1D Embeddings cannot be plotted in 2D.')
        plot_data = 0

        if self.Dimension > 2:
            plot_data = self.reduceDimensions(n_comp=2, method=reduction_method)
        elif self.Dimension == 2:
            if apply_pca:
                plot_data = PCA.fit_transform(self.values)
            else:
                plot_data = self.values

        freq = dataset.sum(axis=0)
        colors = np.array(['tab:red' if g in dataset.genes(as_set=True) else 'tab:blue' for g in self.genes])
        sizes = np.array([freq[g] if g in dataset.genes(as_set=True) else 3 for g in self.genes])

        plt.figure()
        plt.scatter(plot_data[:, 0], plot_data[:, 1], c=colors, s=sizes, alpha=0.5)
        plt.xlabel('First dimension', fontsize=14)
        plt.ylabel('Second Dimension', fontsize=14)
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.show()


    def PlotScatterInteractive(self, gene_list=None, reduction_method='tsne', fig_title='', apply_pca=False, alpha=0.5):
        assert self.Dimension > 1, print('1D Embeddings cannot be plotted in 2D.')
        plot_data = 0

        if self.Dimension > 2:
            plot_data = self.reduceDimensions(n_comp=2, method=reduction_method)
        elif self.Dimension == 2:
            if apply_pca:
                plot_data = PCA.fit_transform(self.values)
            else:
                plot_data = self.values

        if gene_list is None:
            gene_list = [None]

        gene_list = set(gene_list)

        colors = np.array(['tab:orange' if g in gene_list else 'tab:blue' for g in self.genes])
        sizes = np.array([10 if g in gene_list else 3 for g in self.genes])

        cluster_coords = create_shape_on_image(plot_data, colors=colors, sizes=sizes, alpha=alpha)
        cluster_genes = dict()

        for k, v in cluster_coords.items():
            xs, ys = v
            x_min, x_max, y_min, y_max = np.min(xs), np.max(xs), np.min(ys), np.max(ys)
            cluster_genes[k] = self.genes[(plot_data[:, 0] > x_min) & (plot_data[:, 0] < x_max) &\
                                          (plot_data[:, 1] > y_min) & (plot_data[:, 1] < y_max)]
        # TODO: further improve this selection method

        return cluster_genes

    def checkNeighbors(self, network, genes, reduction_method='umap', apply_pca=False, fig_title=''):
        adj_dict = network.getAdjDict()

        nbs = []
        for gene in genes:
            nbs +=  list(adj_dict[gene])

        gene_list = set(nbs)

        assert self.Dimension > 1, print('1D Embeddings cannot be plotted in 2D.')
        plot_data = 0

        if self.Dimension > 2:
            plot_data = self.reduceDimensions(n_comp=2, method=reduction_method)
        elif self.Dimension == 2:
            if apply_pca:
                plot_data = PCA.fit_transform(self.values)
            else:
                plot_data = self.values

        colors = np.array(['tab:red' if g in genes else'tab:orange' if g in gene_list else 'tab:blue' for g in self.genes])
        sizes = np.array([60 if g in genes else 20 if (g in gene_list) else 3 for g in self.genes])

        plt.figure()
        plt.scatter(plot_data[:, 0], plot_data[:, 1], c=colors, s=sizes, alpha=0.5)
        plt.xlabel('First dimension', fontsize=14)
        plt.ylabel('Second Dimension', fontsize=14)
        plt.title(fig_title)
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.show()


class LineBuilder:
    def __init__(self, line, ax, color):
        self.line = line
        self.ax = ax
        self.color = color
        self.xs = []
        self.ys = []
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
        self.counter = 0
        self.precision = 0.01
        self.precision_x = (ax.get_xlim()[1] - ax.get_xlim()[0]) * self.precision
        self.precision_y = (ax.get_ylim()[1] - ax.get_ylim()[0]) * self.precision
        self.clusters = dict()
        self.cluster_counter = 0

    def __call__(self, event):
        if event.inaxes != self.line.axes: return
        if self.counter == 0:
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.ax.scatter(self.xs, self.ys, s=60, color=self.color)
        if np.abs(event.xdata-self.xs[0]) <= self.precision_x and np.abs(event.ydata-self.ys[0]) <= self.precision_y and self.counter > 2:
            self.xs.append(self.xs[0])
            self.ys.append(self.ys[0])
            self.ax.scatter(self.xs,self.ys, s=60, color=self.color)
            self.ax.scatter(self.xs[0], self.ys[0], s=40, color='blue')
            self.ax.plot(self.xs, self.ys, color=self.color)
            self.ax.text((min(self.xs) + max(self.xs))/2,
                         (min(self.ys) + max(self.ys))/2,
                         'Cluster ' + str(self.cluster_counter))
            self.line.figure.canvas.draw()

            self.clusters['Cluster ' + str(self.cluster_counter)] = (np.array(self.xs), np.array(self.ys))
            self.cluster_counter += 1

            self.xs = []
            self.ys = []
            self.counter = 0
        else:
            if self.counter != 0:
                self.xs.append(event.xdata)
                self.ys.append(event.ydata)

            self.ax.scatter(self.xs, self.ys, s=60, color=self.color)
            self.ax.plot(self.xs, self.ys,color=self.color)

            if not ((self.counter == 0) and (self.cluster_counter > 0)):
                self.line.figure.canvas.draw()

            self.counter = self.counter + 1

def create_shape_on_image(data, colors='tab:blue', sizes=3, alpha=0.5):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('click to include shape markers')

    line = plt.scatter(data[:, 0], data[:, 1], c=colors, s=sizes, alpha=alpha)
    plt.xlabel('First dimension', fontsize=14)
    plt.ylabel('Second Dimension', fontsize=14)
    ax = plt.gca()
    print(ax.get_xlim())
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    linebuilder = LineBuilder(line, ax, 'red')
    plt.gca().invert_yaxis()
    plt.show(block=True)
    # new_shapes = change_shapes(linebuilder.shape)
    x_coords, y_coords = linebuilder.xs, linebuilder.ys
    cluster_coords = linebuilder.clusters

    return cluster_coords

