import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

email_data_path = os.path.join(ROOT_DIR, 'data', 'emails.csv')

df = pd.read_csv(email_data_path)

data = df.iloc[:, :-1]
label = df.iloc[:, -1]
X = data.drop('Email No.', axis=1)
x_train, x_test, y_train, y_test = train_test_split(X, label, test_size=0.2, random_state=1)

np.random.seed(0)

class LogisticRegression:
    def __init__(self, learning_rate, iterations):
        self.learning_rate = learning_rate
        self.iterations = iterations

    def fit(self, X, y):
        self.features = np.array(X)
        self.label = np.array(y)
        self.num_samples, self.num_features = self.features.shape
        self.W = np.random.randn(self.num_features, 1)
        self.b = 0
        for i in range(self.iterations):
            self.update_weights()

    def sigmoid(self, Z):
        return 1.0 / (1.0 + np.exp(-Z))
    
    def update_weights(self):
        Z = np.dot(self.features, self.W) + self.b
        H = self.sigmoid(Z)
        self.label = np.reshape(self.label, H.shape)
        loss = H - self.label
        dw = np.dot(self.features.T, loss) / self.num_samples
        db = np.sum(loss) / self.num_samples

        self.W = self.W - self.learning_rate * dw
        self.b = self.b - self.learning_rate * db

    def predict(self, X):
        Z = np.dot(X, self.W) + self.b
        H = self.sigmoid(Z)
        preds = np.where(H >= 0.5, 1, 0)
        return preds


if __name__ == '__main__':
    model = LogisticRegression(learning_rate=0.1, iterations = 2000)
    model.fit(x_train, y_train)

    preds = model.predict(x_test)

    score = f1_score(y_test, preds)
    print(score)


