import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.mixture import GaussianMixture
from cycler import cycler
from scipy.stats import expon, pearsonr, spearmanr, kendalltau
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.preprocessing import StandardScaler
from OmicsAnalysis.DiscreteOmicsDataSet import DiscreteOmicsDataSet
from OmicsAnalysis.InteractionNetwork import UndirectedInteractionNetwork
from OmicsAnalysis.OmicsDataSet import OmicsDataSet
import copy

class ContinuousOmicsDataSet(OmicsDataSet):
    def __init__(self, dataframe, patient_axis='auto', remove_nas=True, type='Omics',
                 remove_zv=True, verbose=True,
                 average_dup_genes=True, average_dup_samples=True):

        super().__init__(dataframe, patient_axis, remove_nas, type=type, remove_zv=remove_zv,
                         verbose=verbose, average_dup_genes=average_dup_genes,
                         average_dup_samples=average_dup_samples)

    def compareSampleProfiles(self, kind='density', randomseed=None, Npatients=4):
        np.random.seed(randomseed)

        random_patients = list(np.random.permutation(self.samples())[:Npatients])
        plot_df = self.df.loc[random_patients]
        plot_df = plot_df.transpose()
        if kind == 'density':
            plot_df.plot(kind='density', subplots=True, use_index=False)
        else:
            plot_df.hist(bins=100)
        plt.show()

    def compareGeneProfiles(self, gene_list=None, Ngenes=4, kind='histogram'):
        if gene_list is None:
            random_genes = list(np.random.permutation(self.genes())[:Ngenes])
            print(random_genes)
            plot_df = self.df[random_genes]
        else:
            plot_genes = list(set(gene_list).intersection(set(self.genes())))
            plot_df = self.df[plot_genes]

        if plot_df.shape[1] > 0:
            if kind == 'density':
                plot_df.plot(kind='density', subplots=True, use_index=False)
            else:
                plot_df.hist(bins=100)

            plt.xlabel('Normalized expression', fontsize=14)
            plt.show()
        else:
            print('None of the genes are found in the dataset...')

    def normalizeProfiles(self, method='Quantile', axis=1):
        '''
        :param method: defines the method by which the (expression) profiles are scaled.
        currently supported is standardscaling, quantile normalization and centering.
        :param axis: the axis along which to scale (0 scales the genes profiles, 1 scales the patient profiles)
        :return: None (self.df is normalized)
        '''
        if axis == 1:
            self.df = self.df.transpose()

        if method.lower() == 'standardscaling':
            self.df = (self.df - self.mean(axis=0))/self.std(axis=0)
        elif method.lower() == 'quantile':
            rank_mean = self.df.stack().groupby(self.df.rank(method='first').stack().astype(int)).mean()
            self.df = self.df.rank(method='min').stack().astype(int).map(rank_mean).unstack()
        elif method.lower() == 'center':
            self.df = self.df - self.mean(axis=0)
        else:
            raise Exception('NotImplementedError')

        if axis == 1:
            self.df = self.df.transpose()
        #TODO: invent fantastic scaling algorithm

    def concatDatasets(self, datasets, axis=1, include_types=True, average_dup_genes=True, average_dup_samples=True):
        DF = super().concatDatasets(datasets, axis, include_types)

        return ContinuousOmicsDataSet(DF, patient_axis=0,
                                      average_dup_genes=average_dup_genes,
                                      average_dup_samples=average_dup_samples)

    def __getitem__(self, item):
        if item > len(self.samples()):
            raise IndexError
        return ContinuousOmicsDataSet(self.df.iloc[item], type=self.type, remove_zv=False, patient_axis=0)

    def GetPatientDistances(self, norm):
        pass

    def GetGeneDistances(self, norm):
        pass

    def getGeneCorrelations(self, gene_list=None, method='pearson', **kwargs):
        '''
        :param gene_list: genes for which to calculate the correlation
        :param method: method to use for calculating the correlations.
        Options are:
        pearson
        spearman
        kendall, ranked-pearson, ranked-spearman and ranked-kendall.
        The ranked- version applies a ranking correction that both genes are also amongst the higest ranked
        genes in each other's list of co-expressed genes.
        '''
        if gene_list is not None:
            corrs, pvals = self.getGeneSubset(gene_list).getGeneCorrelations(method=method)
            return corrs, pvals
        else:
            corrs = calculateAssociationSelf(self.df, method=method.lower(), **kwargs)
            return corrs

        # TODO add other methods

    def getSampleSubset(self, sample_list):
        return ContinuousOmicsDataSet(super().getSampleSubset(sample_list), patient_axis=0, type=self.type)

    def getGeneSubset(self, gene_list):
        return ContinuousOmicsDataSet(super().getGeneSubset(gene_list), patient_axis=0, type=self.type)

    def applyDensityBinarization(self, save_path=None, min_clustersize=150,
                                 max_nclusters=1000, p_thresh=1.e-5, MA_window=1,
                                 remove_zv=True):

        bin_gx = self.df.apply(lambda x: densityDiscretization1D(x, min_clustersize=min_clustersize,
                                                                 max_nclusters=max_nclusters, p_thresh=p_thresh,
                                                                 MA_window=MA_window), axis=0)

        if save_path is not None:
            print('data is being saved to:' + save_path)
            bin_gx.to_csv(save_path, sep='\t', index=True, header=True)

        return DiscreteOmicsDataSet(bin_gx, type=self.type, patient_axis=0, remove_zv=remove_zv)

    def applyGMMBinarization(self, save_path=None, max_regimes=2, remove_zv=False, criterion='bic'):
        '''
        :param save_path: the path to which to save the binarized dataframe
        :param max_regimes: the max number of regimes
        :return: a DiscreteOmicsDataSet containing the discretized data
        '''

        np.random.seed(42)

        bin_gx = np.zeros(self.df.shape, dtype=np.uint16)
        id = 0

        for gene in self.genes():
            temp = self.df[gene]

            temp = np.reshape(temp.values, (-1, 1))
            max_val = np.max(temp)
            print(id)
            gm_best, BIC_min, n_regimes = get_optimal_regimes(temp, max_regimes=max_regimes,
                                                              criterion=criterion)

            if n_regimes == 2:
                labels = gm_best.predict(temp)
                labels = 1*(gm_best.predict(max_val) == labels)
                bin_gx[:, id] = labels.astype(np.uint16)
            else:
                labels = gm_best.predict(temp)
                bin_gx[:, id] = labels.astype(np.uint16)

            id += 1

        bin_gx = pd.DataFrame(bin_gx, index=self.samples(), columns=self.genes())

        if save_path is not None:
            print('data is being saved to:' + save_path)
            bin_gx.to_csv(save_path, sep='\t', index=True, header=True)

        return DiscreteOmicsDataSet(bin_gx, type=self.type, patient_axis=0, remove_zv=remove_zv)

    def applyGMMBinarization_new(self, save_path=None, max_regimes=2, remove_zv=True, criterion='bic'):
        '''
        :param save_path: the path to which to save the binarized dataframe
        :param max_regimes: the max number of regimes
        :return: a DiscreteOmicsDataSet containing the discretized data
        '''
        np.random.seed(42)

        bin_gx = self.df.apply(lambda x: getGMMRegimes(x, max_regimes=max_regimes, criterion=criterion), axis=0)

        if save_path is not None:
            print('data is being saved to:' + save_path)
            bin_gx.to_csv(save_path, sep='\t', index=True, header=True)

        return DiscreteOmicsDataSet(bin_gx, type=self.type, patient_axis=0, remove_zv=remove_zv)

    def KmeansBinning(self, n_clusters=2, save_path=None, remove_zv=True):
        km = KMeans(n_clusters=n_clusters)
        km_bin_df = self.df.apply(lambda x: km.fit_predict(np.reshape(x, (-1, 1))), axis=0)

        if save_path is not None:
            print('data is being saved to:' + save_path)
            km_bin_df.to_csv(save_path, sep='\t', index=True, header=True)

        return DiscreteOmicsDataSet(km_bin_df, type=self.type, patient_axis=0, remove_zv=remove_zv)

    def applySTDBinning(self, std_thresh=1.5, save_path=None):

        scaled_df = (self.df - self.mean(axis=0))/self.std(axis=0)
        std_bin_gx = 1*(scaled_df > std_thresh) - 1*(scaled_df < - std_thresh)
        std_bin_gx = std_bin_gx.astype(np.uint16)
        std_bin_gx[~np.isfinite(std_bin_gx)] = 0

        if save_path is not None:
            print('data is being saved to:' + save_path)
            std_bin_gx.to_csv(save_path, sep='\t', index=True, header=True)

        return DiscreteOmicsDataSet(std_bin_gx, type=self.type, patient_axis=0)

    def binData(self, method='GMM', n_regimes=3, remove_zv=False, criterion='bic'):

        if 'kmeans' in method.lower():
            binned_data = self.KmeansBinning(n_clusters=n_regimes, remove_zv=remove_zv)
        elif 'gmm' in method.lower():
            binned_data = self.applyGMMBinarization(max_regimes=n_regimes, remove_zv=remove_zv, criterion=criterion)
        elif 'density' in method.lower():
            binned_data = self.applyDensityBinarization(max_nclusters=n_regimes, remove_zv=remove_zv)
        else:
            binned_data = self.applySTDBinning()

        return binned_data

    def plotExpressionRegime(self, gene, insert_title=True, savepath=None, remove_frame=False, criterion='bic',
                             annotated_patients=None, annotation_labels=None, max_regimes=2, method='GMM',
                             return_data=False):

        plotmat = self.df[gene].values
        max_val = np.max(plotmat)
        mpl.rcParams['axes.prop_cycle'] = cycler(color=['tab:blue', 'tab:orange', 'tab:green', 'tab:red',
                                                'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
                                                'tab:olive', 'tab:cyan'])

        if method.lower() == 'std':
            std_thresh = 1.5
            labels = (plotmat - np.mean(plotmat))/np.std(plotmat)
            labels = 1*(labels > std_thresh) - 1*(labels < - std_thresh)

        else:
            plotmat = plotmat.reshape((-1, 1))
            gm_best, BIC_min, n_regimes = get_optimal_regimes(plotmat, max_regimes=max_regimes, criterion=criterion)
            labels = gm_best.predict(plotmat)

            if n_regimes == 2:
                labels = 1*(gm_best.predict(max_val) == labels)

        n_regimes = len(np.unique(labels))

        if n_regimes == 1:

            plot_df = pd.DataFrame({'Expression': plotmat.flatten(), 'Label': labels}, index=self.samples())
            bin_seq = np.linspace(plot_df.Expression.min(), plot_df.Expression.max(), num=200)
            label = ['Basal']
            fig, ax = plt.subplots(figsize=(8, 6))
            plot_df.groupby('Label').hist(ax=ax, bins=bin_seq, label=label)

            if annotated_patients is not None:
                print('Adding annotation lines')
                r = plot_df.loc[annotated_patients]
                r.Expression.hist(ax=ax, bins=bin_seq, label=annotation_labels)
                label.extend(annotation_labels)
                print(label)

            plt.legend(label, fontsize=16)

        elif n_regimes == 2:

            plot_df = pd.DataFrame({'Expression': plotmat.flatten(), 'Label': labels}, index=self.samples())
            plot_df.sort_values('Expression', ascending=True, inplace=True)

            labels = ['Regime 0', 'Regime 1']
            fig, ax = plt.subplots(figsize=(8, 6))
            bin_seq = np.linspace(plot_df.Expression.min(), plot_df.Expression.max(), num=200)
            plot_df.groupby('Label').hist(ax=ax, bins=bin_seq, label=labels)

            if annotated_patients is not None:
                print('Adding annotation lines')
                r = plot_df.loc[annotated_patients]
                r.Expression.hist(ax=ax, bins=bin_seq, label=annotation_labels)
                labels.extend(annotation_labels)
                print(labels)

            plt.legend(labels, fontsize=18)

        else:
            plot_df = pd.DataFrame({'Expression': plotmat.flatten(), 'Label': labels}, index=self.samples())
            plot_df.sort_values('Expression', ascending=True, inplace=True)

            fig, ax = plt.subplots(figsize=(8, 6))
            bin_seq = np.linspace(plot_df.Expression.min(), plot_df.Expression.max(), num=200)
            plot_df.groupby('Label').hist(ax=ax, bins=bin_seq)

            if annotated_patients is not None:
                print('Adding annotation lines')
                r = plot_df.loc[annotated_patients]
                r.Expression.hist(ax=ax, bins=bin_seq)

        if insert_title:
            plt.title('Expression profile for ' + str(gene), fontsize=18)
        else:
            plt.title('')

        plt.xlabel('Normalized expression', fontsize=20)
        plt.ylabel('Frequency', fontsize=20)
        ax.tick_params(axis='both', which='major', labelsize=18)
        ax.tick_params(axis='both', which='minor', labelsize=18)
        ax.grid(False)

        if remove_frame:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        if savepath is not None:
            print('Saving figure to: ' + savepath)
            plt.savefig(savepath, dpi=1000, bbox_inches="tight")

        plt.show()
        if return_data:
            return plot_df

    def Benchmarkbinning(self, labels, nregimes=None, nsplits=5, test_ratio=0.3, save_path=None):
        '''
        :param labels: provides class labels for each of the methods
        :param params: a nested dict containing the parameters for each binning method
        :return:
        '''

        sss = StratifiedShuffleSplit(n_splits=nsplits, test_size=test_ratio, random_state=0)
        sss.get_n_splits(self.df, labels)

        if nregimes is None:
            binning_methods = ['STD', 'GMM']
            nregimes = {'STD': 3, 'GMM': 3}
        else:
            binning_methods = list(nregimes.keys())

        scores_train, scores_val = pd.DataFrame(0, index=np.arange(nsplits), columns=binning_methods + ['Continuous']),\
                                   pd.DataFrame(0, index=np.arange(nsplits), columns=binning_methods + ['Continuous'])
        split_id = 0
        n_trees = 1500

        for train_index, test_index in sss.split(self.df, labels):

            X_train, X_val = self.df.iloc[train_index], self.df.iloc[test_index]
            Y_train, Y_val = labels[train_index], labels[test_index]
            print(self.df.shape)
            rf = RandomForestClassifier(n_estimators=n_trees)
            rf.fit(X_train, Y_train)

            scores_train.loc[split_id, 'Continuous'] = accuracy_score(Y_train, rf.predict(X_train))
            scores_val.loc[split_id, 'Continuous'] = accuracy_score(Y_val, rf.predict(X_val))

            for binning_method in binning_methods:
                bin_data = self.binData(method=binning_method, n_regimes=nregimes[binning_method])  #ZV features are automatically removed
                print(bin_data.df.shape)
                X_train, X_val = bin_data.df.iloc[train_index], bin_data.df.iloc[test_index]

                rf = RandomForestClassifier(n_estimators=n_trees)
                rf.fit(X_train, Y_train)

                scores_train.loc[split_id, binning_method] = accuracy_score(Y_train, rf.predict(X_train))
                scores_val.loc[split_id, binning_method] = accuracy_score(Y_val, rf.predict(X_val))

            split_id += 1

        ax = scores_val.boxplot(boxprops={'linewidth': 2}, flierprops={'linewidth': 2},
                                medianprops={'linewidth': 2, 'color': 'darkgoldenrod'})
        plt.xticks(fontsize=14)
        plt.ylabel('Accuracy', fontsize=14)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        if save_path is not None:
            plt.savefig(save_path + 'boxplot_binning_benchmark.pdf', dpi=1000, bbox_inches="tight")
            plt.savefig(save_path + 'boxplot_binning_benchmark.png', dpi=1000, bbox_inches="tight")

            scores_train.to_csv(save_path + 'training_scoresGMM.csv', header=True, index=False)
            scores_val.to_csv(save_path + 'val_scoresGMM.csv',  header=True, index=False)

        plt.show()

    def benchmarkOtherDataset(self, dataset2, labels1, labels2, params=None, n_regimes=3, save_path=None):
        print(self.df.shape)
        print(dataset2.df.shape)
        if params is None:
            binning_methods = ['Kmeans', 'GMM', 'Density'] # make STD work!
        else:
            binning_methods = params.keys()

        scores_train, scores_val, methods = [], [], []
        n_trees = 1500

        bin_dict1 = {binning_method: self.binData(method=binning_method, n_regimes=n_regimes).df
                    for binning_method in binning_methods}

        bin_dict2 = {binning_method: dataset2.binData(method=binning_method, n_regimes=n_regimes).df
                    for binning_method in binning_methods}

        bin_dict1['Continuous'], bin_dict2['Continuous'] = copy.deepcopy(self.df), copy.deepcopy(dataset2.df)

        for method, dataset in bin_dict1.items():
            print('##########################' + method + '####################################')
            print(dataset.shape)

            test_data = bin_dict2[method]
            print(test_data.shape)

            if dataset.shape[1] != test_data.shape[1]:
                genes_train = set(dataset.columns.values)
                genes_test = set(test_data.columns.values)

                if len(genes_train) > len(genes_test):
                    genediff = genes_train.difference(genes_test)
                    print('Genes that are only present in the training data: ')
                    print(genediff)
                    print(dataset[list(genediff)])

                else:
                    genediff = genes_test.difference(genes_train)
                    print('Genes that are only present in the testing data: ')
                    print(genediff)
                    print(test_data[list(genediff)])

            if method.lower() == 'continuous':
                sd = StandardScaler()
                dataset = sd.fit_transform(dataset)

                test_data = sd.fit_transform(test_data)

            rf = RandomForestClassifier(n_estimators=n_trees)
            rf.fit(dataset, labels1)

            scores_train += [accuracy_score(labels1, rf.predict(dataset))]
            scores_val += [accuracy_score(labels2, rf.predict(test_data))]
            methods += [method]

        results_df = pd.DataFrame({'Training': scores_train,
                                   'Test': scores_val}, index=methods).plot.bar(rot=45)

        return scores_train, scores_val, methods

    def getPosNegPairs(self, dataset2=None, n_batches=1, method='pearson', pos_criterion='5%',
                       neg_criterion='5%', gamma=5, alpha=1):
        if dataset2 is None:
            df2 = None
        else:
            df2 = dataset2.df

        pos, neg = batchPairConstruction(self.df, df2=df2, n_batches=n_batches, method=method,
                                         pos_criterion=pos_criterion, neg_criterion=neg_criterion,
                                         gamma=gamma, alpha=alpha)
        return pos, neg

    def getTrainTestPairs(self, corr_measure='pearson', train_ratio=0.7, neg_pos_ratio=5,
                          sampling_method='balanced', return_summary=True, **kwds):
        '''
        :param corr_measure:
        :param train_ratio:
        :param neg_pos_ratio:
        :param sampling_method:
        :param return_summary:
        :param kwds:
        :return: a tuple containing X_train, X_test, Y_train, Y_test, and optionally a summary of the data
        '''
        pos, _ = batchPairConstruction(self.df, df2=None, method=corr_measure, **kwds)
        graph_ = UndirectedInteractionNetwork(pos, colnames=('Gene_A', 'Gene_B'))
        train_data = graph_.getTrainTestData(train_ratio=train_ratio,
                                             neg_pos_ratio=neg_pos_ratio,
                                             method=sampling_method,
                                             return_summary=return_summary)

        return train_data

