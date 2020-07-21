import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import wilcoxon


def counts_from_series(series):
    counts = np.unique(series, return_counts=True)
    counts = dict(zip(counts[0], counts[1]))
    return counts


def complete_dict(dict_incomplete, dict_full):
    for key in dict_full:
        if key not in dict_incomplete:
            dict_incomplete[key] = 0


def plot_3hist_group(cat_list, count_dict_tuple, x_tick_coords, plot_title, y_lim=None):
    color_list = ['blue', 'black', 'yellow', 'green', 'red', 'orange']
    bar_width = .25

    x_gson = np.array(range(len(cat_list))) * bar_width
    x_js = x_gson + len(cat_list) * bar_width + bar_width
    x_orgjson = x_js + len(cat_list) * bar_width + bar_width

    ax = plt.bar(x_gson, [count_dict_tuple[0][key] for key in cat_list], width=bar_width,
                 color=color_list[:len(cat_list)], align='center')
    plt.bar(x_js, [count_dict_tuple[1][key] for key in cat_list], width=bar_width,
            color=color_list[:len(cat_list)], align='center')
    plt.bar(x_orgjson, [count_dict_tuple[2][key] for key in cat_list], width=bar_width,
            color=color_list[:len(cat_list)], align='center')
    plt.title(plot_title)
    plt.xticks(x_tick_coords * bar_width, ['GSON', 'json-simple', 'org.json'])
    plt.legend(ax, cat_list)
    if y_lim is not None:
        plt.ylim(y_lim)


# File import
gson_correct = pd.read_csv('../results/Gson_correct_results.csv')
gson_errored = pd.read_csv('../results/Gson_errored_results.csv')
gson_undefined = pd.read_csv('../results/Gson_undefined_results.csv')

js_correct = pd.read_csv('../results/json-simple_correct_results.csv')
js_errored = pd.read_csv('../results/json-simple_errored_results.csv')
js_undefined = pd.read_csv('../results/json-simple_undefined_results.csv')

orgjson_correct = pd.read_csv('../results/org.json_correct_results.csv')
orgjson_errored = pd.read_csv('../results/org.json_errored_results.csv')
orgjson_undefined = pd.read_csv('../results/org.json_undefined_results.csv')

# Counting categories
count_dict = {'gson_correct': counts_from_series(gson_correct.Result),
              'gson_errored': counts_from_series(gson_errored.Result),
              'gson_undefined': counts_from_series(gson_undefined.Result),
              'js_correct': counts_from_series(js_correct.Result),
              'js_errored': counts_from_series(js_errored.Result),
              'js_undefined': counts_from_series(js_undefined.Result),
              'orggson_correct': counts_from_series(orgjson_correct.Result),
              'orggson_errored': counts_from_series(orgjson_errored.Result),
              'orggson_undefined': counts_from_series(orgjson_undefined.Result)}

correct_cats = np.unique(gson_correct.Result.unique().tolist() + js_correct.Result.unique().tolist() +
                         orgjson_correct.Result.unique().tolist())
errored_cats = np.unique(gson_errored.Result.unique().tolist() + js_errored.Result.unique().tolist() +
                         orgjson_errored.Result.unique().tolist())
undefined_cats = np.unique(gson_undefined.Result.unique().tolist() + js_undefined.Result.unique().tolist() +
                           orgjson_undefined.Result.unique().tolist())

for key in count_dict:
    if key[-7:] == 'correct':
        complete_dict(count_dict[key], correct_cats)
    elif key[-7:] == 'errored':
        complete_dict(count_dict[key], errored_cats)
    elif key[-9:] == 'undefined':
        complete_dict(count_dict[key], undefined_cats)

# Draw a title and some text to the app:
'''
# Results of json replacement experiments with maven

The correct, errored and undefined files have the following labels:
'''

f'\nCorrect categories: {correct_cats}\n'
f'\nErrored categories: {errored_cats}\n'
f'\nUndefined categories: {undefined_cats}\n'

"""
The counts of labels can be seen in these plots:
"""

plot_3hist_group(correct_cats, (count_dict['gson_correct'], count_dict['js_correct'], count_dict['orggson_correct']),
                 np.array([2.5, 9.5, 16.5]), 'Correct files', y_lim=(0, 175))
st.pyplot()

plot_3hist_group(errored_cats, (count_dict['gson_errored'], count_dict['js_errored'], count_dict['orggson_errored']),
                 np.array([2.5, 9.5, 16.5]), 'Files with errors')
st.pyplot()

plot_3hist_group(undefined_cats, (count_dict['gson_undefined'], count_dict['js_undefined'],
                                  count_dict['orggson_undefined']),
                 np.array([1.5, 9.5, 16.5]), 'Undefined files', y_lim=(0, 40))
st.pyplot()

"""
### Frequency comparison
"""

d = [6, 8, 14, 16, 23, 24, 28, 29, 41, -48, 49, 56, 60, -67, 75]
w, p = wilcoxon(d)
w, p
