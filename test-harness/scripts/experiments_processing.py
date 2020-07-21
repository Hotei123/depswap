import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

# Correct categories
# 'EQUIVALENT_OBJECT', 'OK', 'NON_EQUIVALENT_OBJECT', 'NULL_OBJECT', 'PARSE_EXCEPTION', 'PRINT_EXCEPTION'
# Categories with errors
# 'FILE_ERROR', 'OK', 'UNEXPECTED_OBJECT', 'CRASH', 'NULL_OBJECT'
# Undefined categories
# 'EQUIVALENT_OBJECT', 'FILE_ERROR', 'OK', 'NON_EQUIVALENT_OBJECT', 'PARSE_EXCEPTION', 'PRINT_EXCEPTION'
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

print(f'\nCorrect categories: {correct_cats}\n')
print(f'\nErrored categories: {errored_cats}\n')
print(f'\nUndefined categories: {undefined_cats}\n')
print(f'gson_correct_res_counts: {list(count_dict["gson_correct"].keys())}\n')
print(f'gson_errored_res_counts: {list(count_dict["gson_errored"].keys())}\n')
print(f'gson_undefined_res_counts: {list(count_dict["gson_undefined"].keys())}\n')
print(f'js_correct_res_counts: {list(count_dict["js_correct"].keys())}\n')
print(f'js_errored_res_counts: {list(count_dict["js_errored"].keys())}\n')
print(f'js_undefined_res_counts: {list(count_dict["js_undefined"].keys())}\n')
print(f'orggson_correct_res_counts: {list(count_dict["orggson_correct"].keys())}\n')
print(f'orggson_errored_res_counts: {list(count_dict["orggson_errored"].keys())}\n')
print(f'orggson_undefined_res_counts: {list(count_dict["orggson_undefined"].keys())}\n')


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