def get_optimal_regimes(data1d, max_regimes=2, criterion='bic', penalty=5):
    BIC_min, n_regimes = 1.e20, 1
    gm_best = None

    for regimes in range(1, max_regimes+1):
        gm = GaussianMixture(n_components=regimes, random_state=0) #42
        gm.fit(data1d)
        if criterion.lower() == 'aic':
            bic = gm.aic(data1d)
        elif criterion.lower() == 'rbic':
            bic = rbic(gm, data1d, penalty=penalty)
        else:
            bic = gm.bic(data1d)

        if bic < BIC_min:
            gm_best = gm
            BIC_min = bic
            n_regimes = regimes

    return gm_best, BIC_min, n_regimes

def getGMMRegimes(v, max_regimes, criterion='bic'):
    temp = np.reshape(v, (-1, 1))
    max_val = np.max(temp)
    gm_best, BIC_min, n_regimes = get_optimal_regimes(temp, max_regimes=max_regimes, criterion=criterion)

    if n_regimes == 2:
        labels = gm_best.predict(temp)
        labels = 1*(gm_best.predict(max_val) == labels)
        v_out = labels.astype(np.uint16)
    else:
        labels = gm_best.predict(temp)
        v_out = labels.astype(np.uint16)

    return v_out

def densityDiscretization1D(v, min_clustersize=200, max_nclusters=1000, p_thresh=0.0001, MA_window=1):

    # step 1: calculate distances
    v_sort = np.sort(v)
    v_diff = v_sort[1:] - v_sort[:-1]

    if MA_window > 1:
        window_size = list(np.arange(1, MA_window)) + [MA_window] * len(v_diff) + list(np.arange(MA_window-1, 0, -1))
        ids_begin = [0] * (MA_window - 1) + list(np.arange(len(v_diff))) + [len(v_diff)-1] * (MA_window -1)
        v_diff = np.array([np.sum(v_diff[ids_begin[i]:(window_size[i]+ids_begin[i])])/window_size[i] for i in range(len(ids_begin))])

    pvals = expon.sf(np.max(v_diff), scale=np.mean(v_diff[v_diff < np.percentile(v_diff, q=95)]))

    # step 2: select the areas with the lowest densities
    nclusters = 1
    min_ = np.min(v_diff)
    v_diff[:min_clustersize] = min_
    v_diff[-min_clustersize:] = min_
    v_diff[pvals > p_thresh] = min_
    break_points = []

    while (np.sum(v_diff > min_) > 0) & (nclusters < max_nclusters):
        id_breakpoint = np.argmax(v_diff)
        id_low, id_high = np.minimum(0, id_breakpoint), np.maximum(len(v_diff), id_breakpoint)
        v_diff[id_low:id_high] = min_
        nclusters += 1
        break_points += [v_sort[id_breakpoint]]

    if len(break_points) > 0:
        labels = np.sum(np.array([1 * (break_point < v) for break_point in break_points]), axis=0)
    else:
        labels = np.array([0 for _ in range(len(v))])

    return labels

