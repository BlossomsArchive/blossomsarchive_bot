import datetime
now = datetime.datetime.now()

f2 = open("test.txt", "a")
f2.write(str(now)+"\n")
f2.close

#Tue, 27 Jun 2023 14:00:07 +0000
f2 = open("feed.txt", "a")
f2.write(str(now)+"\n")
f2.close
