import pandas as pd
import numpy as np
import copy
import warnings

class OmicsDataSet():

    @classmethod
    def from_file(cls, path, type='Omics', sep=',', header=0, column_index=0, patient_axis='auto',
                  remove_nas=True, remove_zv=True):
        data_df = pd.read_csv(path, sep=sep, header=header, index_col=column_index)
        return cls(data_df, patient_axis=patient_axis, remove_nas=remove_nas, type=type, remove_zv=remove_zv)

    def __init__(self, dataframe, patient_axis='auto', remove_nas=True,
                 type='', remove_zv=False, verbose=True, average_dup_samples=False,
                 average_dup_genes=False):

        if str(patient_axis).lower() == 'auto':
            if dataframe.shape[0] > dataframe.shape[1]:
                dataframe = dataframe.transpose()

        elif patient_axis == 1:
            dataframe = dataframe.transpose()

        if remove_nas:
            dataframe = dataframe.dropna(axis=1, how='any', inplace=False)

        samples_ = [str(s) for s in list(dataframe.index)]
        genes_ = [str(s) for s in list(dataframe.columns)]

        if len(samples_) > len(set(samples_)):
            warnings.warn('Duplicated index entries found.', UserWarning)
            if average_dup_samples:
                old_shape = dataframe.shape[1]
                dataframe = dataframe.groupby(samples_).mean()
                new_shape = dataframe.shape[1]
                print('Removed %i rows by averaging.' % (old_shape - new_shape))

        if len(genes_) > len(set(genes_)):
            warnings.warn('Duplicated column entries found.', UserWarning)
            if average_dup_genes:
                old_shape = dataframe.shape[1]
                dataframe = dataframe.transpose().groupby(genes_).mean().transpose()
                new_shape = dataframe.shape[1]

                print('Removed %i columns by averaging.' % (old_shape - new_shape))

        self.df = dataframe
        self.df.columns = [str(s) for s in list(dataframe.columns)]
        self.df.index = [str(s) for s in list(dataframe.index)]

        if remove_zv:
            self.removeZeroVarianceGenes()

        if verbose:
            print('Number of samples %d, number of genes %d' % (len(self.samples()), len(self.genes())))

        self.type = type

        if (type == '') or (type is None):
            print('Please provide an identifier for the type of data stored in the dataset (EXP, MUT, CNA, PROT).')

    def samples(self, as_set=False):
        samples = list(self.df.index)
        if as_set:
            return set(samples)
        else:
            return np.array(samples)

    def genes(self, as_set=False):
        genes = list(self.df.columns)
        if as_set:
            return set(genes)
        else:
            return np.array(genes)

    def subsetGenes(self, genes, inplace=False):
        if inplace:
            self.df = self.df[genes]
        else:
            return self.df[genes]

    def subsetSamples(self, samples, inplace=False):
        if inplace:
            self.df = self.df.loc[samples]
        else:
            return self.df.loc[samples]

    def getCommonGenes(self, datasets, extra_gene_list=None, as_set=False):

        try:
            _ = len(datasets)

        except TypeError:  # convert to iterable
            datasets = [datasets]

        intersecting_genes = self.genes(as_set=True)

        if extra_gene_list is not None:
            intersecting_genes = intersecting_genes.intersection(set(extra_gene_list))

        for dataset in datasets:
            intersecting_genes = intersecting_genes.intersection(dataset.genes(as_set=True))

        if as_set:
            return intersecting_genes
        else:
            return list(intersecting_genes)

    def getCommonSamples(self, datasets, extra_sample_list=None, as_set=False):

        try:
            _ = len(datasets)

        except TypeError:  # convert to iterable
            datasets = [datasets]

        intersecting_samples = self.samples(as_set=True)

        if extra_sample_list is not None:
            intersecting_samples = intersecting_samples.intersection(set(extra_sample_list))

        for dataset in datasets:
            intersecting_samples = intersecting_samples.intersection(dataset.samples(as_set=True))

        if as_set:
            return intersecting_samples
        else:
            return list(intersecting_samples)

    def keepCommonSamples(self, datasets, extra_sample_list=None, inplace=False):

        intersecting_samples = self.getCommonSamples(datasets, extra_sample_list=extra_sample_list)
        
        if inplace:
            for dataset in datasets:
                dataset.subsetSamples(intersecting_samples, inplace=True)

            self.subsetSamples(intersecting_samples, inplace=True)
        else:
            datasets = [d.subsetSamples(intersecting_samples, inplace=False) for d in datasets]
            self_df = self.subsetSamples(intersecting_samples, inplace=False)
            return [self_df] + datasets

    def keepCommonGenes(self, datasets, extra_gene_list=None, inplace=False):
        intersecting_genes = self.getCommonGenes(datasets, extra_gene_list=extra_gene_list)

        if inplace:
            for dataset in datasets:
                dataset.subsetGenes(intersecting_genes, inplace=True)

            self.subsetGenes(intersecting_genes, inplace=True)

        else:
            datasets = [d.subsetGenes(intersecting_genes, inplace=False) for d in datasets]
            self_df = self.subsetGenes(intersecting_genes, inplace=False)
            return [self_df] + datasets

    def mapGeneIDs(self, gene_map,  method='strict', average_duplicates=False):

        '''
        :param patient_map: a dictionary mapping olds patient identifiers onto new ones
        :param the method that is used for the mapping, can be one of the three following:
                - 'strict' (default): raises an error if old patient ids have no new equivalent.
                - 'lossy' removes the old patients that are not mapped onto new ids.
                - 'conservative' keeps the old ids for patients that can not be mapped.
        '''

        if method.lower() == 'lossy':  # throw away all interactions of which at least one gene can not be mapped
            old_N_samples = len(self.genes())
            self.df = self.df.loc[:, [x in set(gene_map.keys()) for x in self.df.columns]]
            self.df.columns = [gene_map[x] for x in self.df.columns]
            print(str(old_N_samples - len(self.genes())) + ' genes have been removed')

        elif method.lower() == 'conservative':
            self.df.columns = [gene_map[x] if x in gene_map.keys() else x for x in self.df.columns]

        else:
            try:
                self.df.columns = [str(gene_map[x]) for x in self.genes()]
            except KeyError:
                print('Not all old sample IDs are mapped onto new IDs. Specify method=\'lossy\' to allow '
                      'for lossy mapping, or method=\'conservative\' to keep old IDs when no new ID is known.')

        unique_new_genes = list(self.genes(as_set=True))
        # check if the new genes are unique, otherwise we average over the IDs that are duplicate
        if (len(self.genes()) > len(unique_new_genes)):
            warnings.warn('The new genes contain %i duplicate IDs.'
                          % (len(self.genes()) - len(unique_new_genes)), UserWarning)

            if average_duplicates:
                print('Averaging over duplicate IDs')
                self.df = self.df.transpose().groupby(unique_new_genes).mean().transpose()

    def mapSampleIDs(self, patient_map, average_duplicates=False, method='strict'):
        '''
        :param patient_map: a dictionary mapping olds patient identifiers onto new ones
        :param the method that is used for the mapping, can be one of the three following:
                - 'strict' (default): raises an error if old patient ids have no new equivalent.
                - 'lossy' removes the old patients that are not mapped onto new ids.
                - 'conservative' keeps the old ids for patients that can not be mapped.
        '''

        if method.lower() == 'lossy':  # throw away all interactions of which at least one gene can not be mapped
            old_N_samples = len(self.samples())
            self.df = self.df.loc[[x in set(patient_map.keys()) for x in self.df.index]]
            self.df.index = [patient_map[x] for x in self.df.index]
            print(str(old_N_samples - len(self.samples())) + ' samples have been removed')

        elif method.lower() == 'conservative':
            self.df.index = [patient_map[x] if x in patient_map.keys() else x for x in self.df.index]

        else:
            try:
                self.df.index = [str(patient_map[x]) for x in self.samples()]
            except KeyError:
                print('Not all old sample IDs are mapped onto new IDs. Specify method=\'lossy\' to allow '
                      'for lossy mapping, or method=\'conservative\' to keep old IDs when no new ID is known.')

        unique_new_genes = list(self.genes(as_set=True))
        if (len(self.genes()) > len(unique_new_genes)):
            warnings.warn('The new genes contain %i duplicate IDs.'
                          % (len(self.genes()) - len(unique_new_genes)), UserWarning)

            if average_duplicates:
                print('Averaging over duplicate IDs')
                self.df = self.df.transpose().groupby(unique_new_genes).mean().transpose()

    def changeGeneIDs(self, gene_list):
        self.df.columns = gene_list

    def changeSampleIDs(self, sample_list):
        self.df.index = sample_list

    def GetSampleDistances(self, norm):
        pass

    def GetGeneDistances(self, norm):
        pass

    def mean(self, axis=0):
        return self.df.mean(axis=axis)

    def max(self, axis=0):
        return self.df.max(axis=axis)

    def min(self, axis=0):
        return self.df.min(axis=axis)

    def sum(self, axis=0):
        return self.df.sum(axis=axis)

    def std(self, axis=0):
        return self.df.std(axis=axis)

    def print(self, ntop=5):
        print(self.df.head(ntop))

    def to_nparray(self):
        return self.df.values

    def unique(self):
        return pd.unique(self.df.values.ravel('K'))

    def equals(self, dataset2):
        return self.df.equals(dataset2.df)

    def loc(self, samples):
        self.df = self.df.loc[samples]

    def get_all_pairs(self, include_type=False, colnames=('Samples', 'Genes')):
        '''
        Returns a df of two columns listing all sample-gene pairs that have a non-zero entry
        '''
        Genes, Samples = self.genes(), self.samples()
        row_ids, col_ids = np.where(self.df.values != 0)

        if include_type:
            Genes = np.array([gene + ' ' + self.type for gene in Genes])
            Samples = np.array([sample + ' ' + 'PAT' for sample in Samples])

        return pd.DataFrame({colnames[0]: Samples[row_ids], colnames[1]: Genes[col_ids]})

    def removeZeroVarianceGenes(self):
        mask = self.std(axis=0).values > 1e-15
        nzv_genes = self.genes()[mask]
        self.df = self.df[nzv_genes]

    def concatDatasets(self, datasets, axis=1, include_types=True):
        try:
            _ = len(datasets)

        except TypeError:  # convert to iterable
            datasets = [datasets]

        datasets = datasets + [self]
        datasets2 = [copy.deepcopy(dataset) for dataset in datasets]

        if include_types:

            for dataset in datasets2:
                dataset.mapGeneIDs({gene: gene + ' ' + dataset.type for gene in dataset.genes()})

        DF = pd.concat([dataset.df for dataset in datasets2], axis=axis)

        return DF

    def __getitem__(self, item):
        return OmicsDataSet(self.df.iloc[item], type=self.type, remove_zv=False, patient_axis=0, verbose=False)

    def deepcopy(self):
        return copy.deepcopy(self)

    def logtransform(self, base=2):
        epsilon = 1.e-15
        self.df = np.log(self.df + epsilon) / np.log(base)
