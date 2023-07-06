import datetime
now = datetime.datetime.now()

f2 = open("post-list.txt", "a")
f2.write(str(now)+"\n")
f2.close

f2 = open("feed.txt", "w")
f2.write("Tue, 27 Jun 2023 14:00:07 +0000")
f2.close
