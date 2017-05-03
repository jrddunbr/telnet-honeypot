import os

usernames = {}
passwords = {}
scripts = []

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

def getUsernamePassword(filename): # returns username, password
    fa = open("logs/" + filename)
    line = fa.readline()
    split = line.split("'Password: ")
    try:
        username = split[0].split("Login: b'")[1].strip()
    except:
        try:
            username = split[0].strip()
        except:
            username = "INVALID"
    try:
        password = split[1].strip()
    except:
        password = "INVALID"
    return username, password

#
# Main Code - Reads all files, then  tells us what the passwords are,
# from most to least common.
# If the file is longer than 50 characters,
# we will consider them executable code,
# and combine the username and password as a script
# (as many bots do no actually send login information)
#

for item in filelist:
    ip, day, month, year, hour, minute, second = parseFilename(item)
    username, password = getUsernamePassword(item)
    if(len(username) + len(password) >= 50):
        # We're considering this a script! Yay!
        script = "".format(username, password)
        scripts.append(script)
    else:
        username = username.replace("\\n", "").replace("\\r","")
        # This is a standard username/password combo
        if(username not in usernames):
            usernames[username] = 1
        else:
            usernames[username] += 1
        if(password not in passwords):
            passwords[password] = 1
        else:
            passwords[password] += 1

print("We have {} unique logins".format(len(passwords)))

print("\nDetected Usernames:")

for username in sorted(usernames, key=usernames.get, reverse=True):
    print ("{},{}".format(usernames[username], username))

print("\nDetected Passwords:")

for password in sorted(passwords, key=passwords.get, reverse=True):
    print ("{},{}".format(passwords[password], password))
