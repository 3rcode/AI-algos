import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

class NaiveBayes:
    def __init__(self):
        # Your Code here
        # Isolating spam and ham messages first
        
        # P(Spam) and P(Ham)
        # N_Spam
        self.n_words_per_spam_message = spam_messages['SMS'].apply(len)
        self.n_spam = n_words_per_spam_message.sum()
        # N_Ham
        self.n_words_per_ham_message = ham_messages['SMS'].apply(len)
        self.n_ham = n_words_per_ham_message.sum()
        
        # Laplace smoothing
        self.alpha = 1
        # pass

    def fit(self, X, Y):
        # N_Vocabulary
        self.n_vocabulary = len(X.shape[0])
        self.spam_messages = X[Y == 1]
        self.ham_messages = X[Y == 0]

        self.p_spam = len(self.spam_messages) / X.shape[0]
        self.p_ham = len(self.ham_messages) / X.shape[0]


        # Your Code here
        pass

    def predict(self, x):
        # Your Code here
        pass