def rbic(GMMobject, X, penalty=5):
    """Bayesian information criterion for the current model on the input X.
    Parameters
    ----------
    X : array of shape (n_samples, n_dimensions)
    Returns
    -------
    bic : float
        The lower the better.
    """
    return (-2 * GMMobject.score(X) * X.shape[0] +
            penalty * GMMobject._n_parameters() * np.log(X.shape[0]))

def calculateAssociationOther(df, df2=None, method='pearson', alpha=1, gamma=5, as_pairs=False,
                             pos_criterion='5%', neg_criterion='5%'):
        pass

def calculateAssociationSelf(df, method='pearson', alpha=1, gamma=5, as_pairs=False,
                             pos_criterion='5%', neg_criterion='5%'):

    genes_a = df.columns.values

    if method.lower() == 'pearson':
        dist = df.corr(method='pearson').abs()
    elif method.lower() == 'spearman':
        dist = df.corr(method='spearman').abs()
    elif method.lower() == 'kendall':
        dist = df.corr(method='kendall').abs()
    elif method.lower() == 'ranked-pearson':
        dist = df.corr(method='pearson').abs()
        dist = np.argsort(np.absolute(dist), axis=0)
        dist = np.exp(-(np.sqrt(np.transpose(dist) * dist) - alpha)/gamma)
    elif method.lower() == 'ranked-spearman':
        dist = df.corr(method='spearman').abs()
        dist = np.argsort(np.absolute(dist), axis=0)
        dist = np.exp(-(np.sqrt(np.transpose(dist) * dist) - alpha)/gamma)
    elif method.lower() == 'ranked-kendall':
        dist = df.corr(method='kendall').abs()
        dist = np.argsort(np.absolute(dist), axis=0)
        dist = np.exp(-(np.sqrt(np.transpose(dist) * dist) - alpha)/gamma)
    else:
        dist = 0
        raise IOError('The provided method is not known, possible methods are:'
                      '\'pearson\', \'spearman\', \'kendall\','
                      ' \'ranked-pearson\', \'ranked-spearman\', \'ranked-kendall\'.')

    dist = pd.DataFrame(dist, index=genes_a, columns=genes_a)

    if as_pairs:
        pos_pairs, neg_pairs = createPairsFromDistance(dist, upper_criterion=pos_criterion,
                                                       lower_criterion=neg_criterion)
        return pos_pairs, neg_pairs
    else:
        return dist


