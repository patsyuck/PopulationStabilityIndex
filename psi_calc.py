# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 23:28:18 2021
Script for PSI calculation of two population (number arrays).
@author: o.patsiuk
"""

import numpy as np
from math import floor

def get_bins_points(array, n=10, method='quantiles'):
    res = []
    array = sorted(array)
    if method == 'quantiles': # equal numbers of elements
        length = int(floor(len(array) / n))
        rest = len(array) - n * length
        for i in range(1, n):
            if rest >= i:
                res.append((array[i * length + i - 1] + array[i * length + i]) / 2)
            else:
                res.append((array[i * length + rest - 1] + array[i * length + rest]) / 2)
    elif method == 'bins': # equal distances between points
        m = np.min(array)
        delta = np.max(array) - m
        for i in range(1, n):
            res.append(i * delta / n + m)
    return res

def get_parts(array, bins):
    res = []
    l = len(array)
    for i in range(len(bins) + 1):
        if i == 0:
            res.append(sum([x < bins[0] for x in array]) / l)
        elif i == len(bins):
            res.append(sum([x >= bins[len(bins) - 1] for x in array]) / l)
        else:
            res.append(sum([(x >= bins[i-1]) and (x < bins[i]) for x in array]) / l)
    return res

def get_psi(old, new):
    psi = 0
    e = 0.00000001
    for i in range(len(old)):
        if old[i] == 0:
            psi += (new[i] - old[i]) * np.log((new[i] + e) / (old[i] + e))
        else:
            psi += (new[i] - old[i]) * np.log(new[i] / old[i])
    return psi

def psi(array_old, array_new, n=10, method='quantiles'):
    bins = get_bins_points(array_old, n, method)
    parts_old = get_parts(array_old, bins)
    parts_new = get_parts(array_new, bins)
    return get_psi(parts_old, parts_new)