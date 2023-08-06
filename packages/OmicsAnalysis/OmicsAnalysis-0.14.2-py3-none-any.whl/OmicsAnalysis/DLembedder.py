import pandas as pd
import numpy as np
import copy
import warnings
from keras.layers import Embedding, Input, Dense, Flatten, Dropout, Lambda
from keras.models import Model, save_model
from keras.losses import binary_crossentropy
from keras.callbacks import EarlyStopping
from sklearn.metrics import roc_auc_score, precision_score, accuracy_score, average_precision_score, precision_recall_curve
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
import pandas as pd
import keras.backend as K
import tensorflow as tf
import pdb
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp, mannwhitneyu
from statsmodels.stats.multitest import multipletests


class DLembedder:
    def __init__(self, N_nodes, embed_dim, nodes_per_layer=[None],
                 activations_per_layer=[None],
                 seq_length=2,  dropout=0.2, merge_method='flatten', int2genedict=None):
        '''
        :param N_nodes: The number of genes for which to train embeddings
        :param embed_dim: The embedding dimension
        :param layers_per_model: The number of hidden layers, *including* the output layer. If the model will be used to predict multiple outputs, then
        this value should be a dictionary {output_type1: [n_nodes_hidden_layer1, n_nodes_hidden_layer2],
         output_type2: ...}, for single output models a single iterable containing ints suffices (e.g. [32, 32, 1]
        :param seq_length: The length of a sequence (default is sequences of 2)
        :param dropout: the amount of dropout to apply
        :param merge_method: how to obtain an edge representation from the two gene representations
        '''

        # First we check the input variables and convert them to dicts
        nodes_per_layer = checkInputIterable(nodes_per_layer, int, input_name='nodes_per_layer',
                                                   type_name='Integer', new_model_name='Single_Output_Model')

        activations_per_layer = checkInputIterable(activations_per_layer, str, input_name='activations_per_layer',
                                                   type_name='String', new_model_name='Single_Output_Model')

        # Check that the nodes and activation have the same model names and the same number of layers
        compareDictsOfIterables(nodes_per_layer, activations_per_layer, dict1_name='Nodes', dict2_name='Activations')

        # Then we can safely start building the architecture of the model
        embedding_layer = Embedding(input_dim=N_nodes, output_dim=embed_dim, input_length=seq_length)
        sequence_input = Input(shape=(seq_length,), dtype='int32')
        embedded_sequences = embedding_layer(sequence_input)

        if merge_method.lower() == 'flatten':
            x = Flatten()(embedded_sequences)
        elif merge_method.lower() == 'average':
            av_layer = Lambda(average_, output_shape=[embed_dim])
            x = av_layer(embedded_sequences)
        elif merge_method.lower() == "hadamard":
            h_layer = Lambda(hadamard, output_shape=[embed_dim])
            x = h_layer(embedded_sequences)
        elif merge_method.lower() == "difference":
            diff_layer = Lambda(diff, output_shape=[embed_dim])
            x = diff_layer(embedded_sequences)
        else:   # TODO: try other merging methods
            diff_layer = Lambda(lambda X: np.abs(X[:, 1] - X[:, 0]), output_shape=[embed_dim])
            x = diff_layer(embedded_sequences)

        outputs = []

        for modelname, hidden_layers in nodes_per_layer.items():

            try:
                for layer, n_nodes in enumerate(hidden_layers):
                    if layer == (len(hidden_layers) - 1):  # last layer needs to have a name
                        preds = Dense(n_nodes, activation=activations_per_layer[modelname][layer], name=modelname)(x)
                        outputs += [preds]
                    else:
                        x = Dense(n_nodes, activation=activations_per_layer[modelname][layer])(x)
                        x = Dropout(dropout)(x)
            except:
                warnings.warn('Please provide the number of nodes per hidden layer as a dictionary containing'
                              ' arrays of integers.')

            self.model = Model(inputs=sequence_input, outputs=outputs)

        self.embedding_dim = embed_dim
        self.seq_length = seq_length
        self.embedding_layer = embedding_layer
        self.nodes = nodes_per_layer
        self.activations = activations_per_layer
        self.model_names = list(self.activations.keys())
        self.n_models = len(self.model_names)
        self.counter = 0
        self.voc_size = N_nodes
        self.int2gene = int2genedict


    def fit(self, X_train, Y_train, validation_data=None, validation_split=0.2, optimizer='adam',
            loss='binary_crossentropy', return_history=False, verbose=2, batch_size=32,
            n_epochs=10, callbacks="default", predefined_embeddings=None, lossWeights=None,
            metrics=['accuracy'], allow_nans=True):

        # Check the training and test data
        Y_train = checkInputDict(Y_train, np.ndarray, self.model_names, inputname='Training labels', allowed_type_name='Numpy array')

        if validation_data is not None:
            validation_labels = checkInputDict(validation_data[1], np.ndarray, self.model_names,
                                                inputname='Test labels', allowed_type_name='Numpy array')

            validation_data = (validation_data[0], validation_labels)
        # Check the loss and the metrics
        loss = checkInputDict(loss, str, self.model_names,
                                                inputname='Losses', allowed_type_name='String')
        metrics = checkInputDict(metrics, str, self.model_names,
                                                inputname='Metrics', allowed_type_name='String')
        if lossWeights is None:
            lossWeights = 1.

        lossWeights = checkInputDict(lossWeights, float, self.model_names,
                                                inputname='Loss weights', allowed_type_name='float')

        if predefined_embeddings is not None:
            self.embedding_layer.set_weights([predefined_embeddings])
        # If the user allows for NaNs we map every loss/metric to a user-friendly version
        if allow_nans:
            try:
                loss = {model: LOSSMAPPER[loss_] for model, loss_ in loss.items()}
            except KeyError:
                raise KeyError('There is not yet an NaN proof version for all provided losses.'
                               ' Implemented NaN metrics are: %s' %', '.join(list(LOSSMAPPER.keys())))

            try:
                metrics = {model: LOSSMAPPER[metric_] for model, metric_ in metrics.items()}
            except KeyError:
                raise KeyError('There is not yet an NaN proof version for all provided losses.'
                               ' Implemented NaN metrics are: %s' %', '.join(list(LOSSMAPPER.keys())))

        # initialize the optimizer and compile the model
        if self.counter == 0:
            print("Compiling the model...")
            print(loss)
            print(metrics)
            self.model.compile(optimizer=optimizer, loss=loss, loss_weights=lossWeights, metrics=metrics)
            self.counter += 1 # To keep the learning rate to its old value

        if str(callbacks).lower() == 'default':
            if validation_data is not None:
                callbacks = [EarlyStopping(monitor='val_loss', patience=1, verbose=0, mode='auto')]
            else:
                callbacks = None

        if validation_data is not None:
            validation_split = 0.

        print("Training the model...")
        history = self.model.fit(X_train, Y_train, epochs=n_epochs, validation_data=validation_data,
                                 validation_split=validation_split,
                                 callbacks=callbacks, batch_size=batch_size, verbose=verbose)

        if return_history:
            return history


    def fit_generator(self, Generator, validation_data=None, validation_split=0.2, optimizer='adam',
            loss='binary_crossentropy', return_history=False, verbose=2, steps_per_epoch=10,
            n_epochs=10, callbacks="default", predefined_embeddings=None, lossWeights=None,
            metrics=['accuracy'], allow_nans=True, use_multiprocessing=False, workers=1):

        if validation_data is not None:
            validation_labels = checkInputDict(validation_data[1], np.ndarray, self.model_names,
                                                inputname='Test labels', allowed_type_name='Numpy array')

            validation_data = (validation_data[0], validation_labels)
        # Check the loss and the metrics
        loss = checkInputDict(loss, str, self.model_names,
                                                inputname='Losses', allowed_type_name='String')
        metrics = checkInputDict(metrics, str, self.model_names,
                                                inputname='Metrics', allowed_type_name='String')
        if lossWeights is None:
            lossWeights = 1.

        lossWeights = checkInputDict(lossWeights, float, self.model_names,
                                                inputname='Loss weights', allowed_type_name='float')

        if predefined_embeddings is not None:
            self.embedding_layer.set_weights([predefined_embeddings])
        # If the user allows for NaNs we map every loss/metric to a user-friendly version
        if allow_nans:
            try:
                loss = {model: LOSSMAPPER[loss_] for model, loss_ in loss.items()}
            except KeyError:
                raise KeyError('There is not yet an NaN proof version for all provided losses.'
                               ' Implemented NaN metrics are: %s' %', '.join(list(LOSSMAPPER.keys())))

            try:
                metrics = {model: LOSSMAPPER[metric_] for model, metric_ in metrics.items()}
            except KeyError:
                raise KeyError('There is not yet an NaN proof version for all provided losses.'
                               ' Implemented NaN metrics are: %s' %', '.join(list(LOSSMAPPER.keys())))

        # initialize the optimizer and compile the model
        if self.counter == 0:
            print("Compiling the model...")
            print(loss)
            print(metrics)
            self.model.compile(optimizer=optimizer, loss=loss, loss_weights=lossWeights, metrics=metrics)
            self.counter += 1 # To keep the learning rate to its old value

        if str(callbacks).lower() == 'default':
            if validation_data is not None:
                callbacks = [EarlyStopping(monitor='val_loss', patience=1, verbose=0, mode='auto')]
            else:
                callbacks = None

        print("Training the model...")
        history = self.model.fit_generator(generator=Generator,
                                           steps_per_epoch=steps_per_epoch,
                                           use_multiprocessing=use_multiprocessing,
                                           workers=workers,
                                           verbose=2,
                                           callbacks=callbacks,
                                           validation_data=validation_data,
                                           epochs=n_epochs)

        if return_history:
            return history

    def modelSave(self, fpath):
        return save_model(self, fpath)

    def getEmbeddings(self):
        return np.asarray(self.embedding_layer.get_weights())[0]

    def predict_proba(self, X):
        return self.model.predict(X)

    def predict(self, X):
        return np.round(self.model.predict(X)).astype(np.int)

    def predictProbMatrix(self, sources, targets):
        '''
        Predicts the output as a node list
        :param sources: A list of nodenames
        :param targets: A list of nodenames
        :return: a DF (len(sources) x len(targets) containing the interaction probabilities between the nodes

        '''

        gene2int = {gene: i for i, gene in self.int2gene.items()}

        try:
            sources_ints = [gene2int[node] for node in sources if node in gene2int.keys()]
            targets_ints = [gene2int[node] for node in targets if node in gene2int.keys()]

        except KeyError:
            raise KeyError('The provided list needs to contain the strings with the nodenames.')

        input = np.transpose(np.vstack((np.repeat(sources_ints, len(targets_ints)),
                                        np.tile(targets_ints, len(sources_ints)))))

        probs = self.predict_proba(input).flatten()
        prob_mat = pd.DataFrame(np.reshape(probs, (len(sources_ints), len(targets_ints)), order='F'),
                                columns=targets,
                                index=sources)
        return prob_mat

    def getModelPerformance(self, X, Y_true, metric='AUC'):
        preds = self.predict_proba(X)

        if metric.lower() == 'auc':
            score = roc_auc_score(Y_true, preds)
            fpr, tpr, _ = roc_curve(Y_true, preds)
            print('The %s score of the model is: %f' % (metric, score))
            return score, fpr, tpr
        elif metric.lower() == 'precision':
            score = average_precision_score(Y_true, preds)
            pr, recall, _ = precision_recall_curve(Y_true, preds)
            print('The %s score of the model is: %f' % (metric, score))
            return score, pr, recall
        else:
            #pdb.set_trace()
            score = accuracy_score(Y_true, (preds>0.5).astype(np.int_))
            print('The %s score of the model is: %f' % (metric, score))
            return score


    def getNodeEnrichment(self, node_int, genelist_ints, num_permutations=100000, random_state=42, include_pval=True,
                          agg_score='mean', testtype='mannwhitney'):

        np.random.seed(42)
        genelist_ints = np.array(genelist_ints)

        probs = self.getNodeProbs(node_int=node_int)
        list_probs = probs[genelist_ints]

        if agg_score.lower() == 'prob':
            score = np.prod(list_probs) ** (1 / len(genelist_ints))
        else:
            score = np.sum(list_probs) / np.sum(probs)

        other_ints = np.setdiff1d(np.arange(self.voc_size), genelist_ints)

        if testtype == 'ks':
            D, p_val = ks_2samp(probs[other_ints], list_probs)
        else:
            U, p_val = mannwhitneyu(list_probs, probs[other_ints], alternative='both')


        if include_pval:

            if agg_score.lower() == 'prob':
                random_scores = np.array([np.prod(probs[np.random.choice(self.voc_size, len(genelist_ints), replace=False)])
                                      for _ in range(num_permutations)])
            else:
                random_scores = np.array([np.mean(probs[np.random.choice(self.voc_size, len(genelist_ints), replace=False)])
                                      for _ in range(num_permutations)])
            p_val = np.sum(random_scores >= score)/len(random_scores)

            return score, p_val

        else:
            return score


    def getNodeProbs(self, node_int, genelist_ints=None):

        if genelist_ints is None:
            genelist_ints = np.arange(self.voc_size)
        else:
            genelist_ints = np.array(genelist_ints)

        pair_ints = np.zeros((len(genelist_ints), 2))
        pair_ints[:, 1] = genelist_ints
        pair_ints[:, 0] = node_int
        probs = self.predict_proba(pair_ints).flatten()

        return probs

    def runDiscreteEnrichment(self, pathways_ints, genelist_ints, Nperm=10000,
                              agg_score='mean', testtype='mw'):

        all_probs = np.vstack([self.getNodeProbs(gene) for gene in pathways_ints])  # pathways x nodes

        genelist_ints = np.array(genelist_ints)
        probs_list = all_probs[:, genelist_ints]
        gene_ints = np.setdiff1d(np.arange(self.voc_size), pathways_ints)

        if agg_score.lower() == 'prob':
            score = np.prod(probs_list, axis=1) ** (1 / len(genelist_ints))

        else:
            score = np.sum(probs_list, axis=1) / np.sum(all_probs[:, gene_ints], axis=1)

        if self.int2gene is not None:
            pathways_ints = [self.int2gene[i] for i in pathways_ints]

        output_dict = {'Pathway': pathways_ints}
        output_dict['Score'] = score

        if testtype == 'mw':
            other_genes = np.setdiff1d(gene_ints, genelist_ints)
            output_dict['Pval'] = [
                mannwhitneyu(probs_list[i, :], all_probs[i, :][other_genes], alternative='greater')[1]
                for i in range(len(pathways_ints))]
        elif testtype == 'ks':
            other_genes = np.setdiff1d(gene_ints, genelist_ints)
            output_dict['Pval'] = [ks_2samp(probs_list[i, :], all_probs[i, :][other_genes])[1]
                                   for i in range(len(pathways_ints))]
        else:  # testtype == 'permute':

            random_scores = np.zeros((len(score), Nperm))

            for n in range(Nperm):
                random_genes = np.random.choice(gene_ints, len(genelist_ints), replace=False)
                perm_probs = all_probs[:, random_genes]
                random_scores[:, n] = np.sum(perm_probs, axis=1) / np.sum(all_probs[:, gene_ints], axis=1)

            score = score[..., None]
            output_dict['Pval'] = np.sum(random_scores >= score, axis=1) / Nperm

        _, output_dict['FDR'], _, _ = multipletests(output_dict['Pval'], method='fdr_bh')

        return pd.DataFrame(output_dict).sort_values(by='Score', ascending=False)

    def runContinuousEnrichment(self, pathways_ints, score_df,
                                agg_score='mean', testtype='permute', Nperm=10000):

        genelist_ints = np.array(list(score_df.index))
        all_probs = np.vstack([self.getNodeProbs(gene) for gene in pathways_ints])  # pathways x genes

        probs_list = all_probs[:, genelist_ints]
        gene_ints = np.setdiff1d(np.arange(self.voc_size), pathways_ints)

        scores = np.dot(probs_list, score_df.values).flatten() / np.sum(probs_list, axis=1)

        if self.int2gene is not None:
            pathways_ints = [self.int2gene[i] for i in pathways_ints]

        output_dict = {'Pathway': pathways_ints}
        output_dict['Score'] = scores

        random_scores = np.zeros((len(scores), Nperm))

        shuffles = score_df.values

        print(shuffles.shape)

        if testtype == 'permute':
            for n in range(Nperm):
                np.random.shuffle(shuffles)
                random_scores[:, n] = np.dot(probs_list, shuffles).flatten() / np.sum(probs_list, axis=1)

            scores = scores[..., None]
            p_vals = np.sum(random_scores >= scores, axis=1) / Nperm
            print(p_vals.shape)

            output_dict['Pval'] = p_vals
            _, output_dict['FDR'], _, _ = multipletests(p_vals, method='fdr_bh')

        return pd.DataFrame(output_dict).sort_values(by='Score', ascending=False)

    def plotProbHistogram(self, gene_int, genelist=None, plot_title='', binsize=100, savepath=None,
                          normalize=True, font=16, save_path=None):

        pair_ints = np.zeros((self.voc_size, 2))
        pair_ints[:, 1] = np.arange(self.voc_size)
        pair_ints[:, 0] = gene_int

        probs = self.predict_proba(pair_ints).flatten()

        print(probs.shape)

        bin_size = np.linspace(0, 1, num=binsize)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(probs, density=normalize, bins=bin_size, alpha=0.5)

        if genelist is not None:
            genelist = np.array(genelist)
            probs_list = probs[genelist]
            ax.hist(probs_list, density=normalize, bins=bin_size, alpha=0.5)

        plt.xlabel('Probability', fontsize=font)
        plt.ylabel('Frequency')
        plt.title(plot_title)

        if save_path is not None:
            plt.savefig(save_path)

        plt.show()
        return probs

