"""Tests for the words plots from lisc."""

from collections import Counter

import numpy as np
from nltk import FreqDist

from lisc.tests.utils import plot_test, optional_test

from lisc.plts.words import *

###################################################################################################
###################################################################################################

@optional_test('wordcloud')
@plot_test
def test_plot_wordcloud():

    freq_dist = FreqDist(['lots', 'of', 'words', 'words'])
    plot_wordcloud(freq_dist, 5)

@optional_test('matplotlib')
@plot_test
def test_plot_years():

    years = Counter([2000, 2000, 2015, 2016])
    plot_years(years, year_range=[1999, 2017])
