import os, random

usernames = {}
passwords = {}
scripts = []
ips = []

filelist = os.listdir("../logs")

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
    fa = open("../logs/" + filename)
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
    if ip not in ips:
        ips.append(ip)
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



#print("We have {} unique logins".format(len(passwords)))

#print("\nDetected Usernames:")

udata = ""
uname = ""
pdata = ""
pname = ""
color1 = ""
color2 = ""

for username in sorted(usernames, key=usernames.get, reverse=True):
    udata += "{},".format(usernames[username])
    uname += "\"{}\",".format(username.replace('"','').replace('\'', ''))
    color1 += "'rgb({},{},{})',".format(random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255))
    #print ("{} of {}".format(usernames[username], username))

#print("\nDetected Passwords:")

for password in sorted(passwords, key=passwords.get, reverse=True):
    pdata += "{},".format(passwords[password])
    pname += "\"{}\",".format(password.replace('"','').replace('\'', ''))
    color2 += "'rgb({},{},{})',".format(random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255))
    #print ("{} of {}".format(passwords[password], password))

fil = "<html><head><title>Honeypot Information</title><script src=\"chart.js\"></script></head><body><div><p>Number of unique IP addresses: " + str(len(ips)) + "</p><p>Number of unique logins: " + str(len(passwords)) + "</p></div><div id=\"canvas-holder\" style=\"width:40%\"><canvas id=\"usernames\" /></div><div id=\"canvas-holder2\" style=\"width:40%\"><canvas id=\"passwords\" /></div><script>var config = {type: 'doughnut',data: {datasets: [{data: [" + udata + "],backgroundColor: [" + color1 + "],}],labels: [" + uname + "]},options: {responsive: true,legend: {position: 'top',},title: {display: true,text: 'Usernames'},}};var config2 = {type: 'doughnut',data: {datasets: [{data: [" + pdata + "],backgroundColor: [" + color2 + "],}],labels: [" + pname + "]},options: {responsive: true,legend: {position: 'top',},title: {display: true,text: 'Passwords'},}};window.onload = function() {var ctx = document.getElementById(\"usernames\").getContext(\"2d\");window.un = new Chart(ctx, config);var ctx2 = document.getElementById(\"passwords\").getContext(\"2d\");window.pn = new Chart(ctx2, config2);};</script></html>"

ind = open("/srv/http/index.html", "w+")
ind.write(fil)
ind.close()