'''
    def getErnichmentScore(self, path_dict, genelist,  num_permutations=100000, random_state=42):
        
        max_len = max([len(v) for v in path_dict.values()])
        
        for path in path_dict.keys():
            for 
        
        
        return 
'''

### Helper functions to check inputs

def checkIterableType(iterable, expected_type, input_name='', type_name= ''):
    '''
    Checks whether all elements in a iterable belong to an expected_type (e.g. int, str, ...). returns an error if
    not all elements in the iterable are of expected_type or if the iterable is in fact not an iterable.
    :param iterable: a iterable, returns an error if there can be iterated over this object
    :param expected_type: the expected type for all elements of the iterable
    :param input_name: a string specifying what the iterable represents in the model,
     used to create more informative errors
    :param type_name: A string specifying the expected_type, used to create more informative errors
    '''
    try:
        bools = [isinstance(x, expected_type) for x in iterable]
    except TypeError:
        raise TypeError('Input ' + input_name + ' expected to be an iterable.')

    assert sum(bools) == len(bools), 'Input ' + input_name + ' should consist of all ' + type_name


def checkInputIterable(iterable, expected_type, input_name='', type_name= '', new_model_name='Single_Output_Model'):
    '''
    Checks if an object is a dict or not. If the object is a dict, then all values are verified to be arrays consisting of
    expected type. If the object is another type of iterable, then every element is checked to belong to be of expected_type
    The iterable is converted to a dictionary {new_model_name: iterable}
    :param iterable: a iterable, returns an error if there can be iterated over this object
    :param expected_type: the expected type for all elements of the iterable
    :param input_name: a string specifying what the iterable represents in the model,
     used to create more informative errors
    :param type_name: A string specifying the expected_type, used to create more informative errors
    :param new_model_name:
    :return: a dictionary containing arrays of expected_type
    '''
    if isinstance(iterable, dict):
        for model_, activations_ in iterable.items():
            checkIterableType(activations_, expected_type, input_name=input_name, type_name=type_name)
        return iterable
    else:
        checkIterableType(iterable, expected_type, input_name=input_name, type_name=type_name)
        iterable = {new_model_name: iterable}

        return iterable

