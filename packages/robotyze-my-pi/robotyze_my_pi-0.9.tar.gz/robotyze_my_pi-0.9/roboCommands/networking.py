import subprocess

def ping(ipAddress, numberOfTimes=5):
    p = subprocess.Popen(["ping", "-c", str(numberOfTimes), ipAddress], stdout=subprocess.PIPE)
    out, err = p.communicate()
    print(out.decode('utf-8'))
    return out.decode('utf-8')

def findIP():
    p = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
    out, err = p.communicate()
    ipAddresses = out.decode('utf-8')
    linesplitIP = ipAddresses.split("\n")
    currentAddresses = {}
    networkIdentifier = ["wlan", "wlp", "eth", "enp"]
    for wifi in networkIdentifier:
        try:
            temp = ipAddresses.split(wifi)[1].split("inet ")[1].split(" ")[0]
        except IndexError:
            print(wifi + " doesn't exist.")
        for line in linesplitIP:
            if (wifi in line):
                currentAddresses[line.split(":")[0]] = temp
            if len(currentAddresses[line.split(":")[0]].split(".")) < 4
    return currentAddresses

def ipChange(ipAddress):
