#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as plt


def load_data(filename):
    with open(filename, 'rb') as f:
        data = []
        for row in f.readlines():
            data.append(map(float, row.split()))
    return np.array(data)


class LMS(object):
    def __init__(self, eta=0.001, iterations=10000):
        self.eta = eta
        self.iterations = iterations

    def fit(self, X_train, y_train):
        assert X_train.shape[0] == y_train.shape[0]

        n_data = X_train.shape[0]
        dim = X_train.shape[1]
        X_train = np.concatenate(
            [X_train, np.ones(n_data).reshape(n_data, 1)],
            axis=1)
        y_train = y_train.reshape((n_data, 1))
        w = np.ones(dim+1)
        for i in range(self.iterations):
            choice = np.random.randint(X_train.shape[0])
            predict = np.dot(X_train[choice], w)
            error = y_train[choice] - predict
            dw = self.eta * error * X_train[choice]
            w += dw
        self.w = w

    def predict(self, X_test):
        n_data = X_test.shape[0]
        X_test = np.concatenate(
            [X_test, np.ones(n_data).reshape(n_data, 1)],
            axis=1)
        y_pred = np.zeros(n_data).astype(int)
        for i, xt in enumerate(X_test):
            yp = np.dot(xt, self.w)
            y_pred[i] = np.argmin([(0-yp)**2, (1-yp)**2])
        return y_pred


def main():
    # get train dataset
    X1_train = load_data('../data/Train1.txt')
    y1 = np.empty(X1_train.shape[0]).astype(int)
    y1.fill(0)
    X2_train = load_data('../data/Train2.txt')
    y2 = np.empty(X2_train.shape[0]).astype(int)
    y2.fill(1)
    X_train = np.vstack((X1_train, X2_train))
    y_train = np.hstack((y1, y2))
    # plot train data
    plt.scatter(X1_train[:,0], X1_train[:,1], c='b', alpha=0.5, label='Train omega1')
    plt.scatter(X2_train[:,0], X2_train[:,1], c='r', alpha=0.5, label='Train omega2')
    # get test dataset
    X1_test = load_data('../data/Test1.txt')
    y1_test = np.empty(X1_test.shape[0]).astype(int)
    y1_test.fill(0)
    X2_test = load_data('../data/Test2.txt')
    y2_test = np.empty(X2_test.shape[0]).astype(int)
    y2_test.fill(1)
    X_test = np.vstack((X1_test, X2_test))
    y_test = np.hstack((y1_test, y2_test))
    # plot test data
    plt.scatter(X1_test[:,0], X1_test[:,1], c='g', alpha=0.5, label='Test omega1')
    plt.scatter(X2_test[:,0], X2_test[:,1], c='y', alpha=0.5, label='Test omega2')
    # lms computing
    lms = LMS()
    lms.fit(X_train, y_train)
    y_pred = lms.predict(X_test)
    # plot classification surface
    x = np.arange(-3, 5)
    y = 1 / lms.w[1] * (0.5 - lms.w[0]*x - lms.w[2])
    plt.plot(x, y, 'r', label='Classification surface')

    plt.legend(loc=2)
    plt.ylim(None, 9)
    # plt.show()
    plt.savefig('../output/kadai1.png')


if __name__ == '__main__':
    main()
