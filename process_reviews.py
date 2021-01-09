# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 16:06:25 2021

@author: Paula
"""
import json
import csv

with open("data/review_1091500.json", 'r') as f:
    review_dict = json.load(f)

review_dict = review_dict["reviews"]
for k,v in review_dict.items():
    timestamp = v["timestamp_updated"]
    review = v["review"]
    
    with open('data/reviews.csv', mode='a+', encoding='utf8') as review_file:
        r = csv.writer(review_file, delimiter=',', 
                                     quotechar='"', quoting=csv.QUOTE_MINIMAL)
        r.writerow([timestamp, review])
    