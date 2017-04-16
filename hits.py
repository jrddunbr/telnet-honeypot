import os

times = {}

filelist = os.listdir("logs")

def parseFilename(filename): # returns ip, day, month, year, hour, minute, second
    ip = item.split("~")[0].replace("_",".")
    time = item.split("~")[1].split(".")[0]
    year = time[0:4]
    month = time[4:6]
    day = time[6:8]
    hour = time[8:10]
    minute = time[10:12]
    second = time[12:14]
    return ip, day, month, year, hour, minute, second

for item in filelist:
    ip, day, month, year, hour, minute, second = parseFilename(item)
    datestring = "{}/{}/{} at {}:{}:{}".format(month, day, year, hour, minute, second)
    if datestring not in times:
        times[datestring] = 1
    else:
        times[datestring] += 1

csv = open("times.csv", "w+")
for time in sorted(times, key=times.get, reverse=True):
    csv.write("{},{}\n".format(times[time], time))
    #print ("{} of {}".format(times[time], time))
