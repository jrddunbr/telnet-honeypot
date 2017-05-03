import os

ips = []

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

#
# Main Code - Reads all files, then  tells us number of unique IP's

for item in filelist:
    ip, day, month, year, hour, minute, second = parseFilename(item)
    if ip not in ips:
        ips.append(ip)

print("There were {} unique IP's that attacked.".format(len(ips)))
