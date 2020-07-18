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
gson_errored_res_counts = np.unique(gson_errored.Result, return_counts=True)
gson_undefined_res_counts = np.unique(gson_undefined.Result, return_counts=True)

js_correct_res_counts = np.unique(js_correct.Result, return_counts=True)
js_errored_res_counts = np.unique(js_errored.Result, return_counts=True)
js_undefined_res_counts = np.unique(js_undefined.Result, return_counts=True)

orggson_correct_res_counts = np.unique(orgjson_correct.Result, return_counts=True)
orggson_errored_res_counts = np.unique(orgjson_errored.Result, return_counts=True)
orggson_undefined_res_counts = np.unique(orgjson_undefined.Result, return_counts=True)

correct_cats = np.unique(gson_correct.Result.unique().tolist() + js_correct.Result.unique().tolist() +
                         orgjson_correct.Result.unique().tolist())

print(f'\nCorrect categories: {correct_cats}\n')
print(f'gson_correct_res_counts: {gson_correct_res_counts}\n')
print(f'gson_errored_res_counts: {gson_errored_res_counts}\n')
print(f'gson_undefined_res_counts: {gson_undefined_res_counts}\n')
print(f'js_correct_res_counts: {js_correct_res_counts}\n')
print(f'js_errored_res_counts: {js_errored_res_counts}\n')
print(f'js_undefined_res_counts: {js_undefined_res_counts}\n')
print(f'orggson_correct_res_counts: {orggson_correct_res_counts}\n')
print(f'orggson_errored_res_counts: {orggson_errored_res_counts}\n')
print(f'orggson_undefined_res_counts: {orggson_undefined_res_counts}\n')

x = [
    datetime.datetime(2011, 1, 4, 0, 0),
    datetime.datetime(2011, 1, 5, 0, 0),
    datetime.datetime(2011, 1, 6, 0, 0)
]
x = date2num(x)

y = [4, 9, 2]
z = [1, 2, 3]
k = [11, 12, 13]

ax = plt.subplot(111)
ax_1 = ax.bar(x - 0.2, y, width=0.2, color='b', align='center')
ax_2 = ax.bar(x, z, width=0.2, color='g', align='center')
ax_3 = ax.bar(x + 0.2, k, width=0.2, color='r', align='center')
# ax.xaxis_date()
plt.legend((ax_1[0], ax_2[0], ax_3[0]), ('A', 'B', 'C'))

plt.show()
