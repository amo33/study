import numpy as np 


def permutation_train_test_split(X, y, test_size=0.3, shuffle=True, random_state=1004):
    test_num = int(X.shape[0] * test_size)
    train_num = X.shape[0] - test_num

    if shuffle:
        np.random.seed(random_state)
        shuffled = np.random.permutation(X.shape[0])
        X = X.iloc[shuffled,:]
        y = y.iloc[shuffled]
        X_train = X.iloc[:train_num]
        X_test = X.iloc[train_num:]
        y_train = y.iloc[:train_num]
        y_test = y.iloc[train_num:]

    else:
        X_train = X.iloc[:train_num]
        X_test = X.iloc[train_num:]
        y_train = y.iloc[:train_num]
        y_test = y.iloc[train_num:]

    return X_train, X_test, y_train, y_test


def Standardscaler(scaling_value,col,data):
    mean_val = np.mean(data)
    std_val = np.std(data)
    scaling_value[col]=[mean_val,std_val]

    return data.apply(lambda x: (x - mean_val)/(std_val))

def outlier_iqr(data):
    q1, q3 = np.percentile(data, [25,75])
    
    iqr = q3 - q1 
    lower_bound = q1 - (iqr*1.5)
    upper_bound = q3 + (iqr*1.5)
    
    return np.where((data > upper_bound)|(data < lower_bound))