def compareDictsOfIterables(dict1, dict2, dict1_name='', dict2_name=''):
    '''
    Compares if two dicts (with iterables as values) have the same keys and whether the arrays are of the same length
    :param dict1: a dictionary to be compared
    :param dict2: a second dictionary to be compared
    :param dict1_name: a string specifying the name of the first dictionary, used for generating more precise errors
    :param dict2_name: a string specifying the name of the first dictionary, used for generating more precise errors
    '''
    try:
        bools = [len(dict1[k]) == len(dict2[k]) for k, v in dict1.items()]
    except KeyError:
        raise KeyError('The modelnames of %s and %s are not consistent.' % (dict1_name, dict2_name))
    except TypeError:
        raise TypeError('All iterables specifying %s and %s should be lists or np.arrays.' % (dict1_name, dict2_name))

    assert sum(bools) == len(bools), 'The number of ' + dict1_name + ' and ' + dict2_name +\
                                     ' are not consistent across all models.'

def checkInputDict(input, allowed_type, modelnames, inputname, allowed_type_name=''):
    '''
    Checks if an input is dict consisting of values of allowed_type and keys equal to modelnames,
    else if the input is a scalar, it is converted to a dict, where all the keys are modelnames,
    all of which map to input.
    :param input: a dict or an object of allowed_type
    :param allowed_type: The allowed type() for an instance of input (when a dict), or input dict (when a scalar)
    :param modelnames: keys of the new dict when input is a scalar
    :param inputname: a string speficying the name of the input, used for more informative errors
    :param allowed_type_name:
    :return: a dictionary, all elements of which belong to allowed_type and keys are given by modelnames
    '''
    if isinstance(input, dict):
        assert set(list(input.keys())) == set(modelnames), \
            'The modelnames of ' + inputname + ' are not consistent with the model'

        bools = [isinstance(v, allowed_type) for model, v in input.items()]

        assert sum(bools) == len(bools), \
            'The types of ' + inputname + ' are not all ' + allowed_type_name

        return input
    elif isinstance(input, allowed_type):
        return {modelname_: input for modelname_ in  modelnames}
    else:
        raise IOError('The input ' + inputname + ' should be a dictionary or a ' + allowed_type_name)


