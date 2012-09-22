'''
Created on May 27, 2012

@author: sijin
'''

import numpy as np
from sklearn.preprocessing import Scaler
from sklearn.linear_model import LogisticRegression

with open('../../data/quora/input00.txt') as f:
    mn = f.readline().split(' ')
    N, M = int(mn[0]), int(mn[1])
    
    print 'M, N = {}, {}'.format(M, N)    
    
    X = np.zeros((N, M))
    Y = np.zeros(N, np.int)
    for row in range(N):
        training_data = f.readline().strip().split(' ')
        Y[row] = 1 if training_data[1] == '+1' else -1
        for col in range(2, 2+M):
            X[row, col-2] = training_data[col].split(':')[1]
    
    
    X = Scaler().fit_transform(X)
    clf_l1_LR = LogisticRegression(C=0.01, penalty='l1', tol=0.01)
    clf_l1_LR.fit(X, Y)
    print clf_l1_LR.decision_function(X)
      
if __name__ == '__main__':
    pass