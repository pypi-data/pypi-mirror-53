#!/usr/bin/env python3
#===============================================================================
# finrich.py
#===============================================================================

# Imports ======================================================================

import json

from argparse import ArgumentParser
from functools import partial
from math import log
from multiprocessing import Pool
from pybedtools import BedTool
from random import sample
from statistics import mean




# Functions ====================================================================j

def ppa_in_interval(interval, finemap):
    """Compute the total posterior probability mass contained in a
    genomic interval

    Parameters
    ----------
    interval
        a BedTool representing the genomic interval
    finemap
        a BedTool representing the fine mapping data
    
    Returns
    -------
    float
        the total posterior probability mass contained in the interval
    """

    return sum(
        float(i.fields[-1]) for i in finemap.intersect(BedTool([interval]))
    )


def draw_sample(dummy, population, k):
    """Draw a sample total PPA value from the background distribution

    Parameters
    ----------
    dummy
        a dummy variable, used for multiprocessing
    population
        iterable containing the population of values
    k
        size of the sample to draw
    
    Returns
    -------
    float
        the total PPA of the sample drawn
    """

    return sum(sample(population, k))


def permutation_test(
    finemap,
    regions,
    background,
    permutations: int = 100_000,
    processes: int = 1
):
    """Perform a permutation test for enrichment of fine-mapping signals in
    a set of genomic regions

    Parameters
    ----------
    finemap
        a BedTool representing the fine mapping data
    regions
        a BedTool representing the genomic regions
    background
        a bedTool representing the background
    permutations : int
        the number of permutations to perform
    processes : int
        the number of processes to use
    
    Returns
    -------
    float
        the p-value of the test
    """

    with Pool(processes=processes) as pool:
        ppa_vals = tuple(
            pool.map(
                partial(ppa_in_interval, finemap=finemap),
                background.intersect(finemap, u=True)
            )
        )
    population =  (
        tuple(sorted(ppa_vals, reverse=True))
        + (0,) * (len(background) - len(ppa_vals))
    )
    max_val = sum(population[:len(regions)])
    print(max_val)
    observed_val = sum(float(i.fields[-1]) for i in finemap.intersect(regions))
    print(observed_val)

    def log_odds(val):
        return (
            log(observed_val)
            + log(max_val - val)
            - log(max_val - observed_val)
            - log(val)
        )

    with Pool(processes=processes) as pool:
        empirical_dist = sorted(
            pool.map(
                partial(draw_sample, population=population, k=len(regions)),
                range(permutations)
            )
        )
    pval = sum(val >= observed_val for val in empirical_dist) / permutations
    print(pval)
    empirical_log_odds = tuple(log_odds(val) for val in empirical_dist)
    mean_log_odds = mean(empirical_log_odds)
    conf_lower = empirical_log_odds[int(permutations * 0.95)]
    conf_upper = empirical_log_odds[int(permutations * 0.05)]
    return {
        'pval': pval,
        'logOR': mean_log_odds,
        'conf_lower': conf_lower,
        'conf_upper': conf_upper
    }


def parse_arguments():
    parser = ArgumentParser(
        description='enrichment of fine mapping probability'
    )
    parser.add_argument(
        'finemap',
        metavar='<path/to/finemap.bed>',
        type=BedTool,
        help='bed file with fine-mapping data'
    )
    parser.add_argument(
        'regions',
        metavar='<path/to/regions.bed>',
        type=BedTool,
        help='bed file with test regions data'
    )
    parser.add_argument(
        'background',
        metavar='<path/to/background.bed>',
        type=BedTool,
        help='bed file with background regions data'
    )
    parser.add_argument(
        '--permutations',
        metavar='<int>',
        type=int,
        default=10_000,
        help='number of permutations'
    )
    parser.add_argument(
        '--processes',
        metavar='<int>',
        type=int,
        default=1,
        help='number of processes to use'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    result = permutation_test(
        args.finemap,
        args.regions,
        args.background,
        permutations=args.permutations,
        processes=args.processes
    )
    print(json.dumps(result))
