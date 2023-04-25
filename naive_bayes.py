import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

email_data_path = os.path.join(ROOT_DIR, 'data', 'emails.csv')

df = pd.read_csv(email_data_path)

data = df.iloc[:, :-1]
label = df.iloc[:, -1]
X = data.drop('Email No.', axis=1)
x_train, x_test, y_train, y_test = train_test_split(X, label, test_size=0.2, random_state=1)

class NaiveBayes:
    def __init__(self):
        pass

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self._classes = np.unique(y)
        n_classes = len(self._classes)

        self._mean = np.zeros((n_classes, n_features), dtype=np.float64)
        self._var = np.zeros((n_classes, n_features), dtype=np.float64)
        self._prior = np.zeros(n_classes, dtype=np.float64)

        for idx, c in enumerate(self._classes):
            X_c = X[y==c]
            self._mean[idx, :] = X_c.mean(axis=0)
            self._var[idx, :] = X_c.var(axis=0)
            self._prior[idx] = X_c.shape[0] / float(n_samples) 
    
    def predict(self, X):
        preds = [self._predict(X.iloc[i]) for i in range(X.shape[0])]
        return np.array(preds)
    
    def _predict(self, x):
        posteriors = []
        for idx, c in enumerate(self._classes):
            
            prior = np.log(self._prior[idx])
            posterior = self._posterior(idx, x)
            posterior += prior
            posteriors.append(posterior)
        
        return self._classes[np.argmax(posteriors)]
    
    def _posterior(self, class_idx, x):
        mean = self._mean[class_idx]
        var = self._var[class_idx]
        numerator = np.exp(-(x - mean) ** 2 / (2 * var))
        denominator = np.sqrt(2 * np.pi * var)
        posterior = np.sum(np.log(numerator / denominator))
        return posterior
        

if __name__ == '__main__':
    model = NaiveBayes()
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    score = f1_score(y_test, preds)
    print(score)

    