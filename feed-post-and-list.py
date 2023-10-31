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
                    # api.notes_create(text=post_text)
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

i = 0
while True:
    now_entry = entries[i]
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

    # 4つのスレッドを作成し、それぞれ異なる関数を実行
    for i in range(1, 5):
        thread = threading.Thread(target=thread_function, args=(i,))
        threads.append(thread)
        thread.start()

    # 全てのスレッドが終了するのを待つ
    for thread in threads:
        thread.join()

    # すべてのスレッドが終了した後にメッセージを表示
    print(post_text)
    print("ALL Thread - Result: OK")
    print("-----------------------")
    i = i+1
    print(i)

print("All End")