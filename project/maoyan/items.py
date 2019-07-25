# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cmdate = scrapy.Field()#'time'评论日期
    cmtime = scrapy.Field()#"time"评论时间
    userId = scrapy.Field()#'userID'用户ID
    cityName = scrapy.Field()#'cityName'城市
    content = scrapy.Field()#'content'评论
    gender = scrapy.Field()#'gender'性别
    nickName = scrapy.Field()#'nickName'昵称
    userLevel = scrapy.Field()#'userLevel'用户等级
    score =scrapy.Field()#'score'电影评分
    
