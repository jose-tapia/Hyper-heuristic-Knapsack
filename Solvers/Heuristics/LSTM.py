import numpy as np
import pandas as pd
import tensorflow
from keras.layers import LSTM, Bidirectional, Dense
from keras.models import Sequential
from Solvers.Heuristics.metaheuristic import solveMetaheuristic
from Utils.IO import loadInstance, obtainFilenames, tapia_path
from Utils.knapsack import Knapsack, generateItemList

def series_to_supervised(data, n_in = 1, n_out = 1, dropnan = True):
    # Get the number of variables in the dataset
    if type(data) == list:
        n_vars = 1
    else:
        n_vars = data.shape[1]
    # n_vars = 1 if type(data) is list else data.shape[1]
    # Convert the data to a dataframe if it is not.
    df = pd.DataFrame(data)
    # Initialize temporary lists that will append the shifted columns
    columns, var_name = list(), list()
    # Append columns with the number of input sequence and shift the data everytime a column is created
    for i in range(n_in, 0, -1):
        columns.append(df.shift(i))
        var_name += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # Append columns for present and future forecast with the inverse of the shift function
    for i in range(n_out):
        columns.append(df.shift(-i))
        if i == 0:
            var_name += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            var_name += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # Concatenate all the columns
    agg = pd.concat(columns, axis=1)
    agg.columns = var_name
    # drop rows with missing values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

def create_dummies(data, column_name, prefix=None):
    return pd.concat([data, pd.get_dummies(data[column_name], prefix = prefix)], axis = 1).drop(column_name, axis = 1)

def train_lstm(data, n_id, n_output, lag, hiddenLayer_neurons, batch_size, epochs):
    # Create a copy of the dataset
    df = data.copy()
    # Create supervised problem
    df_sup = series_to_supervised(df, lag, 1)
    # Drop the features we do not want do predict
    df_sup.drop(df_sup.columns[(-7-n_output-n_id):-n_output], axis = 1, inplace = True)
    # Get the number of variables without the output values
    n_var = len(df.columns.values)-n_output
    # Split into input and outputs
    X_train, y_train = df_sup.iloc[:, :lag*n_var].values, df_sup.iloc[:, -n_output:].values
    # Reshape input to be [samples, timesteps, features]
    X_train = X_train.reshape((X_train.shape[0], lag, n_var))
    # Design the neural network
    model = Sequential()
    model.add(Bidirectional(LSTM(hiddenLayer_neurons, activation = 'tanh', input_shape = (X_train.shape[1], X_train.shape[2]))))
    model.add(Dense(n_output, activation = 'softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    # Fit network
    model.fit(X_train, y_train, epochs = epochs, batch_size = batch_size, shuffle = False)
    return model

def buildModel(modelPath, trainPath):
    df = pd.read_csv(trainPath, dtype = {'ID': str})
    n_id = len(df.ID.unique())
    n_output = len(df.NextHeuristic.unique())
    df = create_dummies(df, 'ID', prefix = 'ID')
    df = create_dummies(df, 'NextHeuristic')
    tensorflow.keras.backend.clear_session()
    model = train_lstm(df, n_id, n_output, lag = 2, hiddenLayer_neurons = 50, batch_size = 64, epochs = 100)
    model.save(modelPath)

def generateTrainDataset(trainFilename = 'traindata.csv', overwrite = True, instances = 'Pisinger'):
    if type(instances) == str: 
        instances = obtainFilenames(tapia_path, instances)
    for filePath in instances:    
        n, W, weights, profits = loadInstance(filePath)
        kp = Knapsack(W)
        items = generateItemList(weights, profits)
        np.random.seed(0)
        solveMetaheuristic('SimulatedAnnealing', kp, items, saveMetaheuristic = True, fileName = trainFilename, overwrite = overwrite)
        overwrite = False   
    