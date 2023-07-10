# coding: utf-8

import os
import feedparser
from misskey import Misskey
import tweepy
from mastodon import Mastodon

f = open("feed.txt", "r")
old_up = f.read()
f.close()

post_list = "post-list.txt"

entries = feedparser.parse("https://blossomsarchive.com/blog/feed/")["entries"]

new_up = entries[0]["updated"]
f2 = open("feed.txt", "w")
f2.write(new_up)
f2.close()

i = 0
while True:
    now_entry = entries[i]
    if now_entry["updated"] == old_up:
        new_up = entries[0]["updated"]
        f3 = open(
            "feed.txt", "w"
        )
        f3.write(new_up)
        f3.close()
        break

    else:
        title = now_entry["title"]
        page_url = now_entry["link"]
        author = now_entry["author"]
        category = [t.get("term") for t in now_entry.tags]

        category_count = len(category)

        l = 0
        while True:
            if l < category_count:
                if not "ニュース" in category:
                    content_list_content = title + "," + page_url + "\n"
                    f4 = open(post_list, "a", encoding="utf-8")
                    f4.write(content_list_content)
                    f4.close

            else:
                break

            l += 1

        post_text = "【" + author + "がブログを更新しました】\n" + title + "\n" + page_url

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

    i += 1
