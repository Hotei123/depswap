import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import datetime

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
gson_correct_res_counts = np.unique(gson_correct.Result, return_counts=True)
gson_correct_res_counts = dict(zip(gson_correct_res_counts[0], gson_correct_res_counts[1]))
gson_errored_res_counts = np.unique(gson_errored.Result, return_counts=True)
gson_errored_res_counts = dict(zip(gson_errored_res_counts[0], gson_errored_res_counts[1]))
gson_undefined_res_counts = np.unique(gson_undefined.Result, return_counts=True)
gson_undefined_res_counts = dict(zip(gson_undefined_res_counts[0], gson_undefined_res_counts[1]))

js_correct_res_counts = np.unique(js_correct.Result, return_counts=True)
js_correct_res_counts = dict(zip(js_correct_res_counts[0], js_correct_res_counts[1]))
js_errored_res_counts = np.unique(js_errored.Result, return_counts=True)
js_errored_res_counts = dict(zip(js_errored_res_counts[0], js_errored_res_counts[1]))
js_undefined_res_counts = np.unique(js_undefined.Result, return_counts=True)
js_undefined_res_counts = dict(zip(js_undefined_res_counts[0], js_undefined_res_counts[1]))

orggson_correct_res_counts = np.unique(orgjson_correct.Result, return_counts=True)
orggson_correct_res_counts = dict(zip(orggson_correct_res_counts[0], orggson_correct_res_counts[1]))
orggson_errored_res_counts = np.unique(orgjson_errored.Result, return_counts=True)
orggson_errored_res_counts = dict(zip(orggson_errored_res_counts[0], orggson_errored_res_counts[1]))
orggson_undefined_res_counts = np.unique(orgjson_undefined.Result, return_counts=True)
orggson_undefined_res_counts = dict(zip(orggson_undefined_res_counts[0], orggson_undefined_res_counts[1]))

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

a = np.array([0, 3, 0, 1, 0, 1, 2, 1, 0, 0, 0, 0, 1, 3, 4])
unique, counts = np.unique(a, return_counts=True)
print(dict(zip(unique, counts)))

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
