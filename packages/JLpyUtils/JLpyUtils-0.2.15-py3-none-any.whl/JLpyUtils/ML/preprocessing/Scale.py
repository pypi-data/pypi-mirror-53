

class continuous_features():
    
    import sklearn, sklearn.preprocessing
    
    def __init__(self, Scaler = sklearn.preprocessing.MinMaxScaler()):
        
        """
        Instantiate a Scaler object to scale continuous_features specified in fit method

        Arguments:
        ---------
            Scaler: sklearn.preprocessing....: defaults: sklearn.preprocessing.MinMaxScaler()
                - Object specifing the scaler operation the data will be fit and transformed to.
        """
        
        self.Scaler = Scaler

    def fit(self, X, continuous_headers = 'auto'):
        """
        Fit the Scaler to the continous features contained in the dataframe passed
        
        Arguments:
        ----------
            X: the dataframe of interest (dask or pandas)
            continuous_headers: the header names for the continuous features of interest.
                - If 'auto', all columns will be assumed to be continuous features.
        
        Returns:
        --------
            None. The Scaler object will be ready to run the transform operation.
        """
        
        X = X.copy()
        
        if type(continuous_headers) == type(list):
            self.continuous_headers = continuous_headers
        else:
            self.continuous_headers = list(X.columns)
            
        self.Scaler.fit(X[self.continuous_headers])
        
    def transform(self, X):
        
        import warnings
        
        warnings.filterwarnings('ignore')
    
        
        type_X = str(type(X))
        if 'dask' in type_X:
            npartitions = X.npartitions
            X = X.compute()

        X[self.continuous_headers] = self.Scaler.transform(X[self.continuous_headers])
        
        if 'dask' in type_X:
            import dask, dask.dataframe
            X = dask.dataframe.from_pandas(X, npartitions=npartitions)
            
        warnings.filterwarnings('default')

        return X

def default_Scalers_dict():
    """
    fetch dictionary containing typical scalers used for transforming continuous data
    
    Returns:
    -------
        Scalers_dict: dictionary containing typical scalers used for transforming continuous data
    """
    import sklearn.preprocessing
    
    Scalers_dict = {'MinMaxScaler':sklearn.preprocessing.MinMaxScaler(),
                    'StandardScaler':sklearn.preprocessing.StandardScaler(),
                    'RobustScaler':sklearn.preprocessing.RobustScaler()}
    return Scalers_dict