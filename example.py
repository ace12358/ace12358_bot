from api import API
"""
sentences distant system using one-of-K (by word average)
"""
import sys 
import csv 
import shutil
import MeCab
import re
import os
import numpy as np
import scipy as sp
import scipy.spatial.distance


def make_vector(sent):
    """ 
    input: sentence 
    output: sentence_vector
    """
    tagger = MeCab.Tagger('-Owakati')
    result = tagger.parse(sent)
    sent_list = result.strip().split(' ')
    sentence_vector = dict()
    for word in sent_list:
        #word = word.decode("utf-8")
        sentence_vector[word]=1
    return sentence_vector

# database loading
database_sent_vector = dict()
for line in open(sys.argv[1]):
    sent = line.strip().split(',')[0]
    vec = make_vector(sent)
    database_sent_vector[sent]=vec

with API() as api:
    # ツイートする
    # api.tweet('tweet test2')

    # リプを取得
    for mention in api.get_mentions():
        text = mention['text']
        tweet_id = mention['id_str']
        screen_name = mention['user']['screen_name']
        # ユーザ情報(プロフィール)
        name = mention['user']['name']
        zone = mention['user']['time_zone']
        location = mention['user']['location']
        description = mention['user']['description']

    # リプを返す
        try:
            common_cnt = 0
            best_common_cnt=0
            best_answer = str()

            for sent, db_vector in database_sent_vector.items():
                for word in text:
                    if word in db_vector:
                        common_cnt+=1
                if common_cnt > best_common_cnt:
                    best_common_cnt = common_cnt
                    best_answer = sent
                common_cnt=0
            content = ' '.join(text.split()[1:])
            api.reply(content, tweet_id, screen_name)
        except(NameError):
            pass
