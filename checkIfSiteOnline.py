import requests
import sys
import time

try:
    website = "http://" + sys.argv[1]
except:
    print("\nSyntax: \ncheckIfSiteIsOnline.py <[sub.]domain.tld> </path/to/outputfile>\n")
    sys.exit()

try:
    path = sys.argv[2]
except:
    print("\nSyntax: \ncheckIfSiteIsOnline.py <[sub.]domain.tld> </path/to/outputfile>\n")
    sys.exit()
if path[len(path) - 1] != "/":
    path += "/"

s = requests.session()
try:
    request = s.get(website)
except requests.exceptions.RequestException:
    print(
        "\nThe website seems to be not reachable. Check the syntax and try again please!\n\nSyntax: \ncheckIfSiteIsOnline.py <[sub.]domain.tld> </path/to/outputfile>\n")
    sys.exit()

print("\nThe website", website, "is reachable. \nStatuscode:", request.status_code, "\n\n")
path += ""
site = website.removeprefix("http://")
outputfile = path+site+" erreichbar.txt"

file = open(outputfile, "w")
t = time.localtime()
requestTime = str(t[2]) + "-" + str(t[1]) + "-" + str(t[0]) + " -> " + str(t[3]) + ":" + str(t[4]) + ":" + str(t[5])
file.write(requestTime)
file.close()

sys.exit()
