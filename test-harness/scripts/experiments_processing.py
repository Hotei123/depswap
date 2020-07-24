"""This file is better run with the command _streamlit run experiments_processing.py_, in order to visualize the output
in the browser."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import wilcoxon
from numpy import round as npr


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


def wilcoxon_p_val_from_2_dicts(dict_pair, cat_list):
    """Returns the p-value of the Wilcoxon test, for the paired dictionaries of dict_pair (they have the same keys)"""
    diff_list = [dict_pair[0][k] - dict_pair[1][k] for k in cat_list]
    return wilcoxon(diff_list)[1]


def wilcox_p_val_3_dicts(dict_3_list, cat_list):
    """Returns the wilcoxon p-value of the test of these pairs of elements of dict_3_list: (first, second),
    (first, third), and (second, third)"""
    return wilcoxon_p_val_from_2_dicts((dict_3_list[0], dict_3_list[1]), cat_list), \
           wilcoxon_p_val_from_2_dicts((dict_3_list[0], dict_3_list[2]), cat_list), \
           wilcoxon_p_val_from_2_dicts((dict_3_list[1], dict_3_list[2]), cat_list)


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
              'orgjson_correct': counts_from_series(orgjson_correct.Result),
              'orgjson_errored': counts_from_series(orgjson_errored.Result),
              'orgjson_undefined': counts_from_series(orgjson_undefined.Result)}

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

"""
# Results of json library replacement experiments with maven

### Introduction
We have a bench of 166 correct, 322 errored and 57 json files. In the following sections will be analyzed the labels
diversity of maven libraries gson, org.json and json-simple with respect to such bench, the diversity of heap use, and
other metrics too. 

### Category count plot
The counts of labels for each json library, for files _correct_, _errored_ and _undefined_ can be seen in these plots:
"""

plot_3hist_group(correct_cats, (count_dict['gson_correct'], count_dict['js_correct'], count_dict['orgjson_correct']),
                 np.array([2.5, 9.5, 16.5]), 'Correct files', y_lim=(0, 175))
st.pyplot()

plot_3hist_group(errored_cats, (count_dict['gson_errored'], count_dict['js_errored'], count_dict['orgjson_errored']),
                 np.array([2.5, 9.5, 16.5]), 'Files with errors')
st.pyplot()

plot_3hist_group(undefined_cats, (count_dict['gson_undefined'], count_dict['js_undefined'],
                                  count_dict['orgjson_undefined']),
                 np.array([1.5, 9.5, 16.5]), 'Undefined files', y_lim=(0, 40))
st.pyplot()

"""### Statistical tests for comparing category counts between libraries
After looking at the data of each of the 
previous 3 plots, we had the null hypothesis that the counts of the categories for each library come from the same 
population, and that therefore there is no diversity between the libraries in this respect. The obtained high p-values
of the [Wilcoxon signed-rank test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html)
agree with our hypothesis, and therefore, so far we have no evidence to reject it. This result makes sense, since
the structure of files is expected to be recognized by the libraries in more or less the same way."""

# Correct files
p_corr_gs_js, p_corr_gs_orgj, p_corr_js_orgj = wilcox_p_val_3_dicts((count_dict['gson_correct'],
                                                                     count_dict['js_correct'],
                                                                     count_dict['orgjson_correct']),
                                                                    correct_cats)
# Files with errors
p_err_gs_js, p_err_gs_orgj, p_err_js_orgj = wilcox_p_val_3_dicts((count_dict['gson_errored'],
                                                                  count_dict['js_errored'],
                                                                  count_dict['orgjson_errored']),
                                                                 errored_cats)
# Undefined files
p_udf_gs_js, p_udf_gs_orgj, p_udf_js_orgj = wilcox_p_val_3_dicts((count_dict['gson_undefined'],
                                                                  count_dict['js_undefined'],
                                                                  count_dict['orgjson_undefined']),
                                                                 undefined_cats)
corr_mat = pd.DataFrame([['gson-js', npr(p_corr_gs_js, 3), npr(p_err_gs_js, 3), npr(p_udf_gs_js, 3)],
                         ['gson-orgj', npr(p_corr_gs_orgj, 3), npr(p_err_gs_orgj, 3), npr(p_udf_gs_orgj, 3)],
                         ['js-orgj', npr(p_corr_js_orgj, 3), npr(p_err_js_orgj, 3), npr(p_udf_js_orgj, 3)]],
                        columns=['Paired tests', 'Correct p-vals ', 'Errored p-vals', 'Undefined p-vals'])
corr_mat
