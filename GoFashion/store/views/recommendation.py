# from math import sqrt
#
# import numpy as np
# import pandas as pd
# from sklearn.metrics import mean_squared_error
# from sklearn.neighbors import NearestNeighbors
#
# # Read the data
# df = pd.read_excel("Dataset.xlsx")
# df.head()
# df.shape
#
# new_df = df.drop(['Title'], axis=1)
# new_df.head()
#
# missing_pivot = new_df.pivot_table(values='Rating', index='UserID', columns='ProductName')
# missing_pivot.head()
# missing_pivot.shape
#
# rate = {}
# rows_indexes = {}
# for i, row in missing_pivot.iterrows():
#     rows = [x for x in range(0, len(missing_pivot.columns))]
#     combine = list(zip(row.index, row.values, rows))
#     rated = [(x, z) for x, y, z in combine if str(y) != 'nan']
#     index = [i[1] for i in rated]
#     row_names = [i[0] for i in rated]
#     rows_indexes[i] = index
#     rate[i] = row_names
# rate
#
# pivot_table = new_df.pivot_table(values='Rating', index='UserID', columns='ProductName').fillna(0)
# pivot_table = pivot_table.apply(np.sign)
# pivot_table.head()
#
# notrated = {}
# notrated_indexes = {}
# for i, row in pivot_table.iterrows():
#     rows = [x for x in range(0, len(missing_pivot.columns))]
#     combine = list(zip(row.index, row.values, row))
#     idx_row = [(idx, col) for idx, val, col in combine if not val > 0]
#     indices = [i[1] for i in idx_row]
#     row_names = [i[0] for i in idx_row]
#     notrated_indexes[i] = indices
#     notrated[i] = row_names
# notrated
#
# n = 3  # closest 3 neighbors to an item
# cosine_nn = NearestNeighbors(n_neighbors=n, algorithm='brute', metric='cosine')
# item_cosine_nn_fit = cosine_nn.fit(pivot_table.T.values)
# item_distances, item_indices = item_cosine_nn_fit.kneighbors(pivot_table.T.values)
#
# items_dic = {}
# for i in range(len(pivot_table.T.index)):
#     item_idx = item_indices[i]
#     col_names = pivot_table.T.index[item_idx].tolist()
#     items_dic[pivot_table.T.index[i]] = col_names
# items_dic
#
# topRecs = {}
# for k, v in rows_indexes.items():  # k = actual user
#     item_idx = [j for i in item_indices[v] for j in i]  # v = most similar to the products that they have already rated
#     item_dist = [j for i in item_distances[v] for j in i]
#     combine = list(zip(item_dist, item_idx))
#     diction = {i: d for d, i in combine if i not in v}
#     zipped = list(zip(diction.keys(), diction.values()))
#     sort = sorted(zipped, key=lambda x: x[1])
#     recommendations = [(pivot_table.columns[i], d) for i, d in sort]
#     topRecs[k] = recommendations
# topRecs
#
#
# def getrecommendations(user, number_of_recs=30):
#     if user > len(pivot_table.index):
#         print('Out of range, there are only {} users, try again!'.format(len(pivot_table.index)))
#     else:
#         print('These are all the clothes you have viewed in the past: \n\n{}'.format('\n'.join(rate[user])))
#         print()
#         print('We recommend to have a look on these clothes too in case you like them:\n')
#     for k, v in topRecs.items():
#         if user == k:
#             for i in v[:number_of_recs]:
#                 print('{} with simlarity: {:.4f}'.format(i[0], 1 - i[1]))
#
#
# getrecommendations(15)
#
# item_distances = 1 - item_distances
# predictions = item_distances.T.dot(pivot_table.T.values) / np.array([np.abs(item_distances.T).sum(axis=1)]).T
# ground_truth = pivot_table.T.values[item_distances.argsort()[0]]
#
#
# def rmse(prediction, ground_truth):
#     prediction = prediction[ground_truth.nonzero()].flatten()
#     ground_truth = ground_truth[ground_truth.nonzero()].flatten()
#     return sqrt(mean_squared_error(prediction, ground_truth))
#
#
# error_rate = rmse(predictions, ground_truth)
# accuracy = ('Accuracy: {:.3f}'.format(100 - error_rate))
# loss = ('RMSE: {:.3f}'.format(error_rate))
# print(accuracy)
# print(loss)


from math import sqrt
#from store.models.product import Product

from django.db.models.aggregates import Avg
#from store.views import product_review_rating

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import NearestNeighbors
from django.apps import apps
Product = apps.get_model(app_label='store', model_name='Product')
Review = apps.get_model(app_label='store', model_name='ProductReviewRating')
print(Product)

def average_rate(product):
        reviews = Review.objects.filter(product=product).aggregate(average=Avg('stars'))
        avg=0
        if reviews["average"] is not None:
            avg=float(reviews["average"])
        return avg

def fetch_data():
    products = Product.objects.all()
    product_list = []
    for product in products:
        product_list.append([product.id, product.title, int(average_rate(product))])
    return product_list
print(fetch_data())


from django.db.models.aggregates import Avg