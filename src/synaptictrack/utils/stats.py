import numpy as np

def calc_mean_weighted(x, weights=None):
    x = np.asarray(x)
    if weights is None:
        return np.mean(x)
    weights = np.asarray(weights)
    return np.sum(weights * x) / np.sum(weights)

def calc_variance(x, weights=None):
    x = np.asarray(x)
    mean = calc_mean_weighted(x, weights)
    if weights is None:
        return np.mean((x - mean) ** 2)
    return np.sum(weights * (x - mean) ** 2) / np.sum(weights)

def calc_covariance(x, y, weights=None):
    x = np.asarray(x)
    y = np.asarray(y)
    mean_x = calc_mean_weighted(x, weights)
    mean_y = calc_mean_weighted(y, weights)
    if weights is None:
        return np.mean((x - mean_x) * (y - mean_y))
    return np.sum(weights * (x - mean_x) * (y - mean_y)) / np.sum(weights)

def calc_correlation(x, y, weights=None):
    cov = calc_covariance(x, y, weights)
    std_x = np.sqrt(calc_variance(x, weights))
    std_y = np.sqrt(calc_variance(y, weights))
    return cov / (std_x * std_y)

def calc_rms(x, weights=None):
    x = np.asarray(x)
    if weights is None:
        return np.sqrt(np.mean(x ** 2))
    weights = np.asarray(weights)
    return np.sqrt(np.sum(weights * x ** 2) / np.sum(weights))

def calc_moment(x, order=3, weights=None):
    """
    Compute central moment of given order.
    """
    x = np.asarray(x)
    mean = calc_mean_weighted(x, weights)
    if weights is None:
        return np.mean((x - mean) ** order)
    return np.sum(weights * (x - mean) ** order) / np.sum(weights)

