# coding: utf-8
import random
from misskey import Misskey
import tweepy
from mastodon import Mastodon
import os
from atproto import Client , models


# ファイル読み込み
with open("post-list.txt", "r", encoding="utf-8") as f:
    l = f.readlines()
    randomline = random.sample(l, 1)

# タイトルとURLを抽出
title_and_url = randomline[0]

# タイトルとURLをリストに変換
title_and_url_list = title_and_url.split(",", 1)

# タイトルを抽出
title = title_and_url_list[0]

# URLから末尾の\nを削除
post_url = title_and_url_list[1].replace("\n", "")

#投稿用フォーマットを作成
post_text = "【本日のおすすめ記事】"+"\n"+title+"\n"+post_url

#SNS投稿API
# Misskey
misskey_address = os.environ.get("MISSKEY_SERVER_ADDRESS")
misskey_token = os.environ.get("MISSKEY_TOKEN")
api = Misskey(misskey_address)
api.token = misskey_token
api.notes_create(text=post_text)

# Mastodon
mastdon_url = os.environ.get("MASTDON_BASE_URL")
mastdon_CID = os.environ.get("MASTDON_CLIENT_ID")
mastdon_secret = os.environ.get("MASTDON_SECRET")
mastdon_token = os.environ.get("MASTDON_TOKEN")
api = Mastodon(
    api_base_url=mastdon_url,
    client_id=mastdon_CID,
    client_secret=mastdon_secret,
    access_token=mastdon_token,
)
api.toot(post_text)

#bluesky
bluesky = Client()
bluesky.login(str(os.environ.get("BLUESKY_MAIL_ADDRESS")),str(os.environ.get("BLUESKY_PASSWORD")))
embed_external = models.AppBskyEmbedExternal.Main(
    external = models.AppBskyEmbedExternal.External(
        title = title,
        description = "BlossomsArchive",
        uri = post_url
    )
)
bluesky.send_post("【本日のおすすめ記事】"+"\n"+title ,embed = embed_external)

# Twitter
twitter_bearer_token = os.environ.get("TWITTER_BEARER_TOKEN")
twitter_consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
twitter_consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
twitter_access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
twitter_access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

client = tweepy.Client(
    bearer_token=twitter_bearer_token,
    consumer_key=twitter_consumer_key,
    consumer_secret=twitter_consumer_secret,
    access_token=twitter_access_token,
    access_token_secret=twitter_access_token_secret,
)

client.create_tweet(text=post_text)

print(post_text+"\n")
