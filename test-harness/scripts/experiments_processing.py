import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def counts_from_series(series):
    counts = np.unique(series, return_counts=True)
    counts = dict(zip(counts[0], counts[1]))
    return counts


def complete_dict(dict_incomplete, dict_full):
    for key in dict_full:
        if key not in dict_incomplete:
            dict_incomplete[key] = 0


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

The correct, errored and undefined files have the following categories:
'''

f'\nCorrect categories: {correct_cats}\n'
f'\nErrored categories: {errored_cats}\n'
f'\nUndefined categories: {undefined_cats}\n'

color_list = ['blue', 'black', 'yellow', 'green', 'red', 'orange']
bar_width = .25

x_gson = np.array(range(len(correct_cats))) * bar_width
x_js = x_gson + len(correct_cats) * bar_width + bar_width
x_orgjson = x_js + len(correct_cats) * bar_width + bar_width

ax = plt.bar(x_gson, [count_dict['gson_correct'][key] for key in correct_cats], width=bar_width,
             color=color_list[:len(correct_cats)], align='center')
plt.bar(x_js, [count_dict['js_correct'][key] for key in correct_cats], width=bar_width,
        color=color_list[:len(correct_cats)], align='center')
plt.bar(x_orgjson, [count_dict['orggson_correct'][key] for key in correct_cats], width=bar_width,
        color=color_list[:len(correct_cats)], align='center')
plt.title('Correct files')
plt.xticks([2.5 * bar_width, 9.5 * bar_width, 16.5 * bar_width], ['GSON', 'json-simple', 'org.json'])
plt.legend([ax[0], ax[1], ax[2], ax[3], ax[4], ax[5]], correct_cats)
plt.ylim((0, 175))

st.pyplot()

x_gson = np.array(range(len(errored_cats))) * bar_width
x_js = x_gson + len(errored_cats) * bar_width + bar_width
x_orgjson = x_js + len(errored_cats) * bar_width + bar_width
ax = plt.bar(x_gson, [count_dict['gson_errored'][key] for key in errored_cats], width=bar_width,
             color=color_list[:len(errored_cats)], align='center')
plt.bar(x_js, [count_dict['js_errored'][key] for key in errored_cats], width=bar_width,
        color=color_list[:len(errored_cats)], align='center')
plt.bar(x_orgjson, [count_dict['orggson_errored'][key] for key in errored_cats], width=bar_width,
        color=color_list[:len(errored_cats)], align='center')
plt.title('Files with errors')
plt.xticks([2.5 * bar_width, 8.5 * bar_width, 14.5 * bar_width], ['GSON', 'json-simple', 'org.json'])
plt.legend([ax[0], ax[1], ax[2], ax[3], ax[4]], errored_cats)
# plt.ylim((0, 175))

st.pyplot()

x_gson = np.array(range(len(undefined_cats))) * bar_width
x_js = x_gson + len(undefined_cats) * bar_width + bar_width
x_orgjson = x_js + len(undefined_cats) * bar_width + bar_width
ax = plt.bar(x_gson, [count_dict['gson_undefined'][key] for key in undefined_cats], width=bar_width,
             color=color_list[:len(undefined_cats)], align='center')
plt.bar(x_js, [count_dict['js_undefined'][key] for key in undefined_cats], width=bar_width,
        color=color_list[:len(undefined_cats)], align='center')
plt.bar(x_orgjson, [count_dict['orggson_undefined'][key] for key in undefined_cats], width=bar_width,
        color=color_list[:len(undefined_cats)], align='center')
plt.title('Undefined files')
plt.xticks([1.5 * bar_width, 9.5 * bar_width, 16.5 * bar_width], ['GSON', 'json-simple', 'org.json'])
plt.legend([ax[0], ax[1], ax[2], ax[3], ax[4], ax[5]], errored_cats)
plt.ylim((0, 40))

st.pyplot()
