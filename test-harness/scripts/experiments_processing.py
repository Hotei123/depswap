import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import datetime


def counts_from_series(series):
    counts = np.unique(series, return_counts=True)
    counts = dict(zip(counts[0], counts[1]))
    return counts


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
gson_correct_res_counts = counts_from_series(gson_correct.Result)  # {'EQUIVALENT_OBJECT': 54, 'OK': 112}
gson_errored_res_counts = counts_from_series(gson_errored.Result)  # {'FILE_ERROR': 30, 'OK': 147, 'UNEXPECTED_OBJECT': 145}
gson_undefined_res_counts = counts_from_series(gson_undefined.Result)  # {'EQUIVALENT_OBJECT': 17, 'FILE_ERROR': 16, 'OK': 24}

js_correct_res_counts = counts_from_series(js_correct.Result)  # {'EQUIVALENT_OBJECT': 79, 'NULL_OBJECT': 1, 'OK': 83, 'PRINT_EXCEPTION': 3}
js_errored_res_counts = counts_from_series(js_errored.Result)  # {'FILE_ERROR': 30, 'NULL_OBJECT': 1, 'OK': 211, 'UNEXPECTED_OBJECT': 80}
js_undefined_res_counts = counts_from_series(js_undefined.Result)  # {'EQUIVALENT_OBJECT': 22, 'FILE_ERROR': 16, 'OK': 7, 'PARSE_EXCEPTION': 7, 'PRINT_EXCEPTION': 5}

orggson_correct_res_counts = counts_from_series(orgjson_correct.Result)  # {'EQUIVALENT_OBJECT': 62, 'NON_EQUIVALENT_OBJECT': 11, 'OK': 91, 'PARSE_EXCEPTION': 2}
orggson_errored_res_counts = counts_from_series(orgjson_errored.Result)  # {'CRASH': 3, 'FILE_ERROR': 30, 'OK': 119, 'UNEXPECTED_OBJECT': 170}
orggson_undefined_res_counts = counts_from_series(orgjson_undefined.Result)  # {'EQUIVALENT_OBJECT': 25, 'FILE_ERROR': 16, 'NON_EQUIVALENT_OBJECT': 6, 'OK': 7, 'PARSE_EXCEPTION': 3}

correct_cats = np.unique(gson_correct.Result.unique().tolist() + js_correct.Result.unique().tolist() +
                         orgjson_correct.Result.unique().tolist())
errored_cats = np.unique(gson_errored.Result.unique().tolist() + js_errored.Result.unique().tolist() +
                         orgjson_errored.Result.unique().tolist())
undefined_cats = np.unique(gson_undefined.Result.unique().tolist() + js_undefined.Result.unique().tolist() +
                           orgjson_undefined.Result.unique().tolist())

print(f'\nCorrect categories: {correct_cats}\n')
print(f'\nErrored categories: {errored_cats}\n')
print(f'\nUndefined categories: {undefined_cats}\n')
print(f'gson_correct_res_counts: {gson_correct_res_counts}\n')
print(f'gson_errored_res_counts: {gson_errored_res_counts}\n')
print(f'gson_undefined_res_counts: {gson_undefined_res_counts}\n')
print(f'js_correct_res_counts: {js_correct_res_counts}\n')
print(f'js_errored_res_counts: {js_errored_res_counts}\n')
print(f'js_undefined_res_counts: {js_undefined_res_counts}\n')
print(f'orggson_correct_res_counts: {orggson_correct_res_counts}\n')
print(f'orggson_errored_res_counts: {orggson_errored_res_counts}\n')
print(f'orggson_undefined_res_counts: {orggson_undefined_res_counts}\n')


x = np.array(range(5))
y = [4, 9, 2, 5, 7]
z = [1, -2, 3, 4, 6]
k = [8, 12, 13, 5, 6]

ax = plt.subplot(311)
width = .25
ax_1 = ax.bar(x - width, y, width=width, color='b', align='center')
ax_2 = ax.bar(x, z, width=width, color='g', align='center')
ax_3 = ax.bar(x + width, k, width=width, color='r', align='center')
plt.legend((ax_1[0], ax_2[0], ax_3[0]), ('A', 'B', 'C'))
plt.title('Correct files')
plt.xticks(x, ['x1', 'x2', 'x3'])
plt.tick_params(axis='x', rotation=45)

ax = plt.subplot(312)
ax_1 = ax.bar(x - width, y, width=width, color='b', align='center')
ax_2 = ax.bar(x, z, width=width, color='g', align='center')
ax_3 = ax.bar(x + width, k, width=width, color='r', align='center')
plt.legend((ax_1[0], ax_2[0], ax_3[0]), ('A', 'B', 'C'))
plt.title('Files with errors')

ax = plt.subplot(313)
ax_1 = ax.bar(x - width, y, width=width, color='b', align='center')
ax_2 = ax.bar(x, z, width=width, color='g', align='center')
ax_3 = ax.bar(x + width, k, width=width, color='r', align='center')
plt.legend((ax_1[0], ax_2[0], ax_3[0]), ('A', 'B', 'C'))
plt.title('Undefined files')
plt.tight_layout(pad=2)

plt.show()