def checkCriterion(dist_df, criterion):

    N = dist_df.shape[0] * dist_df.shape[1]
    if (isinstance(criterion, str)) and ('%' in criterion):
        criterion = np.float(criterion.split('%')[0])

        if (criterion >= 0) and (criterion <= 100):
            th = np.percentile(dist_df, np.int(criterion), interpolation='lower')
        else:
            raise IOError('Percentages are between 0 and 100.')

    elif (np.float(criterion) > 0) and (np.float(criterion) < 1):
        # assumes the measure is scaled between [0, 1]
        th = criterion

    elif (np.float(criterion) > 0) and (np.float(criterion) < N):
        flat_dist = dist_df.values.flatten()
        th = flat_dist[np.argpartition(flat_dist, np.int(criterion))[np.int(criterion)]]

    else:
        raise IOError('Please provide a valid threshold as input.')

    print(th)

    return th


def createPairsFromDistance(dist_df, upper_criterion='95%', lower_criterion='5%'):
    gene_ids1 = np.array(list(dist_df.index))
    gene_ids2 = dist_df.columns.values

    th_up = checkCriterion(dist_df, upper_criterion)
    th_down = checkCriterion(dist_df, lower_criterion)

    dist_df = dist_df.values

    if np.allclose(dist_df.T, dist_df):
        r, c = np.triu_indices(dist_df.shape[0], k=1)
        dist_df = dist_df[(r, c)]
        genes1 = gene_ids1[r]
        genes2 = gene_ids2[c]

        ids = np.where(dist_df > th_up)
        gene1_pos = genes1[ids]
        gene2_pos = genes2[ids]
        association = dist_df[ids]

        pos_df = pd.DataFrame({'Gene_A': gene1_pos, 'Gene_B': gene2_pos, 'Association Strength': association})

        ids = np.where(dist_df < th_down)
        gene1_neg = genes1[ids]
        gene2_neg = genes2[ids]
        association = dist_df[ids]
        neg_df = pd.DataFrame({'Gene_A': gene1_neg, 'Gene_B': gene2_neg, 'Association Strength': association})

    else:
        r_ids, c_ids = np.where(dist_df > th_up)
        gene1_pos = gene_ids1[r_ids]
        gene2_pos = gene_ids2[c_ids]
        association = dist_df[r_ids, c_ids]
        pos_df = pd.DataFrame({'Gene_A': gene1_pos, 'Gene_B': gene2_pos, 'Association Strength': association})

        r_ids, c_ids = np.where(dist_df < th_down)
        gene1_neg = gene_ids1[r_ids, c_ids]
        gene2_neg = gene_ids2[r_ids, c_ids]
        association = dist_df.values[r_ids, c_ids]

        neg_df = pd.DataFrame({'Gene_A': gene1_neg, 'Gene_B': gene2_neg, 'Association Strength': association})

    return pos_df, neg_df


