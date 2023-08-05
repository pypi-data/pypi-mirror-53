"""
Functions for computing benchmark metrics
"""


import numpy as np
import pandas as pd
import sklearn.metrics
import sklearn.neighbors
from . import blast
from . import utils

_identity = lambda x, y: 1 if x == y else 0


#===============================================================================
#
#  Cluster based metrics
#
#===============================================================================
def confusion_matrix(x, y):
    """
    Reimplemented this because sklearn.metrics.confusion_matrix
    does not provide row names and column names.
    """
    x, x_c = utils.encode_integer(x)
    y, y_c = utils.encode_integer(y)
    unique_x, unique_y = np.unique(x), np.unique(y)
    cm = np.empty((len(unique_x), len(unique_y)), dtype=np.int)
    for i in unique_x:
        for j in unique_y:
            cm[i, j] = np.sum((x == i) & (y == j))
    return pd.DataFrame(data=cm, index=x_c, columns=y_c)


def class_specific_accuracy(true, pred, expectation):
    df = pd.DataFrame(index=np.unique(true), columns=["number", "accuracy"])
    expectation = expectation.astype(np.bool)
    for c in df.index:
        true_mask = true == c
        pred_mask = np.in1d(pred, expectation.columns[expectation.loc[c]])
        df.loc[c, "number"] = true_mask.sum()
        df.loc[c, "accuracy"] = np.logical_and(pred_mask, true_mask).sum() / df.loc[c, "number"]
    return df


def mean_balanced_accuracy(true, pred, expectation, population_weighed=False):
    df = class_specific_accuracy(true, pred, expectation)
    if population_weighed:
        return (df["accuracy"] * df["number"]).sum() / df["number"].sum()
    return df["accuracy"].mean()


#===============================================================================
#
#  Distance based metrics
#
#===============================================================================
def nearest_neighbor_accuracy(
        x, y, metric="minkowski", similarity=_identity, n_jobs=1):
    nearestNeighbors = sklearn.neighbors.NearestNeighbors(
        n_neighbors=2, metric=metric, n_jobs=n_jobs)
    nearestNeighbors.fit(x)
    nni = nearestNeighbors.kneighbors(x, return_distance=False)
    return np.vectorize(similarity)(y, y[nni[:, 1].ravel()]).mean()


def mean_average_precision_from_latent(
    x, y, p=None, k=0.01, metric="minkowski", posterior_metric="npd_v1",
    similarity=_identity, n_jobs=1
):
    if k < 1:
        k = y.shape[0] * k
    k = np.round(k).astype(np.int)
    nearestNeighbors = sklearn.neighbors.NearestNeighbors(
        n_neighbors=min(y.shape[0], k + 1), metric=metric, n_jobs=n_jobs)
    nearestNeighbors.fit(x)
    nni = nearestNeighbors.kneighbors(x, return_distance=False)
    if p is not None:
        posterior_metric = getattr(blast, posterior_metric)
        pnnd = np.empty_like(nni, np.float32)
        for i in range(pnnd.shape[0]):
            for j in range(pnnd.shape[1]):
                pnnd[i, j] = posterior_metric(
                    x[i], x[nni[i, j]],
                    p[i], p[nni[i, j]]
                )
            nni[i] = nni[i][np.argsort(pnnd[i])]
    return mean_average_precision(y, y[nni[:, 1:]], similarity=similarity)


def average_silhouette_score(x, y):
    return sklearn.metrics.silhouette_score(x, y)


def seurat_alignment_score(
        x, y, k=0.01, n=1, metric="minkowski", random_seed=None, n_jobs=1):
    random_state = np.random.RandomState(random_seed)
    idx_list = [np.where(y == _y)[0] for _y in np.unique(y)]
    subsample_size = min(idx.size for idx in idx_list)
    subsample_scores = []
    for _ in range(n):
        subsample_idx_list = [
            random_state.choice(idx, subsample_size, replace=False)
            for idx in idx_list
        ]
        subsample_y = y[np.concatenate(subsample_idx_list)]
        subsample_x = x[np.concatenate(subsample_idx_list)]
        _k = subsample_y.shape[0] * k if k < 1 else k
        _k = np.round(_k).astype(np.int)
        nearestNeighbors = sklearn.neighbors.NearestNeighbors(
            n_neighbors=min(subsample_y.shape[0], _k + 1),
            metric=metric, n_jobs=n_jobs
        )
        nearestNeighbors.fit(subsample_x)
        nni = nearestNeighbors.kneighbors(subsample_x, return_distance=False)
        same_y_hits = (
            subsample_y[nni[:, 1:]] == np.expand_dims(subsample_y, axis=1)
        ).sum(axis=1).mean()
        subsample_scores.append(
            (_k - same_y_hits) * len(idx_list) /
            (_k * (len(idx_list) - 1))
        )
    return np.mean(subsample_scores)


def batch_mixing_entropy(
    x, y, boots=100, sample_size=100, k=100,
    metric="minkowski", random_seed=None, n_jobs=1
):
    random_state = np.random.RandomState(random_seed)
    batches = np.unique(y)
    entropy = 0
    for _ in range(boots):
        bootsamples = random_state.choice(
            np.arange(x.shape[0]), sample_size, replace=False)
        subsample_x = x[bootsamples]
        neighbor = sklearn.neighbors.NearestNeighbors(
            n_neighbors=k, metric=metric, n_jobs=n_jobs
        )
        neighbor.fit(x)
        nn = neighbor.kneighbors(subsample_x, return_distance=False)
        for i in range(sample_size):
            for batch in batches:
                b = len(np.where(y[nn[i, :]] == batch)[0]) / k
                if b == 0:
                    entropy = entropy
                else:
                    entropy = entropy + b * np.log(b)
    entropy = -entropy / (boots * sample_size)
    return entropy


#===============================================================================
#
#  Ranking based metrics
#
#===============================================================================
def _average_precision(r):
    positives = np.where(r == 1)[0] + 1
    if len(positives):
        return np.vectorize(
            lambda k, _r=r: _r[0:k].sum() / k
        )(positives).mean()
    return 0.


def mean_average_precision(ref, hits, similarity=_identity):
    r = np.apply_along_axis(np.vectorize(similarity), 0, hits, ref)
    return np.apply_along_axis(_average_precision, 1, r).mean()
