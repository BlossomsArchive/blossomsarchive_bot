import datetime
now = datetime.datetime.now()

f2 = open("test.txt", "a")
f2.write('{0:%Y%m%d}'.format(now))
f2.close
