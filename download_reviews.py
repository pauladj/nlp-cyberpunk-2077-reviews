# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 15:55:07 2021

@author: Paula
"""
import steamreviews

request_params = dict()
request_params['language'] = 'english'
request_params['review_type'] = 'recent'
request_params['purchase_type'] = 'steam'
request_params['num_per_page'] = '100'
request_params['day_range'] = '7'

app_id = 1091500
review_dict, query_count = steamreviews.download_reviews_for_app_id(
    app_id, chosen_request_params=request_params, verbose=True)