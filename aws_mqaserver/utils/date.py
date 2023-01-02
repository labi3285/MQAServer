
import datetime, time

date = time.localtime(1640966401)
date1 = datetime.datetime.fromtimestamp(1640966401)
print(date)
print(date1)

# print(int(date1.strftime("%D", date)))

print(date1.strftime("%W"))

print(date1.year)
print(date1.month)
print(date1.day)

# print(date1[1])
# print(date1[2] == 31)