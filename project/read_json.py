# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 15:50:24 2019

@author: 蘇
"""

import json

path=r'D:\graduate\project\city_coordinates.json'

with open(path,'r',encoding='utf-8') as f:
    data=json.loads(f.read())