def batchPairConstruction(df1, df2=None, n_batches=1, method='pearson', pos_criterion='5%', neg_criterion='5%', **kwds):
    # TODO: parallelize
    if df2 is None:
        n_cols = df1.shape[1]
        break_points = np.linspace(0, n_cols, num=n_batches+1, dtype=np.int)

        pos_pairs, neg_pairs = [], []

        for i in range(len(break_points) - 1):
            for j in range(i + 1):
                pos_, neg_ = calculateAssociationSelf(df1.iloc[:, break_points[i]:break_points[i + 1]],
                                                 method=method, as_pairs=True, pos_criterion=pos_criterion,
                                                 neg_criterion=neg_criterion, **kwds)
                print(neg_)
                print(pos_)
                pos_pairs += [pos_]
                neg_pairs += [neg_]
    else:
        n_cols1, n_cols2 = df1.shape[1], df2.shape[1]
        break_points1 = np.linspace(0, n_cols1, num=n_batches+1, dtype=np.int)
        break_points2 = np.linspace(0, n_cols2, num=n_batches+1, dtype=np.int)

        pos_pairs, neg_pairs = [], []

        for i in range(len(break_points1) - 1):
            for j in range(len(break_points2) - 1):
                pos_, neg_ = calculateAssociationOther(df1.iloc[:, break_points1[i]:break_points1[i + 1]],
                                     df2.iloc[:, break_points2[j]:break_points2[j + 1]],
                                     method=method, as_pairs=True, pos_criterion=pos_criterion,
                                     neg_criterion=neg_criterion, **kwds)
                pos_pairs += [pos_]
                neg_pairs += [neg_]

    pos_pairs = pd.concat(pos_pairs, axis=0, ignore_index=True)
    neg_pairs = pd.concat(neg_pairs, axis=0, ignore_index=True)

    return pos_pairs, neg_pairs