### Masking versions of the loss functions from keras
def diff(X):
    return X[:, 0] - X[:, 1]

def average_(X):
    return (X[:, 0] + X[:, 1]) / 2.0

def hadamard(X):
    return X[:,0] * X[:,1]

def binary_crossentropy_masked(y_true, y_pred):
    mask = ~tf.is_nan(y_true)
    y_pred = tf.boolean_mask(y_pred, mask)
    y_true = tf.boolean_mask(y_true, mask)
    return K.sum(K.binary_crossentropy(y_true, y_pred), axis=-1)

def binary_accuracy_masked(y_true, y_pred):
    mask = ~tf.is_nan(y_true)
    y_pred = tf.boolean_mask(y_pred, mask)
    y_true = tf.boolean_mask(y_true, mask)
    return K.mean(K.equal(y_true, K.round(y_pred)), axis=-1)

def categorical_crossentropy_masked(y_true, y_pred): # Not working at the moment, error during backpropagation
    mask = ~tf.is_nan(K.sum(y_true, axis=1))
    y_pred = tf.boolean_mask(y_pred, mask)
    y_true = tf.boolean_mask(y_true, mask)
    return K.categorical_crossentropy(y_true, y_pred)

def categorical_accuracy_masked(y_true, y_pred):
    mask = ~tf.is_nan(K.sum(y_true, axis=1))
    y_pred = tf.boolean_mask(y_pred, mask)
    y_true = tf.boolean_mask(y_true, mask)
    return K.cast(K.equal(K.argmax(y_true, axis=-1),
                          K.argmax(y_pred, axis=-1)),
                  K.floatx())

def top_k_categorical_accuracy_masked(y_true, y_pred, k=5):
    mask = ~tf.is_nan(K.sum(y_true, axis=1))
    y_pred = tf.boolean_mask(y_pred, mask)
    y_true = tf.boolean_mask(y_true, mask)
    return K.mean(K.in_top_k(y_pred, K.argmax(y_true, axis=-1), k), axis=-1)

LOSSMAPPER = {'categorical_crossentropy': categorical_crossentropy_masked,
              'binary_crossentropy': binary_crossentropy_masked,
              'binary_crossentropy_masked': binary_crossentropy_masked,
              'categorical_accuracy_masked': categorical_accuracy_masked,
              'categorical_crossentropy_masked': categorical_crossentropy_masked,
              'binary_accuracy_masked':binary_accuracy_masked,
              'binary_accuracy': binary_accuracy_masked,
              'categorical_accuracy': categorical_accuracy_masked,
              'top_k_categorical_accuracy':top_k_categorical_accuracy_masked,
              'top_k_categorical_accuracy_masked': top_k_categorical_accuracy_masked}
