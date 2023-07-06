import datetime
now = datetime.datetime.now()

f2 = open("test.txt", "a")
f2.write(str(now)+"\n")
f2.close
