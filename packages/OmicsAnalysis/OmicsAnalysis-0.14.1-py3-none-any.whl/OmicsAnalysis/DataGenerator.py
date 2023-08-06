import pandas as pd
import numpy as np
import keras
import random
from tensorflow import set_random_seed
import copy
from OmicsAnalysis.InteractionNetwork import UndirectedInteractionNetwork, checkTrainingSetsPairs
from keras.layers import Embedding, Input, Dense, Flatten, Dropout, Lambda
from keras.models import Model
from keras.losses import binary_crossentropy


class DataGenerator(keras.utils.Sequence):
    "Data generator for keras models"
    def __init__(self, X_pos, neg_pos_ratio, num_pos, testing=None, prohib=None, keep_seed=False,
                 random_state=42, undersample=None):
        'Initialize variables'
        self.X_pos = copy.deepcopy(X_pos)
        self.neg_pos_ratio = np.int(neg_pos_ratio)  # has to be integer!!!
        self.testing = testing
        self.num_pos = num_pos  # The amount of positives shown each epoch
        self.random_state = random_state
        self.keep_seed = keep_seed
        self.undersample = undersample
        self.indexes = np.arange(X_pos.shape[0])
        self.max_int = np.max(self.X_pos)

        if self.keep_seed:
            np.random.seed(self.random_state)
            random.seed(self.random_state)
            set_random_seed(self.random_state)

        self.on_epoch_end()  # related to shuffle


        self.ncols = self.X_pos.shape[1]

        if prohib is None:
            prohib = np.array([[0, 0]], dtype=np.uint16)

        self.prohib = set([tuple(sorted(tuple(pair))) for pair in prohib])
        self.counter = 0

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(self.X_pos.shape[0] / self.num_pos))

    def on_epoch_end(self):
        """
        makes sure every epoch start with the original adjacency matrix
        :return: original adjacency matrix
        """
        np.random.shuffle(self.indexes)

        self.batch_counter = 0
        print('Batch counter has been reset.')
        if self.keep_seed:
            np.random.seed(self.random_state)
            random.seed(self.random_state)
            set_random_seed(self.random_state)

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        ids = self.indexes[index*self.num_pos:(index+1)*self.num_pos]

        # Generate data
        X, y = self.__simple_generator(ids)

        return X, y

    def __simple_generator(self, ids):

        self.batch_counter += 1
        genes = np.unique(self.X_pos[ids])

        negs = np.transpose(np.vstack((np.repeat(genes, self.neg_pos_ratio),
                                       np.random.randint(0, self.max_int + 1,
                                                         len(genes) * self.neg_pos_ratio))))
        negs = np.sort(negs, axis=1)
        negs = set([tuple(p) for p in negs])
        negs = negs.difference(self.prohib)

        Y = np.hstack((np.ones(len(ids)), np.zeros(len(negs))))
        X = np.vstack((self.X_pos[ids], np.array(list(negs))))

        return X, Y


if __name__ == "__main__":
    DATA_PATH = '/home/mlarmuse/Documents/NetworkData/'

    workers = 1
    train_ratio = 0.7
    neg_pos_ratio = 5
    num_pos = 8
    batch_size = (num_pos * neg_pos_ratio + 1)  # to have similar batchsizes for all training
    n_epochs = 100
    n_subsample = 100
    embed_dim = 10

    react_net_names = pd.read_csv(DATA_PATH + "FIsInGene_071718_with_annotations.txt", sep='\t', header=0,
                            usecols=('Gene1', 'Gene2'))
    all_genes_not_unique = list(react_net_names['Gene1'].values)+list(react_net_names['Gene2'].values)

    react_net = UndirectedInteractionNetwork(react_net_names, colnames=('Gene1', 'Gene2'))
    subnet = react_net.subsample(n=n_subsample)

    net= react_net
    X_train_ms, X_test_ms, Y_train_ms, Y_test_ms, summary_ms_tree = net.getTrainTestData(train_ratio=train_ratio,
                                                                                               neg_pos_ratio=neg_pos_ratio,
                                                                                               method='ms_tree',
                                                                                               random_state=51)

    embedding_layer = Embedding(input_dim=net.N_nodes, output_dim=10, input_length=2)  # initialize separately

    sequence_input = Input(shape=(2,), dtype='int32') # = model input with dimension of (batchsize, MAX_SEQUENCE_LENGTH)
    embedded_sequences = embedding_layer(sequence_input)
    #x = Flatten()(embedded_sequences)

    x = Lambda(lambda X: np.abs(X[:, 0] - X[:, 1]), output_shape=[embed_dim])(embedded_sequences)
    #x = Lambda(lambda X: X[:, 0] * X[:, 1], output_shape=[embed_dim])(embedded_sequences)

    x = Dense(32, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(32, activation='relu')(x)
    x = Dropout(0.2)(x)
    preds = Dense(1, activation='sigmoid')(x)

    model = Model(sequence_input, preds) # define relationship between INPUT and OUTPUT
    model.compile(optimizer="adam", loss=binary_crossentropy, metrics=["binary_accuracy"])
    earlyStopping = keras.callbacks.EarlyStopping(monitor='val_loss', patience=1, verbose=0, mode='auto')

    model_ML = keras.models.clone_model(model)
    model_ML.set_weights(model.get_weights())
    model_ML.compile(optimizer="adam", loss=binary_crossentropy, metrics=["binary_accuracy"])

    training_generator_maarten = DataGenerator(X_pos=X_train_ms[Y_train_ms == 1].astype(np.uint16),
                                               neg_pos_ratio=5,
                                               num_pos=num_pos,
                                               prohib=np.vstack((X_train_ms[Y_train_ms == 1].astype(np.uint16),
                                                                 X_test_ms.astype(np.uint16))),
                                               keep_seed=True)

    ML_history = model_ML.fit_generator(generator=training_generator_maarten,
                                        steps_per_epoch=len(training_generator_maarten),
                                       use_multiprocessing=False,
                                       workers=1,  # Need to be put to 1 for fair comparison?
                                       verbose=2,
                                       callbacks=[earlyStopping],
                                       validation_data=(X_test_ms, Y_test_ms),
                                       epochs=n_epochs)
