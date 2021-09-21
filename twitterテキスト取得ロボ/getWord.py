import tweepy
import csv
import pandas as pd
import codecs
import datetime
import os

consumer_key = "JwFKpWvNr4f2TLqrFtNto0jsL"
consumer_secret = "hnkDRJeryenJgzGcWLYmwPC2YuT4vPamgf4Mmo6CJ5FQcldPR4"
access_key = "1408669003300544512-cOo823WEYgIj8IcWUsuL4wrdBw3uuI"
access_secret = "gLVPuPYqjfYPRXhqqjewcEbIjF6ixYV4iBHpefsi1fzrz"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

q = "新卒　やめたい"
count = 10

tweet_list = []

tweets = api.search(q=q, locale="ja", count=count, tweet_mode='extended')
for tweet in tweets:
    tweet_list.append([[tweet.user.id, tweet.user.followers_count,
                        tweet.user.friends_count, tweet.user.description],
                       [tweet.id, tweet.full_text, tweet.favorite_count,
                        tweet.retweet_count]])


# リストをデータフレーム変換
df = pd.DataFrame(tweet_list)

# アウトプットフォルダパス
outputFilePath = 'C:/Users/hm111/twitterテキスト取得ロボ'

# ファイル作成時間
now = datetime.datetime.now()

# フォーマット変更(年月-時分秒)
created_Time = now.strftime('%Y%m%d-%H%M%S')

# フォルダ名
outNameFolder = outputFilePath + "/" + created_Time

# フォルダ作成
os.makedirs(outNameFolder)

# ファイル名
tmpoutNameFile = outNameFolder + "/結果ファイル.csv"

with codecs.open(tmpoutNameFile, 'w', 'CP932', 'replace') as outNameFile:
    # ファイル作成
    df.to_csv(outNameFile, encoding="CP932")
