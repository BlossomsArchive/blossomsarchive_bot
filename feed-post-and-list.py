# coding: utf-8
from misskey import Misskey
import tweepy
from mastodon import Mastodon
import os
from atproto import Client, models
import threading
import time
import feedparser


f = open("feed.txt", "r")
old_up = f.read()
f.close()

post_list = "post-list.txt"

entries = feedparser.parse("https://blossomsarchive.com/blog/feed/")["entries"]

new_up = entries[0]["updated"]
f2 = open("feed.txt", "w")
f2.write(new_up)
f2.close()

while_count = 0
while True:
    now_entry = entries[while_count]
    if now_entry["updated"] == old_up:
        new_up = entries[0]["updated"]
        f3 = open("feed.txt", "w")
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


    # スレッドが終了したことを追跡するためのリスト
    threads = []


    # 各スレッドで実行する関数
    def thread_function(thread_id):
        # Misskey
        if thread_id == 1:
            # 処理内容
            a = 1
            while True:
                try:
                    if a != 20:
                        api = Misskey(os.environ.get("MISSKEY_SERVER_ADDRESS"))
                        api.token = os.environ.get("MISSKEY_TOKEN")
                        #api.notes_create(text=post_text)
                        print("Misskey - "+title)
                    else:
                        break
                except:
                    print(f"Misskey - Result: NO")
                    print(f"Misskey - ReTry: {a}")
                    a = a + 1
                    time.sleep(300)
                else:
                    print(f"Misskey - Result: OK")
                    break

        # Mastodon
        elif thread_id == 2:
            # 処理内容
            b = 1
            while True:
                try:
                    if b != 20:
                        api = Mastodon(
                            api_base_url=os.environ.get("MASTDON_BASE_URL"),
                            client_id=os.environ.get("MASTDON_CLIENT_ID"),
                            client_secret=os.environ.get("MASTDON_SECRET"),
                            access_token=os.environ.get("MASTDON_TOKEN"),
                        )
                        #api.toot(post_text)
                        print("Mastdon - "+title)
                    else:
                        break
                except:
                    print(f"Mastdon - Result: NO")
                    print(f"Mastdon - ReTry: {b}")
                    b = b + 1
                    time.sleep(300)
                else:
                    print(f"Mastdon - Result: OK")
                    break

        # Bluesky
        elif thread_id == 3:
            # 処理内容
            c = 1
            while True:
                try:
                    if c != 20:
                        bluesky = Client()
                        bluesky.login(
                            str(os.environ.get("BLUESKY_MAIL_ADDRESS")),
                            str(os.environ.get("BLUESKY_PASSWORD")),
                        )
                        embed_external = models.AppBskyEmbedExternal.Main(
                            external=models.AppBskyEmbedExternal.External(
                                title=title, description="BlossomsArchive", uri=page_url
                            )
                        )
                        #bluesky.send_post("【" + author + "がブログを更新しました】\n" + title ,embed = embed_external)
                        print("Bluesky - "+title)
                    else:
                        break
                except:
                    print(f"Bluesky - Result: NO")
                    print(f"Bluesky - ReTry: {c}")
                    c = c + 1
                    time.sleep(300)
                else:
                    print(f"Bluesky - Result: OK")
                    break

        # Twitter
        elif thread_id == 4:
            # 処理内容
            d = 1
            while True:
                try:
                    if d != 20:
                        client = tweepy.Client(
                            bearer_token=os.environ.get("TWITTER_BEARER_TOKEN"),
                            consumer_key=os.environ.get("TWITTER_CONSUMER_KEY"),
                            consumer_secret=os.environ.get("TWITTER_CONSUMER_SECRET"),
                            access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
                            access_token_secret=os.environ.get(
                                "TWITTER_ACCESS_TOKEN_SECRET"
                            ),
                        )
                        #client.create_tweet(text=post_text)
                        print("Twitter - "+title)
                    else:
                        break
                except:
                    print(f"Twitter - Result: NO")
                    print(f"Twitter - ReTry: {d}")
                    d = d + 1
                    time.sleep(300)
                else:
                    print(f"Twitter - Result: OK")
                    break


    # 4つのスレッドを作成し、それぞれ異なる関数を実行
    for i in range(1, 5):
        thread = threading.Thread(target=thread_function, args=(i,))
        threads.append(thread)
        thread.start()

    # 全てのスレッドが終了するのを待つ
    for thread in threads:
        thread.join()

    # すべてのスレッドが終了した後にメッセージを表示
    print("\n" + post_text + "\n")
    while_count += 1
        
print("All End")