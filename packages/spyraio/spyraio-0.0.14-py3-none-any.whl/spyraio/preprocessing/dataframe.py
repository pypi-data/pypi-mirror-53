# -*- coding: utf-8 -*-
"""Preprocessing functions.
"""
import os
import pandas as pd
from sklearn.model_selection import train_test_split


def load_dataset(path, files):
    """Load dataframe.
    
    # Arguments
        `path`: a string containing the file directory.
        `files`: a list containing one or more file names.
    # Returns
        Return a concatenated dataframe from files.
    """
    
    dfs = [pd.read_csv(os.path.join(path, file)) for file in files]
    df = pd.concat(dfs, sort=False)
    
    return df


def filter_dataframe(df, filters):
    """Filter data frame.
    
    # Arguments
        `df`: a pandas dataframe.
        `filters`: a list containing the filters to apply to data frame.
    # Returns
        Return a filtered data frame.
    """
    
    df = df.query(filters)
    
    return df
    

def set_threshold(df=None, filters=[], samples=1):
    """Apply threshold to dataframe and merge.
    
    # Arguments
        `df`: a pandas dataframe.
        `filters`: a list containing the filters of threshold to apply to data 
        frame.
        `samples`: a percentage to the smallest filtered data frame.
    # Returns
        Return a single data frame with threshold.
    """
    
    dfs = []
    sizes = []
    labels = range(len(filters))
#    df['label'] = None
    for label, filter_ in zip(labels, filters):
        df_ = df.query(filter_)
        df_['label'] = label
        sizes.append(df_.shape[0])
        dfs.append(df_)
    
    samples *= 100
    samples = int((min(sizes)*samples)/100)
    
    dfs = [df.sample(samples) for df in dfs]
    
    df = pd.concat(dfs, sort=False).sample(samples*len(filters))
    
    return df


def train_and_test_split(X, y, test_size=.2):
    """Slpit test and test dataset .
    
    # Arguments
        `X`: a list n-dimentional containing attributes values.
        `y`: Containg predict class values.
        `test_size (optional)`: size of dataset test (default: 20%).
        `samples`: a percentage to the smallest filtered data frame.
    # Returns
        Return the values of X_train, X_test, y_train and y_test.
    """
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        test_size=test_size)
    return X_train, X_test, y_train, y_test
    
    
if __name__ == "__main__":
    df = load_dataset('./data/private', ['august.csv'])
    print(df)
    