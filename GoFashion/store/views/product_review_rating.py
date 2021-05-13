from math import sqrt

import numpy as np
import pandas as pd
from django.db.models.aggregates import Avg
from django.http import HttpResponseRedirect
from pandas import DataFrame
from sklearn.metrics import mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity

from store.models import Customer
from store.models.product import Product
from store.models.product_review_rating import ProductReviewRating


def product_review_rating(request, ids):
    product = Product.objects.get(id=ids)
    if request.method == 'POST':
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content', '')
        customer_id = request.session.get('customer')
        user = Customer.objects.get(id=customer_id)

        review = ProductReviewRating.objects.create(product=product,
                                                    customer=user,
                                                    stars=stars,
                                                    content=content)
    # recommendation(product.name, user.id, product.id)
    url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(url)


# for recommendation system
def average_rate(product):
    reviews = ProductReviewRating.objects.filter(product=product).aggregate(average=Avg('stars'))
    avg = 0
    if reviews["average"] is not None:
        avg = float(reviews["average"])
    return avg


def fetch_data():
    products = Product.objects.all()
    product_list = []
    for product in products:
        product_list.append([product.id, product.name, int(average_rate(product))])
    # print(product_list)
    return product_list


def recommendation(argProductTitle, argUserID, argProductID):
    # ===================================
    # all product and average rating
    list_of_rate_product = fetch_data()
    # for x in range(len(list_of_rate_product)):
    #     print(list_of_rate_product[x])

    # all reviews
    allReview = ProductReviewRating.objects.all()
    reviewList = []

    for review in allReview:
        reviewList.append([review.customer.id, review.product.name, review.product.id, int(review.stars)])
        # for x in range(len(reviewList)):
    #     print(reviewList[x])

    # creating dataframe
    product = DataFrame(list_of_rate_product, columns=['ID', 'name', 'rating'])
    review = DataFrame(reviewList, columns=['uID', 'name', 'ID', 'rating'])

    #print(product)

    #print('=======================')

    #print(review)

    # # product_index
    product_index = pd.Series(product.index, index=product.name)
    # print(product_index.head())

    # merging
    joined = product.merge(review, how='inner', on='ID')
    #print(joined, 'merge')

    joined = joined[['uID', 'name_x', 'rating_y']]
    #
    # # pivt table
    pivot = pd.pivot_table(joined, index='name_x', columns='uID', values='rating_y')
    # print(pivot.head(20))
    print('===============')
    # # print(pivot.shape)
    #
    # print('===============')

    # drop row with missing value
    pivot.dropna(axis=1, how='all', inplace=True)
    #pivot.head()
    #
    # average subtraction
    pivot_norm = pivot.apply(lambda x: x - np.nanmean(x), axis=1)
    # print(pivot_norm.head(20))
    #
    # fill nan with 0
    pivot_norm.fillna(0, inplace=True)
    # print(pivot_norm.head())
    # ===================================
    #
    # # cosine similarity
    # print('===============')
    #
    item_sim_df = pd.DataFrame(cosine_similarity(pivot_norm, pivot_norm), index=pivot_norm.index,
                               columns=pivot_norm.index)
    #print(item_sim_df.head(20))

    # for similar items
    product_s = None
    scores = None

    product_name = argProductTitle
    max_neighbor = 2

    user_id = argUserID
    n_product = 4

    if product_name in pivot_norm.index:
        product_s = item_sim_df.sort_values(by=product_name, ascending=False).index[1:]
        scores = item_sim_df.sort_values(by=product_name, ascending=False).loc[:, product_name].tolist()[1:]

    else:
        return None

    #print('===============')

    for x, y in zip(product_s[:10], scores[:10]):
        print("{} with similarity of {}".format(x, y))

    #print('===============')

    # for predcting ratings
    product_arr = np.array([x for x in product_s])
    sim_arr = np.array([x for x in scores])

    predict_rating = None

    if argUserID in pivot_norm.columns:
        filtering = pivot_norm[user_id].loc[product_arr] != 0

        predict_rating = np.dot(sim_arr[filtering][:max_neighbor],
                                pivot[user_id].loc[product_arr[filtering][:max_neighbor]]) \
                         / np.sum(sim_arr[filtering][:max_neighbor])

        #print("Predicted rating: ", predict_rating)

    # error calculation
    # if predict_rating:
    #     if not np.any(np.isnan(predict_rating)):
    #         predicted_rate = [predict_rating]
    #         actual_user = review.loc[review['uID'] == argUserID]
    #         actual_product = actual_user.loc[actual_user['ID'] == argProductID]
    #         # print(actual_product, "actual product")
    #
    #         rate = actual_product['rating'].mean()
    #         if np.any(np.isnan(rate)):
    #             rate = 0
    #         # print(rate)
    #         rate = int(rate)
    #
    #         print('Actual rating: ', rate)
    #         rate_list = []
    #         rate_list.append(rate)
    #
    #         if rate_list is None:
    #             rate = [0]
    #         print("MSE: ", mean_squared_error(rate_list, predicted_rate))
    #         # calculate RMSE
    #         print("RMSE: ", sqrt(mean_squared_error(rate_list, predicted_rate)))
    # print('===============')

    # get recommendation
    predicted_rating = np.array([])

    for _product in pivot_norm.index:
        predicted_rating = np.append(predicted_rating, predict_rating)

    temp = pd.DataFrame({'predicted': predicted_rating, 'name': pivot_norm.index})
    # print(temp, "product and prediction")
    recommended_product = None

    if argUserID in pivot_norm.columns:
        filtering = (pivot_norm[user_id] == 0.0)
        # print(filtering, "hello")
        temp = temp.loc[filtering.values].sort_values(by='predicted', ascending=False)
        # print(product.loc[product_index.loc[temp.name[:n_product]]])
        recommended_product = product.loc[product_index.loc[temp.name[:n_product]]]

    items = []
    if recommended_product is not None:
        for item in recommended_product['name']:
            items.append(item)

    print("Recommended items: ", items)
    print("===============================")

    return items
# ==================================
